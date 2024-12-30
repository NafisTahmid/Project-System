from django.urls import path
from base.views import tasks_views as views
urlpatterns = [
    path('<str:pk>/', views.getTask, name="task"),
    path('<str:pk>/update/', views.updateTask, name="update_task"),
    path('<str:pk>/delete/', views.deleteTask, name="delete_task"),
    path('<str:pk>/comments/', views.getComments, name='comments'),
    path('<str:pk>/comments/create/', views.createComment, name="create-comment")
]