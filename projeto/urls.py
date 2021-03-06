"""projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from projeto.edp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projeto.accounts.urls', namespace='accounts')),
    path('edps/', include('projeto.edp.urls', namespace='edp')),
    path('forum/', include('projeto.boards.urls', namespace='boards')),
    path('accounts/', include('django.contrib.auth.urls')),



]
urlpatterns += staticfiles_urlpatterns()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += [

    path('tinymce/', include('tinymce.urls')),
]
