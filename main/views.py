from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.models import ModelForm
from django.contrib.auth import login, logout
from main.models import Course, Subscription


class CourseListView(ListView):
    model = Course
    paginate_by = 10
    context_object_name = 'course_list'
    template_name = 'course_list.html'


class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'course.html'

    def post(self, request, **kwargs):
        if len(Subscription._default_manager.filter(
                Course_id=kwargs.get('pk'),
                User_id=request.user.id)
            ) == 0:
                new_sub = Subscription(Course=self.get_object(), User=request.user)
                new_sub.save()
        return super().get(request)


class SubscriptionListView(ListView):
    model = Subscription
    context_object_name = 'subscription_list'
    template_name = 'subscription_list.html'

    def get_queryset(self):
        return self.model._default_manager.filter(Course_id=self.kwargs.get('Course_id'))[:10]

    def get(self, request, **kwargs):
        return super().get(request)


class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ['id']


class CourseCreate(CreateView):
    form_class = CourseForm
    template_name = 'course_create.html'

    def post(self, request):
        print(request.FILES)
        return super().post(request)

    def get(self, request):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().get(request)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = '/login'
    template_name = 'registration.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutFormView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
