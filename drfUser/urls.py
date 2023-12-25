from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from drfUser import views

urlpatterns = [
    # user增删改查查，使用两个CBV
    path('user/', views.UserView.as_view()),
    path('user/<int:pk>/', views.UserViewDetails.as_view()),
    # group增删改查查，使用一个CBV,利用了**kwargs传参
    path('group/', views.GroupView.as_view(), kwargs={'pk': None}),
    path('group/<int:pk>/', views.GroupView.as_view()),
    path('tasks/',views.CreateTaskView.as_view())

]
urlpatterns = format_suffix_patterns(urlpatterns)
