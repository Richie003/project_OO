from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Product, Review, CheckOut
from django.dispatch import receiver


class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = Product
        fields = (
            "pr_name",
            "description",
            "price",
            "category",
            "size",
            "image",
            "stock",
        )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            "body",
        )


class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = (
            'firstname',
            'lastname',
            'address2',
            'address',
            'gateway',
            'country',
            'email'
        )