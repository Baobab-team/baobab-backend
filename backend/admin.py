from django.contrib import admin

# Register your models here.
from modeltranslation.admin import TranslationAdmin

from backend.forms import BusinessForm, CategoryForm, TagForm, PaymentTypeForm
from backend.models import (
    Category,
    Business,
    Tag,
    OpeningHour,
    Address,
    Phone,
    SocialLink,
    PaymentType,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    form = CategoryForm
    list_display = ("id", "slug", "name", "parent")
    readonly_fields = ("slug",)
    actions = ["slugify"]

    def slugify(self, request, queryset):
        for c in queryset:
            c.save()

    slugify.short_description = "Slugify"


class OpeningHourInline(admin.StackedInline):
    model = OpeningHour
    extra = 0
    exclude = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    ordering = ("day",)


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0
    exclude = (
        "created_at",
        "updated_at",
        "deleted_at",
    )


class TagInline(admin.TabularInline):
    model = Business.tags.through
    extra = 0
    exclude = (
        "created_at",
        "updated_at",
        "deleted_at",
    )


class PaymentTypeInline(admin.TabularInline):
    model = Business.payment_types.through
    extra = 0
    exclude = (
        "created_at",
        "updated_at",
        "deleted_at",
    )


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    exclude = (
        "created_at",
        "updated_at",
        "deleted_at",
    )


class SocialLinkInline(admin.StackedInline):
    model = SocialLink
    extra = 0
    exclude = (
        "created_at",
        "updated_at",
        "deleted_at",
    )


@admin.register(Business)
class BusinessAdmin(TranslationAdmin):
    model = Business
    form = BusinessForm
    list_display = (
        "id",
        "name",
        "slug",
        "category",
        "accepted_at",
        "created_at",
        "status",
        "website",
        "last_updated_by",
    )
    readonly_fields = (
        "slug",
        "deleted_at",
        "created_at",
        "accepted_at",
        "last_updated_by",
    )
    inlines = [
        PhoneInline,
        PaymentTypeInline,
        TagInline,
        SocialLinkInline,
        OpeningHourInline,
        AddressInline,
    ]
    actions = ["slugify"]

    def slugify(self, request, queryset):
        for b in queryset:
            b.save()

    slugify.short_description = "Slugify"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    form = TagForm
    list_display = ("name",)


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    model = PaymentType
    form = PaymentTypeForm
    list_display = ("name",)
