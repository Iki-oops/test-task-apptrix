from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Client


class ClientCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Client
        fields = [
            "email",
            "first_name",
            "last_name",
            "sex",
            "avatar",
            "longitude",
            "latitude",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ClientChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Client
        fields = [
            "email",
            "first_name",
            "last_name",
            "sex",
            "avatar",
            "password",
            "longitude",
            "latitude",
        ]


class ClientAdmin(BaseUserAdmin):
    form = ClientChangeForm
    add_form = ClientCreationForm

    list_display = ["pk", "email", "first_name", "last_name", "sex", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": [
            "first_name", "last_name", "sex", "avatar", "longitude", "latitude"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "sex",
                    "avatar",
                    "password1",
                    "password2",
                    "longitude",
                    "latitude",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(Client, ClientAdmin)
admin.site.unregister(Group)
