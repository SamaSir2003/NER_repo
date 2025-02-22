"""
URL configuration for tagproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tags import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('admin/', admin.site.urls),
    path('get_paragraph/', views.get_paragraph, name='get_paragraph'),
    path('submit_file/', views.submit_file, name='submit_file'),
     path('reset_picked_files/', views.reset_picked_files, name='reset_picked_files'),
     path('clear_tags/', views.clear_tags, name='clear_tags'),
     path('accounts/', include('django.contrib.auth.urls')),
]
