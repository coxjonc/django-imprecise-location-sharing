from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	url(r'^$', views.redirect, name='redirect'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^update_location/$', views.update_location, name="update_location"),
    url(r'^send_request/$', views.send_request, name='send_request'),
    url(r'^accept_friend/$', views.accept_friend, name='accept_friend'),
    url(r'^unfriend/$', views.unfriend, name='unfriend'),
	url(r'^about/$', TemplateView.as_view(template_name="neversets/about.html")),
	url(r'^contact/$', TemplateView.as_view(template_name="neversets/contact.html")),
	url(r'^donate/$', TemplateView.as_view(template_name="neversets/donate.html")),
	url(r'^coming_soon/$', TemplateView.as_view(template_name="neversets/coming_soon.html"))
]
