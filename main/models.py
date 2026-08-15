from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import get_language, gettext_lazy as _
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


PHONE_VALIDATOR = RegexValidator(
    regex=r"^[0-9۰-۹+()\-\s]{7,30}$",
    message=_("شماره تلفن واردشده معتبر نیست."),
)


class Catalog(models.Model):
    file = models.FileField(
        upload_to="catalogs/",
        max_length=500,
        validators=[FileExtensionValidator(allowed_extensions=("pdf",))],
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-pk"]
        verbose_name = "کاتالوگ"
        verbose_name_plural = "کاتالوگ"

    def __str__(self):
        return "کاتالوگ شرکت وزنه"


def validate_resume_size(uploaded_file):
    if uploaded_file.size > 5 * 1024 * 1024:
        raise ValidationError(_("حجم فایل رزومه نباید بیشتر از ۵ مگابایت باشد."))


class LocalizedFieldsMixin:
    """Return English content when available without changing Persian source fields."""

    def localized(self, field_name):
        if get_language() == "en":
            english_value = getattr(self, f"{field_name}_en", None)
            if english_value:
                return english_value
        return getattr(self, field_name)


class ProductType(LocalizedFieldsMixin, models.Model):
    title = models.CharField(max_length=120, unique=True)
    title_en = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(max_length=140, unique=True, allow_unicode=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "title"]

    def __str__(self):
        return self.title

    @property
    def display_title(self):
        return self.localized("title")


class Product(LocalizedFieldsMixin, models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=180, db_index=True)
    title_en = models.CharField(max_length=180, blank=True, db_index=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        allow_unicode=True,
        blank=True,
    )
    subtitle = models.CharField(max_length=240)
    subtitle_en = models.CharField(max_length=240, blank=True)
    short_description = models.TextField()
    short_description_en = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True)
    detailed_description_en = models.TextField(blank=True)
    main_image = models.ImageField(upload_to="products/main/", blank=True, max_length=500)
    header_image = models.ImageField(upload_to="products/headers/", blank=True, max_length=500)
    price = models.DecimalField(max_digits=14, decimal_places=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    similar_products = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="similar_to_products",
        blank=True,
        help_text="حداکثر سه محصول را انتخاب کنید.",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "-created_at"]),
            models.Index(fields=["is_active", "price"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:product-detail", kwargs={"slug": self.slug})

    @property
    def display_title(self):
        return self.localized("title")

    @property
    def display_subtitle(self):
        return self.localized("subtitle")

    @property
    def display_short_description(self):
        return self.localized("short_description")

    @property
    def display_detailed_description(self):
        return self.localized("detailed_description")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = (
                slugify(self.title_en)
                or slugify(self.title, allow_unicode=True)
                or "product"
            )
            candidate = base_slug
            suffix = 2
            while Product.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class OrderedProductItem(LocalizedFieldsMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    title_en = models.CharField(max_length=120, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["position", "id"]

    def __str__(self):
        return self.title

    @property
    def display_title(self):
        return self.localized("title")


class ProductCapacity(OrderedProductItem):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="capacities",
    )


class ProductSize(OrderedProductItem):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sizes",
    )


class ProductFeature(OrderedProductItem):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="features",
    )


class ProductGalleryImage(LocalizedFieldsMixin, models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(upload_to="products/gallery/", max_length=500)
    alt_text = models.CharField(max_length=180, blank=True)
    alt_text_en = models.CharField(max_length=180, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return self.alt_text or f"{self.product.title} - {self.pk}"

    @property
    def display_alt_text(self):
        return self.localized("alt_text") or self.product.display_title


class Project(LocalizedFieldsMixin, models.Model):
    title = models.CharField(max_length=180, db_index=True)
    title_en = models.CharField(max_length=180, blank=True, db_index=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        allow_unicode=True,
        blank=True,
    )
    subtitle = models.CharField(max_length=240, blank=True)
    subtitle_en = models.CharField(max_length=240, blank=True)
    description = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    location = models.CharField(max_length=180, blank=True, db_index=True)
    location_en = models.CharField(max_length=180, blank=True, db_index=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    main_image = models.ImageField(upload_to="projects/main/", blank=True, max_length=500)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_active", "-created_at"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:project-detail", kwargs={"slug": self.slug})

    @property
    def display_title(self):
        return self.localized("title")

    @property
    def display_subtitle(self):
        return self.localized("subtitle")

    @property
    def display_description(self):
        return self.localized("description")

    @property
    def display_location(self):
        return self.localized("location")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = (
                slugify(self.title_en)
                or slugify(self.title, allow_unicode=True)
                or "project"
            )
            candidate = base_slug
            suffix = 2
            while Project.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class OrderedProjectItem(LocalizedFieldsMixin, models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    title_en = models.CharField(max_length=140, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["position", "id"]

    def __str__(self):
        return self.title

    @property
    def display_title(self):
        return self.localized("title")


class ProjectFeature(OrderedProjectItem):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="features",
    )


class ProjectGalleryImage(LocalizedFieldsMixin, models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(upload_to="projects/gallery/", max_length=500)
    alt_text = models.CharField(max_length=180, blank=True)
    alt_text_en = models.CharField(max_length=180, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return self.alt_text or f"{self.project.title} - {self.pk}"

    @property
    def display_alt_text(self):
        return self.localized("alt_text") or self.project.display_title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(
        max_length=30,
        validators=[PHONE_VALIDATOR],
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_read", "-created_at"])]

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Representative(LocalizedFieldsMixin, models.Model):
    name = models.CharField(max_length=140)
    name_en = models.CharField(max_length=140, blank=True)
    city = models.CharField(max_length=100, db_index=True)
    city_en = models.CharField(max_length=100, blank=True, db_index=True)
    phone = models.CharField(
        max_length=30,
        validators=[PHONE_VALIDATOR],
    )
    address = models.TextField()
    address_en = models.TextField(blank=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["city", "name"]
        indexes = [models.Index(fields=["is_active", "city"])]

    def __str__(self):
        return f"{self.city} - {self.name}"

    @property
    def display_name(self):
        return self.localized("name")

    @property
    def display_city(self):
        return self.localized("city")

    @property
    def display_address(self):
        return self.localized("address")


class Service(LocalizedFieldsMixin, models.Model):
    title = models.CharField(max_length=180, unique=True)
    title_en = models.CharField(max_length=180, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    subtitle = models.CharField(max_length=240)
    subtitle_en = models.CharField(max_length=240, blank=True)
    short_description = models.TextField()
    short_description_en = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True)
    detailed_description_en = models.TextField(blank=True)
    main_image = models.ImageField(upload_to="services/main/", blank=True, max_length=500)
    header_image = models.ImageField(upload_to="services/headers/", blank=True, max_length=500)
    position = models.PositiveSmallIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "title"]
        indexes = [models.Index(fields=["is_active", "position"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:service-detail", kwargs={"slug": self.slug})

    @property
    def display_title(self):
        return self.localized("title")

    @property
    def display_subtitle(self):
        return self.localized("subtitle")

    @property
    def display_short_description(self):
        return self.localized("short_description")

    @property
    def display_detailed_description(self):
        return self.localized("detailed_description")

    @property
    def fallback_image_name(self):
        fallback_images = (
            "home-service1.jpg",
            "home-service2.jpg",
            "home-service3.jpg",
        )
        return fallback_images[self.position % len(fallback_images)]


class ServiceItem(LocalizedFieldsMixin, models.Model):
    class Kind(models.TextChoices):
        BENEFIT = "benefit", "مزیت و قابلیت"
        PROCESS = "process", "مرحله اجرا"

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="items",
    )
    kind = models.CharField(max_length=20, choices=Kind.choices)
    title = models.CharField(max_length=160)
    title_en = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["kind", "position", "id"]
        indexes = [models.Index(fields=["service", "kind", "position"])]

    def __str__(self):
        return self.title

    @property
    def display_title(self):
        return self.localized("title")

    @property
    def display_description(self):
        return self.localized("description")


class ServiceGalleryImage(LocalizedFieldsMixin, models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(upload_to="services/gallery/", max_length=500)
    alt_text = models.CharField(max_length=180, blank=True)
    alt_text_en = models.CharField(max_length=180, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return self.alt_text or f"{self.service.title} - {self.pk}"

    @property
    def display_alt_text(self):
        return self.localized("alt_text") or self.service.display_title


class HiringRequest(models.Model):
    full_name = models.CharField(max_length=140)
    phone = models.CharField(max_length=30, validators=[PHONE_VALIDATOR])
    email = models.EmailField()
    desired_position = models.CharField(max_length=160)
    experience_years = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(60)],
    )
    message = models.TextField()
    resume = models.FileField(
        upload_to="hiring/resumes/%Y/%m/",
        blank=True,
        max_length=500,
        validators=[
            FileExtensionValidator(allowed_extensions=("pdf", "doc", "docx")),
            validate_resume_size,
        ],
    )
    is_reviewed = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_reviewed", "-created_at"])]

    def __str__(self):
        return f"{self.full_name} - {self.desired_position}"


class BlogPost(LocalizedFieldsMixin, models.Model):
    title = models.CharField(max_length=220, db_index=True)
    title_en = models.CharField(max_length=220, blank=True, db_index=True)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    excerpt = models.TextField(max_length=500)
    excerpt_en = models.TextField(max_length=500, blank=True)
    body = CKEditor5Field(config_name="blog")
    body_en = CKEditor5Field(config_name="blog", blank=True)
    cover_image = models.ImageField(upload_to="blog/covers/", blank=True, max_length=500)
    author_name = models.CharField(
        max_length=160,
        default="تیم تحقیق و توسعه شرکت وزنه",
    )
    author_name_en = models.CharField(max_length=160, blank=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    related_posts = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="related_to_posts",
        blank=True,
        help_text="حداکثر سه مطلب مرتبط را انتخاب کنید.",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["is_published", "-published_at"]),
            models.Index(fields=["is_featured", "-published_at"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:blog-detail", kwargs={"slug": self.slug})

    @property
    def display_title(self):
        return self.localized("title")

    @property
    def display_excerpt(self):
        return self.localized("excerpt")

    @property
    def display_body(self):
        return self.localized("body")

    @property
    def display_author_name(self):
        return self.localized("author_name")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "article"
            candidate = base_slug
            suffix = 2
            while BlogPost.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    @property
    def fallback_image_name(self):
        fallback_images = (
            "home-service3.jpg",
            "home-service2.jpg",
            "project-image.png",
        )
        position = max((self.pk or 1) - 1, 0)
        return fallback_images[position % len(fallback_images)]


@receiver(m2m_changed, sender=Product.similar_products.through)
def limit_similar_products(sender, instance, action, pk_set, **kwargs):
    if action != "pre_add":
        return

    if instance.pk in pk_set:
        raise ValidationError("A product cannot be similar to itself.")

    current_count = instance.similar_products.count()
    new_count = len(pk_set - set(instance.similar_products.values_list("pk", flat=True)))
    if current_count + new_count > 3:
        raise ValidationError("A product can have at most three similar products.")


@receiver(m2m_changed, sender=BlogPost.related_posts.through)
def limit_related_blog_posts(sender, instance, action, pk_set, **kwargs):
    if action != "pre_add":
        return

    if instance.pk in pk_set:
        raise ValidationError("A blog post cannot be related to itself.")

    existing_ids = set(instance.related_posts.values_list("pk", flat=True))
    if len(existing_ids) + len(pk_set - existing_ids) > 3:
        raise ValidationError("A blog post can have at most three related posts.")
