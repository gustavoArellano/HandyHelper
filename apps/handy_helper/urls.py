from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^registration_process$", views.registration_process, name="registration_process"),
    url(r"^login$", views.login, name="login"),
    url(r"^logout$", views.logout, name="logout"),
    url(r"^logout_complete$", views.logout_complete, name="logout_complete"),
    url(r"^welcome$", views.welcome, name="welcome"),
    url(r"^edit_job/(?P<id>\w+)$", views.edit_job, name="edit_job"),
    url(r"^update/(?P<id>\w+)$", views.update, name="update"),
    url(r"^create_job$", views.create_job, name="add_job"),
    url(r"^create_job_process$", views.create_job_process, name="create_job_process"),
    url(r"^show_job_info/(?P<id>\w+)$", views.show_job_info, name="show_job_info"),
    url(r"^add_job_to_user/(?P<id>\w+)$", views.add_job_to_user, name="add_job_to_user"),
    url(r"^delete_job/(?P<id>\w+)$", views.delete_job, name="delete_job"),
    
    
]
