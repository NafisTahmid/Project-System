from django.urls import path
from base.views import comments_views as views
urlpatterns = [
    path('<str:pk>/', views.getComment, name="comment"),
    path('<str:pk>/update/', views.updateComment, name="update_comment"),
    path('<str:pk>/delete/', views.deleteComment, name="delete_comment")
]