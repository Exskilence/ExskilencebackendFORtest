"""ExskilenceTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from Aptitest import views as ex
urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', ex.home),
    path('add/users/', ex.AddUsers),
    path('login/', ex.login),
    path('get/questions/', ex.get_questions),
    path('questions/submit/',ex.submit_answer),
    path('test/submit/',ex.logout),
    path('test/report/',ex.report)
]
