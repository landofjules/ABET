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
    url(r'^dat/?$',views.listJSON),
    #url(r'^form/pi/(\w+)/(\w+)/(\w+)$',views.piForm),
    #url(r'^form/pi/(\w+)/(\w+)/~$',views.piForm), # use ~ as pi for new form
    #url(r'^form/out/(\w+)/(\w+)$',views.outcomeForm),
    #url(r'^submit/pi$',views.submitPi),
    #url(r'^submit/outcome$',views.submitOut),
    #url(r'populate/', views.populate),
    #url(r'clearDB/', views.clearDB),
    url(r'^admin/', admin.site.urls),
    #url(r'^init/', views.test1),
    url(r'^$', views.professorPage),
] + static(settings.STATIC_URL,docuemnt_root=settings.STATIC_ROOT)
