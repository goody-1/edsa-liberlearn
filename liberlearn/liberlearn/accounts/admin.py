from django.contrib import admin

from .models import Facility, Mentor, Student, User

admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Facility)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "username",
        "date_joined",
        "role",
    ]
    list_filter = [
        "date_joined",
        "is_staff",
        "role",
    ]
    search_fields = ["email", "username"]
    fieldsets = (
        (None, {"fields": ("username", "email")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("User Role", {"fields": ("role",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # prepopulated_fields = {"slug": ("title",)}
    def save_model(self, request, obj, form, change):
        """
        Custom save_model method to handle password setting for superuser.
        """
        if not obj.id and not obj.password:
            # If it's a new user and password is not set, set it for superuser.
            obj.set_password("test123")
        super().save_model(request, obj, form, change)
