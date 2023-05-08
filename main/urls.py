from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    path('user_page', views.user_page, name='users_page'),
    path('profile/<str:username>/', views.PostsListView.as_view(), name='user_posts'),
    path('new_post', views.new_post, name='new_post'),
    path('create_us', views.create_us, name='create_us'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('log_out', views.log_out, name='log_out'),
    path('settings', views.edit_profile, name='settings'),
    path('search', views.search, name='search'),
    path('<int:pk>/update', views.PostsUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', views.PostsDeleteView.as_view(), name='post_delete'),

]
