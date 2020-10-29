from django.forms import ModelForm

from users.models import CustomUser
from .models import Category, Business, Tag, PaymentType


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ["updated_at", "created_at", "deleted_at"]


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        exclude = [
            "updated_at",
            "created_at",
            "deleted_at",
            "last_updated_by",
            "tags",
            "payment_types",
        ]

    def clean_last_updated_by(self):
        if not self.cleaned_data["last_updated_by"]:
            return CustomUser()
        return self.cleaned_data["last_updated_by"]


class TagForm(ModelForm):
    class Meta:
        model = Tag
        exclude = ["updated_at", "created_at", "deleted_at"]


class PaymentTypeForm(ModelForm):
    class Meta:
        model = PaymentType
        exclude = ["updated_at", "created_at", "deleted_at"]
