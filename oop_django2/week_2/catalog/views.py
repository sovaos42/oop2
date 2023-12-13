from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegistrationForm, ApplicationForm, ApplicationCommentForm, ApplicationDesignForm, CategoryForm
from django.views import generic
from .models import Application, AdvUser, Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import ApplicationFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.
def home(request):
    num_applications_in_progress = Application.objects.all().filter(status='Принято в работу').count()
    applications_done = Application.objects.filter(status='Выполнено')

    return render(request, 'home.html', context={'num_applications_in_progress': num_applications_in_progress,
                                                  'applications_done': applications_done})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'catalog/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'catalog/register.html', {'user_form': user_form})


@login_required()
def profile(request):
    return render(request, 'catalog/profile.html')


class ApplicationList(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'catalog/application_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ApplicationFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        return Application.objects.filter(client=self.request.user.id)


class ApplicationListAdmin(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'catalog/application_list_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ApplicationFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ApplicationCreate(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'application_form.html'
    success_url = reverse_lazy('application')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.client = self.request.user
        fields.save()
        return super().form_valid(form)


class ApplicationDelete(DeleteView):
    model = Application
    success_url = reverse_lazy('application')


def confirm_update(request, pk, st):
    newApplication = Application.objects.get(id=pk)
    newApplication.save()

    if st == 'Выполнено':
        if request.method == 'POST':
            form = ApplicationDesignForm(request.POST, request.FILES)
            if form.is_valid():
                newApplication.design = form.cleaned_data['design']
                newApplication.status = st
                newApplication.save()
                return redirect('application-admin')
        else:
            form = ApplicationDesignForm()
        return render(request, 'catalog/update_application.html', {'form': form})

    if st == 'Принято в работу':
        if request.method == 'POST':
            form = ApplicationCommentForm(request.POST, request.FILES)
            if form.is_valid():
                newApplication.comment = form.cleaned_data['comment']
                newApplication.status = st
                newApplication.save()
                return redirect('application-admin')
        else:
            form = ApplicationCommentForm()
        return render(request, 'catalog/update_application.html', {'form': form})


class ViewCategory(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'catalog/categories_list.html'
    context_object_name = 'categories_list'


class CreateCategory(CreateView):
    template_name = 'catalog/category_create.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('view-categories')


class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('view-categories')