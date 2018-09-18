"""agency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import  views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index,name='index'),
    url(r'^caform/$', views.caform,name='caform'),
    url(r'^eventregistration/$', views.eventregistration,name='eventregistration'),
    url(r'^capost/$', views.capost,name='capost'),
    url(r'^eventpost/$', views.eventpost,name='eventpost'),
    url(r'^contact/$', views.contacts,name='contact'),
    url(r'^brochure/$', views.infobro, name='infobro'),
	url(r'^intrigue/$', views.problem_statement, name='problem'),
]
