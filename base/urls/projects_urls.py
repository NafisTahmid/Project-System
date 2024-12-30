from django.urls import path
from base.views import projects_views as views
urlpatterns = [
    path('', views.listProjects, name="list-projects"),
    path('<str:pk>/', views.getProject, name="get-project"),
    path('update/<str:pk>/', views.updateProject, name="update-project"),
    path('delete/<str:pk>/', views.deleteProject, name="delete-project"),
    path('create-project/', views.createProject, name='create-project'),
    path('<str:pk>/tasks/', views.listTasks,  name="tasks"),
    path('<str:pk>/create-task/', views.createTask, name="create-task")
]