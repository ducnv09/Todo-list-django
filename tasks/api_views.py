from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from .models import Task
from .serializers import (
    TaskSerializer, 
    TaskCreateUpdateSerializer, 
    UserSerializer, 
    UserRegistrationSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view với thông tin user"""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = authenticate(
                username=request.data.get('username'),
                password=request.data.get('password')
            )
            if user:
                response.data['user'] = UserSerializer(user).data
        return response


class UserRegistrationView(generics.CreateAPIView):
    """API endpoint cho đăng ký user mới"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Tạo JWT tokens cho user mới
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Đăng ký thành công!'
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """API endpoint cho xem và cập nhật profile user"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class TaskListCreateView(generics.ListCreateAPIView):
    """API endpoint cho danh sách và tạo task"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        
        # Tìm kiếm
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(note__icontains=search)
            )
        
        # Lọc theo trạng thái
        status_filter = self.request.query_params.get('status', None)
        if status_filter == 'done':
            queryset = queryset.filter(is_done=True)
        elif status_filter == 'pending':
            queryset = queryset.filter(is_done=False)
        
        return queryset.order_by('is_done', '-created_at')


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint cho chi tiết, cập nhật và xóa task"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskToggleView(APIView):
    """API endpoint cho toggle trạng thái task"""
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, owner=request.user)
            task.is_done = not task.is_done
            task.save(update_fields=['is_done'])
            
            return Response({
                'task': TaskSerializer(task).data,
                'message': f'Task đã được {"hoàn thành" if task.is_done else "đánh dấu chưa xong"}'
            })
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task không tồn tại'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_stats(request):
    """API endpoint cho thống kê task"""
    user_tasks = Task.objects.filter(owner=request.user)
    
    stats = {
        'total': user_tasks.count(),
        'completed': user_tasks.filter(is_done=True).count(),
        'pending': user_tasks.filter(is_done=False).count(),
    }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """API endpoint cho logout (blacklist refresh token)"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({'message': 'Đăng xuất thành công'})
    except Exception as e:
        return Response(
            {'error': 'Có lỗi xảy ra khi đăng xuất'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
