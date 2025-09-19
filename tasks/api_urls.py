from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import api_views

app_name = "tasks_api"

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', api_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', api_views.UserRegistrationView.as_view(), name='register'),
    path('auth/logout/', api_views.logout_view, name='logout'),
    
    # User endpoints
    path('user/profile/', api_views.UserProfileView.as_view(), name='user_profile'),
    
    # Task endpoints
    path('tasks/', api_views.TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>/', api_views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/toggle/', api_views.TaskToggleView.as_view(), name='task_toggle'),
    path('tasks/stats/', api_views.task_stats, name='task_stats'),
]
