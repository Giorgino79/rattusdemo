"""
URL configuration for amm project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dipendenti import views as dipendenti_views

urlpatterns = [
    path("select2/", include("django_select2.urls")),
    path("admin/", admin.site.urls),
    path('', dipendenti_views.entra, name='login'),
    path('',include('dipendenti.urls')),
    path('home',include('home.urls')),
    path('anagrafica/',include('anagrafica.urls')),
    path('automezzi/',include('automezzi.urls')),
    path('contratti/',include('contratti.urls')),
    path('servizi/',include('servizi.urls')),
    path('contabilità/',include('contabilità.urls')),
    path('logistica/',include('logistica.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
