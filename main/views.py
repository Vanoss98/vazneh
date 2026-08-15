import hashlib
import logging
from decimal import Decimal, InvalidOperation

from django.core.cache import cache
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Max, Min, Prefetch, Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import get_language, gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import ContactMessageForm, HiringRequestForm
from .models import (
    BlogPost,
    ContactMessage,
    HiringRequest,
    Project,
    Product,
    ProductCapacity,
    ProductSize,
    ProductType,
    Representative,
    Service,
    ServiceItem,
)


logger = logging.getLogger(__name__)


def unique_items_by_title(queryset):
    """Keep filter values stable while exposing their localized labels."""
    seen = set()
    items = []
    for item in queryset:
        if item.title in seen:
            continue
        seen.add(item.title)
        items.append(item)
    return items


class HomePageView(TemplateView):
    template_name = "main/index.html"


class AboutPageView(TemplateView):
    template_name = "main/about.html"


class TeamPageView(TemplateView):
    template_name = "main/team.html"


class ServiceListView(ListView):
    model = Service
    template_name = "main/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.filter(is_active=True).order_by("position", "title")


class ServiceDetailView(DetailView):
    model = Service
    template_name = "main/service_detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return Service.objects.filter(is_active=True).prefetch_related(
            "items",
            "gallery_images",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_items = list(self.object.items.all())
        gallery_images = list(self.object.gallery_images.all())
        context.update(
            {
                "benefits": [
                    item
                    for item in service_items
                    if item.kind == ServiceItem.Kind.BENEFIT
                ],
                "process_items": [
                    item
                    for item in service_items
                    if item.kind == ServiceItem.Kind.PROCESS
                ],
                "gallery_images": gallery_images,
                "primary_gallery_image": gallery_images[0]
                if gallery_images
                else None,
                "related_services": Service.objects.filter(is_active=True)
                .exclude(pk=self.object.pk)
                .order_by("position")[:3],
            }
        )
        return context


