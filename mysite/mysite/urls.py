"""mysite URL Configuration

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
"""
from django.conf.urls import url
from django.contrib import admin
from ABET_DB import views
from django.conf.urls.static import static
from django.conf import settings

from ABET_DB.views import CreateContactView, AboutView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^show_data/', views.showData),
    url(r'^show_data_template/', views.showDataTemplate),
    url(r'^validation_test/', CreateContactView.as_view()),
    url(r'^about/', AboutView.as_view()),
    url(r'^/', views.index),
] + static(settings.STATIC_URL,docuemnt_root=settings.STATIC_ROOT)
