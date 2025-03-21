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
from Aptitest import views as ex,Coding_test as cod,sqlviews as sql,pythonrun as ex_py
from Aptitest import views as ex,HTML_CSS_views as html_css,js_views as js
from Aptitest import MCQ_views  as mcq ,Traainer_views as trainer
urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', ex.home),
    path('add/users/', ex.AddUsers),
    path('login/', ex.login),
    # path('get/questions/', ex.get_questions),
    # path('questions/submit/',ex.submit_answer),
    # path('test/submit/',ex.logout),
    # path('test/report/',ex.report),
    path('add/coding/',cod.add_coding_test_questions),
    path('get/coding/',cod.get_Questions),
    path ('runsql/',sql.sql_query ),
    path ('submit/',cod.submit ),
    path ('html/',html_css.html_page ),
    path ('css/',html_css.css_compare ),
    path ('js/',js.js_Score ),
    path ('runpy/',ex_py.run_python ),
    # path('duration/',cod.Coding_duration),
    path('code/backup/',cod.code_backup),
    path('stat/',cod.submitedStatus),
    # path('update/',cod.update_jason),
    # path('update/mcq/',ex.updateJson),

    # MCQ API
     path('loginmcq/', mcq.login),
     path('get/questions/', mcq.get_questions),
     path('questions/submit/',mcq.submit_answer),
     path('test/submit/',mcq.logout),
     path('test/report/',mcq.report),
     path('update/mcq/',mcq.updateJson),

     # both
     path('duration/',ex.Test_duration),

     # Traier API 
     path('logintrainer/', trainer.Trainer_login),
     path('addtrainer/', trainer.AddTrainer),
     path ('delete/users/', trainer.Delete_users),
     path('fetch/users/', trainer.get_all_students),
]
