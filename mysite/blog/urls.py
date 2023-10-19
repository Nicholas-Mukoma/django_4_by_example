from django.urls import path
from   . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('',views.post_list, name= 'post_list'),# mapps to the post list view
    path('tag/<slug:tag_slug>/', views.post_list, name = 'post_list_by_tag'),
    #path('', views.PostListView.as_view(), name= 'post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,name = 'post_detail'), # mapps to the post_detail view
    path('<int:post_id>/share/', views.post_share, name = 'post_share' ),
    path('<int:post_id>/comment/',views.post_comment, name = 'post_comment'),
    path('upload/', views.upload_post, name = 'upload_post'),
    path('login/', views.login_user, name = 'login')
]