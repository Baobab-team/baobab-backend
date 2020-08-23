from django.forms import ModelForm

from .models import Category, Business, Tag


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['updated_at', 'created_at', 'deleted_at']


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        exclude = ['updated_at', 'created_at', 'deleted_at','accepted_at']


class TagForm(ModelForm):
    class Meta:
        model = Tag
        exclude = ['updated_at', 'created_at', 'deleted_at']