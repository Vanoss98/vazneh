from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    BlogPost,
    ContactMessage,
    HiringRequest,
    Project,
    ProjectFeature,
    ProjectGalleryImage,
    Representative,
    Service,
    ServiceGalleryImage,
    ServiceItem,
    Product,
    ProductCapacity,
    ProductFeature,
    ProductGalleryImage,
    ProductSize,
    ProductType,
)


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"

    def clean_related_posts(self):
        posts = self.cleaned_data["related_posts"]
        if posts.count() > 3:
            raise forms.ValidationError(_("حداکثر سه مطلب مرتبط انتخاب کنید."))
        if self.instance.pk and posts.filter(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("مطلب نمی‌تواند به خودش مرتبط باشد."))
        return posts


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_similar_products(self):
        products = self.cleaned_data["similar_products"]
        if products.count() > 3:
            raise forms.ValidationError(_("حداکثر سه محصول مشابه انتخاب کنید."))
        if self.instance.pk and products.filter(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("محصول نمی‌تواند مشابه خودش باشد."))
        return products


class ProductCapacityInline(admin.TabularInline):
    model = ProductCapacity
    extra = 1
    fields = ("title", "title_en", "position")


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ("title", "title_en", "position")


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1
    fields = ("title", "title_en", "position")


class ProductGalleryImageInline(admin.TabularInline):
    model = ProductGalleryImage
    extra = 1
    fields = ("image", "alt_text", "alt_text_en", "position")


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1
    fields = ("title", "title_en", "position")


class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1
    fields = ("image", "alt_text", "alt_text_en", "position")


class ServiceItemInline(admin.StackedInline):
    model = ServiceItem
    extra = 1
    fields = (
        "kind",
        "title",
        "title_en",
        "description",
        "description_en",
        "position",
    )


class ServiceGalleryImageInline(admin.TabularInline):
    model = ServiceGalleryImage
    extra = 1
    fields = ("image", "alt_text", "alt_text_en", "position")


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "title_en", "position")
    list_editable = ("position",)
    search_fields = ("title", "title_en")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        "title",
        "product_type",
        "price",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "product_type", "created_at")
    list_editable = ("price", "is_active")
    search_fields = (
        "title",
        "title_en",
        "subtitle",
        "subtitle_en",
        "short_description",
        "short_description_en",
        "detailed_description",
        "detailed_description_en",
    )
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("product_type", "similar_products")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    inlines = (
        ProductCapacityInline,
        ProductSizeInline,
        ProductFeatureInline,
        ProductGalleryImageInline,
    )
    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": (
                    "product_type",
                    "title",
                    "title_en",
                    "slug",
                    "subtitle",
                    "subtitle_en",
                    "short_description",
                    "short_description_en",
                    "detailed_description",
                    "detailed_description_en",
                    "price",
                    "is_active",
                )
            },
        ),
        (
            "فایل‌ها و تصاویر",
            {"fields": ("main_image", "header_image", "catalog_file")},
        ),
        ("محصولات مشابه", {"fields": ("similar_products",)}),
        ("تاریخ‌ها", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "location",
        "latitude",
        "longitude",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "location", "created_at")
    list_editable = ("is_active",)
    search_fields = (
        "title",
        "title_en",
        "subtitle",
        "subtitle_en",
        "description",
        "description_en",
        "location",
        "location_en",
    )
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    inlines = (ProjectFeatureInline, ProjectGalleryImageInline)
    fieldsets = (
        (
            "اطلاعات پروژه",
            {
                "fields": (
                    "title",
                    "title_en",
                    "slug",
                    "subtitle",
                    "subtitle_en",
                    "description",
                    "description_en",
                    "main_image",
                    "is_active",
                )
            },
        ),
        (
            "موقعیت روی نقشه",
            {"fields": ("location", "location_en", "latitude", "longitude")},
        ),
        ("تاریخ‌ها", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "phone", "message")
    readonly_fields = ("name", "phone", "message", "created_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False


@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "phone",
        "latitude",
        "longitude",
        "is_active",
    )
    list_filter = ("is_active", "city")
    list_editable = ("is_active",)
    search_fields = (
        "name",
        "name_en",
        "city",
        "city_en",
        "phone",
        "address",
        "address_en",
    )
    fieldsets = (
        (
            "اطلاعات نماینده",
            {
                "fields": (
                    "name",
                    "name_en",
                    "city",
                    "city_en",
                    "phone",
                    "address",
                    "address_en",
                    "is_active",
                )
            },
        ),
        ("موقعیت روی نقشه", {"fields": ("latitude", "longitude")}),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "position", "is_active", "updated_at")
    list_filter = ("is_active", "created_at")
    list_editable = ("position", "is_active")
    search_fields = (
        "title",
        "title_en",
        "subtitle",
        "subtitle_en",
        "short_description",
        "short_description_en",
        "detailed_description",
        "detailed_description_en",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    inlines = (ServiceItemInline, ServiceGalleryImageInline)
    fieldsets = (
        (
            "محتوای خدمت",
            {
                "fields": (
                    "title",
                    "title_en",
                    "slug",
                    "subtitle",
                    "subtitle_en",
                    "short_description",
                    "short_description_en",
                    "detailed_description",
                    "detailed_description_en",
                    "position",
                    "is_active",
                )
            },
        ),
        (
            "تصاویر و فایل‌ها",
            {"fields": ("main_image", "header_image", "catalog_file")},
        ),
        ("تاریخ‌ها", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(HiringRequest)
class HiringRequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "desired_position",
        "phone",
        "is_reviewed",
        "created_at",
    )
    list_filter = ("is_reviewed", "desired_position", "created_at")
    list_editable = ("is_reviewed",)
    search_fields = ("full_name", "phone", "email", "desired_position", "message")
    readonly_fields = (
        "full_name",
        "phone",
        "email",
        "desired_position",
        "experience_years",
        "message",
        "resume",
        "created_at",
    )
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "اطلاعات متقاضی",
            {
                "fields": (
                    "full_name",
                    "phone",
                    "email",
                    "desired_position",
                    "experience_years",
                )
            },
        ),
        ("رزومه و معرفی", {"fields": ("message", "resume")}),
        ("وضعیت", {"fields": ("is_reviewed", "created_at")}),
    )

    def has_add_permission(self, request):
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = (
        "title",
        "author_name",
        "is_published",
        "is_featured",
        "published_at",
    )
    list_filter = ("is_published", "is_featured", "published_at", "created_at")
    list_editable = ("is_published", "is_featured")
    search_fields = (
        "title",
        "title_en",
        "excerpt",
        "excerpt_en",
        "body",
        "body_en",
        "author_name",
        "author_name_en",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("related_posts",)
    date_hierarchy = "published_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "محتوای مطلب",
            {
                "fields": (
                    "title",
                    "title_en",
                    "slug",
                    "excerpt",
                    "excerpt_en",
                    "body",
                    "body_en",
                    "cover_image",
                    "author_name",
                    "author_name_en",
                )
            },
        ),
        (
            "انتشار",
            {
                "fields": (
                    "published_at",
                    "is_published",
                    "is_featured",
                )
            },
        ),
        ("مطالب مشابه", {"fields": ("related_posts",)}),
        ("تاریخ‌ها", {"fields": ("created_at", "updated_at")}),
    )
