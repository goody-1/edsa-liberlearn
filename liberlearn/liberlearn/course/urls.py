from django.urls import path

from . import views

urlpatterns = [
    path(
        "mine/",
        views.ManageCourseListView.as_view(),
        name="manage_course_list",
    ),
    path("create/", views.CourseCreateView.as_view(), name="course_create"),
    path("<pk>/edit/", views.CourseUpdateView.as_view(), name="course_edit"),
    path(
        "<pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"
    ),
    path(
        "<pk>/lesson/",
        views.CourseLessonUpdateView.as_view(),
        name="course_lesson_update",
    ),
    path(
        "lesson/<int:lesson_id>/content/<model_name>/create/",
        views.ContentCreateUpdateView.as_view(),
        name="lesson_content_create",
    ),
    path(
        "lesson/<int:lesson_id>/content/<model_name>/<id>/",
        views.ContentCreateUpdateView.as_view(),
        name="lesson_content_update",
    ),
    path(
        "content/<int:id>/delete/",
        views.ContentDeleteView.as_view(),
        name="lesson_content_delete",
    ),
    path(
        "lesson/<int:lesson_id>/",
        views.LessonContentListView.as_view(),
        name="lesson_content_list",
    ),
    path(
        "lesson/order/", views.LessonOrderView.as_view(), name="lesson_order"
    ),
    path(
        "content/order/",
        views.ContentOrderView.as_view(),
        name="content_order",
    ),
    path(
        "subject/<slug:subject>/",
        views.CourseListView.as_view(),
        name="course_list_subject",
    ),
    path(
        "<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"
    ),
]
