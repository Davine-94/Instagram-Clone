from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_images, name='search'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('upload/add/', views.save_image, name='save_image'),
    path('picture/<int:id>/', views.image_comments, name='single_image'),
    path('user/<int:id>/', views.user_profile, name='user_profile'),
    path('like/<int:id>/', views.like_image, name='like_image'),
    path('comment/add', views.save_comment, name='add_comment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
