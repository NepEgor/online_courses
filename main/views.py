from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from main.models import Course


class CourseListView(ListView):
    model = Course
    paginate_by = 2
    context_object_name = 'course_list'
    template_name = 'course_list.html'

'''
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if(self.request.user.is_authenticated):
            context['user_atribs'] = '<span class="link_btn">' + self.request.user.username + '</span>' \
                                     '<a href="/logout" class="link_btn">logout</a>'
        else:
            context['user_atribs'] = '<a href="/login" class="link_btn">login</a>' \
                                     '<a href="/registration" class="link_btn">register</a>'
        return context
'''

class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'course.html'

    def get_object(self):
        object = super(CourseDetailView, self).get_object()
        return object


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
