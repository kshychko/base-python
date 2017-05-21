from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.http import HttpResponse


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include('app_dir.permit.urls')),

    url(r'healthcheck', lambda r: HttpResponse()),

    url(r'^', TemplateView.as_view(template_name='home.html'), name='home'),
]
