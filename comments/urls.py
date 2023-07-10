from django.urls import path
from comments import views

urlpatterns = [
    path('comments/', views.CommentList.as_view()),
    path('comment/<int:pk>', views.CommentDetails.as_view()),
]