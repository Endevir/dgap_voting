from django.conf.urls import patterns, include, url, static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from registration.backends.simple.views import RegistrationView

from polls.views import Index

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/profiles"

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^bicycle/', include('cycle_storage.urls', namespace='bicycle')),
    url(r'^servertime/', include('servertime.urls', namespace='servertime')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^faq/', include('faq.urls', namespace='faq')),
    url('', include('social.apps.django_app.urls', namespace='social')),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
