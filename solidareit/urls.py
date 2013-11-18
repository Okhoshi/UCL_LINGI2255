from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('website.views',
    url(r'^$', 'home'),
    url(r'^login/$', 'login', name='login'),
    url(r'^register/$', 'register', name='register'),
    url(r'^register/individual/$', 'individual_registration'),
    url(r'^register/organisation/$', 'organisation_registration'),
    url(r'^profile/$', 'profile', name='profile'),
    # Examples:
    # url(r'^$', 'solidareit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()