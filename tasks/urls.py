from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("", views.TaskListView.as_view(), name="list"),
    path("tasks/new/", views.TaskCreateView.as_view(), name="create"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="delete"),
    path("tasks/<int:pk>/toggle/", views.TaskToggleDoneView.as_view(), name="toggle"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
