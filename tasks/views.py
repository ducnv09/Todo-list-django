from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, RedirectView, FormView
from .models import Task
from .forms import TaskForm

class SignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks:list")
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Tạo tài khoản thành công!")
        return super().form_valid(form)

class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

class OwnerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

class TaskListView(OwnerQuerysetMixin, ListView):
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10
    # Tìm kiếm & lọc (tuỳ chọn—đã kèm luôn):
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()  # "", "open", "done"
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(note__icontains=q))
        if status == "open":
            qs = qs.filter(is_done=False)
        elif status == "done":
            qs = qs.filter(is_done=True)
        return qs

class TaskCreateView(OwnerQuerysetMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:list")
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Đã tạo công việc.")
        return super().form_valid(form)

class TaskUpdateView(OwnerQuerysetMixin, OwnerOnlyMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:list")
    def form_valid(self, form):
        messages.success(self.request, "Đã cập nhật.")
        return super().form_valid(form)

class TaskDeleteView(OwnerQuerysetMixin, OwnerOnlyMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:list")
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Đã xoá.")
        return super().delete(request, *args, **kwargs)

class TaskToggleDoneView(OwnerQuerysetMixin, OwnerOnlyMixin, RedirectView):
    pattern_name = "tasks:list"

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs["pk"], owner=self.request.user)

    def get_redirect_url(self, *args, **kwargs):
        task = self.get_object()
        task.is_done = not task.is_done
        task.save(update_fields=["is_done"])
        messages.success(self.request, "Đã cập nhật trạng thái.")
        kwargs.pop("pk", None)            # <— loại bỏ 'pk'
        return super().get_redirect_url(*args, **kwargs)
