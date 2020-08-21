from django.contrib import admin

# Register your models here.
from backend.forms import BusinessForm, CategoryForm, TagForm
from backend.models import Category, Business, Tag, OpeningHours, Address


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    form = CategoryForm
    list_display = ("name",)


class OpeningHoursInline(admin.StackedInline):
    model = OpeningHours
    extra = 0
    exclude = ("created_at", "updated_at", "deleted_at",)
    ordering = ("day",)


class AddressInline(admin.StackedInline):
    model = Address
    exclude = ("created_at", "updated_at", "deleted_at",)


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    model = Business
    form = BusinessForm
    list_display = ("name", "category", "accepted_at")
    inlines = [OpeningHoursInline, AddressInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    form = TagForm
    list_display = ("name",)
