'''mysite URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
'''
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


from ABET_DB import views


urlpatterns = [
    url(r'dat/(\w+)',views.listJSON),
    url(r'form/(\w+)',views.form),
    url(r'submit/(\w+)',views.submit),
    url(r'logout',views.logout),
    url(r'populate/', views.populate),
    url(r'populatePis',views.prevPis),
    url(r'clearDB/', views.clearDB),
    url(r'^admin/', admin.site.urls),
    url(r'^graph/', views.graph),
    url(r'^matrix/', views.matrix),
    url(r'^prof/', views.professorPage),
    url(r'^$',views.login),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