class HiringPageView(SuccessMessageMixin, CreateView):
    model = HiringRequest
    form_class = HiringRequestForm
    template_name = "main/hiring.html"
    success_url = reverse_lazy("main:hiring")
    success_message = _(
        "درخواست همکاری شما ثبت شد. پس از بررسی با شما تماس می‌گیریم."
    )
    throttle_limit = 5
    throttle_window = 10 * 60

    def get_throttle_key(self):
        client_address = self.request.META.get("REMOTE_ADDR", "unknown")
        digest = hashlib.sha256(client_address.encode("utf-8")).hexdigest()[:24]
        return f"hiring-request:{digest}"

    def post(self, request, *args, **kwargs):
        throttle_key = self.get_throttle_key()
        attempts = cache.get(throttle_key, 0)
        if attempts >= self.throttle_limit:
            logger.warning("Hiring form rate limit reached for %s", throttle_key)
            form = self.get_form()
            form.add_error(
                None,
                _(
                    "تعداد درخواست‌های شما زیاد است. لطفاً چند دقیقه دیگر دوباره تلاش کنید."
                ),
            )
            return self.form_invalid(form)

        cache.set(throttle_key, attempts + 1, self.throttle_window)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info("Hiring request %s created", self.object.pk)
        return response


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "main/blog_list.html"
    context_object_name = "posts"
    paginate_by = 6

    sort_options = {
        "newest": ("-published_at", "-pk"),
        "oldest": ("published_at", "pk"),
        "alphabetical": ("title", "pk"),
    }

    def get_queryset(self):
        requested_sort = self.request.GET.get("sort", "newest")
        self.current_sort = (
            requested_sort if requested_sort in self.sort_options else "newest"
        )
        queryset = BlogPost.objects.filter(
            is_published=True,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
        )
        ordering = self.sort_options[self.current_sort]
        if self.current_sort == "alphabetical" and get_language() == "en":
            ordering = ("title_en", "pk")
        return queryset.order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_parameters = self.request.GET.copy()
        query_parameters.pop("page", None)
        context.update(
            {
                "current_sort": self.current_sort,
                "blog_querystring": query_parameters.urlencode(),
            }
        )
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "main/blog_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        published_related_posts = BlogPost.objects.filter(
            is_published=True,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
        ).order_by("-published_at")
        return BlogPost.objects.filter(
            is_published=True,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
        ).prefetch_related(
            Prefetch(
                "related_posts",
                queryset=published_related_posts,
                to_attr="published_related_posts",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_posts = BlogPost.objects.filter(
            is_published=True,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
        )
        related_posts = list(self.object.published_related_posts[:3])

        if len(related_posts) < 3:
            excluded_ids = [self.object.pk, *(item.pk for item in related_posts)]
            related_posts.extend(
                published_posts.exclude(pk__in=excluded_ids).order_by(
                    "-published_at"
                )[: 3 - len(related_posts)]
            )

        context["related_posts"] = related_posts
        return context


class ContactPageView(SuccessMessageMixin, CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = "main/contact.html"
    success_url = reverse_lazy("main:contact")
    success_message = _(
        "پیام شما با موفقیت ارسال شد. به‌زودی با شما تماس می‌گیریم."
    )


class RepresentativeListView(ListView):
    model = Representative
    template_name = "main/representative_list.html"
    context_object_name = "representatives"

    def get_queryset(self):
        queryset = Representative.objects.filter(is_active=True)
        self.search_query = self.request.GET.get("q", "").strip()
        if self.search_query:
            queryset = queryset.filter(
                Q(name__icontains=self.search_query)
                | Q(name_en__icontains=self.search_query)
                | Q(city__icontains=self.search_query)
                | Q(city_en__icontains=self.search_query)
                | Q(address__icontains=self.search_query)
                | Q(address_en__icontains=self.search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query
        context["map_representatives"] = [
            {
                "name": representative.display_name,
                "city": representative.display_city,
                "phone": representative.phone,
                "latitude": float(representative.latitude),
                "longitude": float(representative.longitude),
            }
            for representative in self.object_list
        ]
        return context


class ProductListView(ListView):
    model = Product
    template_name = "main/product_list.html"
    context_object_name = "products"
    paginate_by = 8

    sort_options = {
        "newest": ("-created_at", "-pk"),
        "oldest": ("created_at", "pk"),
        "price_asc": ("price", "title"),
        "price_desc": ("-price", "title"),
        "alphabetical": ("title", "pk"),
    }

    @staticmethod
    def parse_price(value):
        if not value:
            return None
        try:
            price = Decimal(value)
        except (InvalidOperation, TypeError, ValueError):
            return None
        return price if price >= 0 else None

    def get_queryset(self):
        queryset = (
            Product.objects.filter(is_active=True)
            .select_related("product_type")
            .prefetch_related("capacities", "sizes")
        )

        product_types = self.request.GET.getlist("type")
        capacities = self.request.GET.getlist("capacity")
        sizes = self.request.GET.getlist("size")
        minimum_price = self.parse_price(self.request.GET.get("min_price"))
        maximum_price = self.parse_price(self.request.GET.get("max_price"))

        if product_types:
            queryset = queryset.filter(product_type__slug__in=product_types)
        if capacities:
            queryset = queryset.filter(capacities__title__in=capacities)
        if sizes:
            queryset = queryset.filter(sizes__title__in=sizes)
        if minimum_price is not None:
            queryset = queryset.filter(price__gte=minimum_price)
        if maximum_price is not None:
            queryset = queryset.filter(price__lte=maximum_price)

        requested_sort = self.request.GET.get("sort", "newest")
        self.current_sort = (
            requested_sort if requested_sort in self.sort_options else "newest"
        )
        ordering = self.sort_options[self.current_sort]
        if self.current_sort == "alphabetical" and get_language() == "en":
            ordering = ("title_en", "pk")
        return queryset.distinct().order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_types = self.request.GET.getlist("type")
        selected_capacities = self.request.GET.getlist("capacity")
        selected_sizes = self.request.GET.getlist("size")
        price_limits = Product.objects.filter(is_active=True).aggregate(
            minimum=Min("price"),
            maximum=Max("price"),
        )
        price_minimum = price_limits["minimum"] or Decimal("0")
        price_maximum = price_limits["maximum"] or Decimal("1000")
        if price_minimum == price_maximum:
            price_maximum += Decimal("1")

        selected_minimum = self.parse_price(self.request.GET.get("min_price"))
        selected_maximum = self.parse_price(self.request.GET.get("max_price"))
        selected_minimum = max(selected_minimum or price_minimum, price_minimum)
        selected_maximum = min(selected_maximum or price_maximum, price_maximum)
        if selected_minimum > selected_maximum:
            selected_minimum = price_minimum
            selected_maximum = price_maximum

        query_parameters = self.request.GET.copy()
        query_parameters.pop("page", None)
        context.update(
            {
                "product_types": ProductType.objects.all(),
                "capacity_options": unique_items_by_title(
                    ProductCapacity.objects.order_by("title", "position")
                ),
                "size_options": unique_items_by_title(
                    ProductSize.objects.order_by("title", "position")
                ),
                "current_sort": self.current_sort,
                "selected_types": selected_types,
                "selected_capacities": selected_capacities,
                "selected_sizes": selected_sizes,
                "price_minimum": int(price_minimum),
                "price_maximum": int(price_maximum),
                "selected_minimum": int(selected_minimum),
                "selected_maximum": int(selected_maximum),
                "filter_querystring": query_parameters.urlencode(),
            }
        )
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "main/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related("product_type")
            .prefetch_related(
                "capacities",
                "sizes",
                "features",
                "gallery_images",
                Prefetch(
                    "similar_products",
                    queryset=Product.objects.filter(is_active=True).select_related(
                        "product_type"
                    ),
                ),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery_images = list(self.object.gallery_images.all())
        selected_products = list(self.object.similar_products.all()[:3])

        if len(selected_products) < 3 and self.object.product_type_id:
            selected_ids = [product.pk for product in selected_products]
            fallback_products = (
                Product.objects.filter(
                    is_active=True,
                    product_type_id=self.object.product_type_id,
                )
                .exclude(pk__in=[self.object.pk, *selected_ids])
                .select_related("product_type")[: 3 - len(selected_products)]
            )
            selected_products.extend(fallback_products)

        context["gallery_images"] = gallery_images
        context["primary_gallery_image"] = gallery_images[0] if gallery_images else None
        context["similar_products"] = selected_products
        return context


class ProjectListView(ListView):
    model = Project
    template_name = "main/project_list.html"
    context_object_name = "projects"
    paginate_by = 8

    sort_options = {
        "newest": ("-created_at", "-pk"),
        "oldest": ("created_at", "pk"),
        "alphabetical": ("title", "pk"),
    }

    def get_queryset(self):
        queryset = Project.objects.filter(is_active=True)
        self.search_query = self.request.GET.get("q", "").strip()
        if self.search_query:
            queryset = queryset.filter(
                Q(title__icontains=self.search_query)
                | Q(title_en__icontains=self.search_query)
                | Q(subtitle__icontains=self.search_query)
                | Q(subtitle_en__icontains=self.search_query)
                | Q(description__icontains=self.search_query)
                | Q(description_en__icontains=self.search_query)
                | Q(location__icontains=self.search_query)
                | Q(location_en__icontains=self.search_query)
            )

        requested_sort = self.request.GET.get("sort", "newest")
        self.current_sort = (
            requested_sort if requested_sort in self.sort_options else "newest"
        )
        ordering = self.sort_options[self.current_sort]
        if self.current_sort == "alphabetical" and get_language() == "en":
            ordering = ("title_en", "pk")
        return queryset.order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        map_projects = [
            {
                "title": project.display_title,
                "location": project.display_location,
                "latitude": float(project.latitude),
                "longitude": float(project.longitude),
                "url": project.get_absolute_url(),
            }
            for project in self.object_list
            if project.latitude is not None and project.longitude is not None
        ]
        query_parameters = self.request.GET.copy()
        query_parameters.pop("page", None)
        context.update(
            {
                "current_sort": self.current_sort,
                "search_query": self.search_query,
                "map_projects": map_projects,
                "project_querystring": query_parameters.urlencode(),
            }
        )
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "main/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(is_active=True).prefetch_related(
            "features",
            "gallery_images",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery_images = list(self.object.gallery_images.all())
        context["gallery_images"] = gallery_images
        context["primary_gallery_image"] = gallery_images[0] if gallery_images else None
        return context
