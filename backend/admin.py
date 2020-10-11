from django.contrib import admin

# Register your models here.
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
    list_display = ("name",)


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
class BusinessAdmin(admin.ModelAdmin):
    model = Business
    form = BusinessForm
    list_display = (
        "name",
        "category",
        "accepted_at",
        "status",
        "website",
        "last_updated_by",
    )
    readonly_fields = ("deleted_at", "accepted_at", "last_updated_by")
    inlines = [
        PhoneInline,
        SocialLinkInline,
        OpeningHourInline,
        AddressInline,
    ]

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
