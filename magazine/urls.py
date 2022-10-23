from django.urls import path
from magazine import views

urlpatterns = [
    path('', views.home, name='home'),
    path('converter/', views.exchange, name='converter'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('update/<int:pk>', views.PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.PostDeleteView.as_view(), name='delete'),
    path('profile/<user_name>', views.profile, name='profile'),
    path('posts/', views.PostShowView.as_view(), name='show_posts'),
    path('getpost/<int:post_id>', views.post, name='get_post'),

    path('profilecreate/', views.ProfileCreateView.as_view(), name='profile_create'),
]