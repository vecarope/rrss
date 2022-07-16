from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
	path('', views.home,  name='home'),
	path('registro', views.registro, name='registro'),
	path('home/login/',auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('home/logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('eliminar/<int:post_id>/', views.eliminar, name='eliminar'),
	path('perfil/<str:username>/', views.perfil, name='perfil'),
	path('editar/', views.editar, name='editar'),
	path('seguir/<str:username>/', views.seguir, name='seguir'),
	path('dejarseguir/<str:username>/', views.dejarSeguir, name='dejarseguir'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)