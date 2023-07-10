from django.urls import path
from followers import views

urlpatterns = [
    path('followers/', views.FollowerList.as_view()),
    path('follower/<int:pk>/', views.FollowerDetial.as_view()),
]