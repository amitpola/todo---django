from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage

urlpatterns = [    
    path('',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task-detail'),
    path('create-task/',TaskCreate.as_view(),name='create-task'),
    path('update-task/<int:pk>/',TaskUpdate.as_view(),name='update-task'),
    path('delete-task/<int:pk>/',TaskDelete.as_view(),name='delete-task'),

    path('login/',CustomLoginView.as_view(),name='login'),
    path('register/',RegisterPage.as_view(),name='register'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    #path('get-logged-tasks/',queryTasks,name='get-logged-tasks')
]