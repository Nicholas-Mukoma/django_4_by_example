from django.urls import path
from   . import views
from django.urls import path, include
from django.contrib import admin

app_name = 'blog'

urlpatterns = [
    path('',views.post_list, name= 'post_list'),# mapps to the post list view
    path('<int:id>/', views.post_detail,name = 'post_detail'), # mapps to the post_detail view
]

