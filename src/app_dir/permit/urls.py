from django.contrib.auth.views import logout
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': '/login/'}, name='logout'),

    url(r'^wizard/$', views.ApplicationWizardView.as_view(), name='application-wizard'),

    url(r'^applicant/$', views.ApplicantView.as_view(), name='applicant'),
    url(r'^agent/$', views.AgentView.as_view(), name='agent'),
    url(r'^recipient/$', views.RecipientView.as_view(), name='recipient'),
    url(r'^transport/$', views.TransportView.as_view(), name='transport'),
    url(r'^goods/$', views.GoogdsView.as_view(), name='goods')
]
