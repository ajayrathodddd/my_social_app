from django.urls import path
from .views import (
    home_view, register_view, login_view, logout_view,
    get_posts_api, create_post_api, like_post_api,
    profile_view # <-- Add import
)

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'), # <-- New Profile Route
    path('api/posts/', get_posts_api, name='get_posts_api'),
    path('api/posts/create/', create_post_api, name='create_post_api'),
    path('api/posts/<int:post_id>/like/', like_post_api, name='like_post_api'),
]