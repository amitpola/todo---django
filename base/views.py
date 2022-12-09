from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

#login view class based
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

#register user view
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    #restricting logged in user to see signup pages
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        
        return super(RegisterPage,self).get(*args,**kwargs)

#function based authentication
# def userLogin(request):
    #print(request.POST)
    # print(request.method)

    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']

    #     user = authenticate(request,username=username,password=password)
    #     print(user)
    #     if user is not None:
    #         login(request,user)
    #         print('success')
    #         return redirect('tasks')
    #     else:
    #         messages.error(request,'Invalid credentials')

    # return render(request,'base/login_register.html')

# ListView by default gives a queryset from table in name of object_list, we can customize it
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/tasks.html'

    #method to get context of logged in user
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area')
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            
        if search_input is not None:
            context['search_input'] = search_input 
        else:
            context['search_input'] = ''
        return context


#detail view provides details about any item
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

#A view that displays a form for creating an object, redisplaying the form with validation errors (if there are any) and saving the object.
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

# view that displays a form for editing an existing object

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    template_name = 'base/task_update.html'
    success_url = reverse_lazy('tasks')


#A view that displays a confirmation page and deletes an existing object
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'base/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


#query only logged in user tasks using function based views
# def queryTasks(request):
#     user = request.user
#     listItems = Task.objects.filter(user = user)

#     context = {'listItems':listItems}
#     return render(request,'base/tasks.html',context)
