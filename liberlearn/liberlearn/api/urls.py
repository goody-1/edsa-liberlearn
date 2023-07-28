from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"subject", views.SubjectView)
# router.register(r"course", views.CourseView)
router.register("courses", views.CourseView)

urlpatterns = [
    path("", include(router.urls)),
]
