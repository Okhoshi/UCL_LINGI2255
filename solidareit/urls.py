from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('website.views',
    url(r'^$', 'home', name='home'),
    url(r'^login/$', 'login', name='login'),
    url(r'^register/$', 'register', name='register'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^account/$', 'account', name='account'),
    url(r'^create/$', 'create_offer_demand', name='create_offer_demand'),
    url(r'^account/add_representative/$', 'add_representative', name='add_representative'),
    url(r'^account/add_pins/$', 'add_pins', name='add_pins'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^concept/$', 'concept', name="concept"),
    url(r'^faq/$', 'faq', name="faq"),
    url(r'^contact/$', 'contact', name="contact"),
    url(r'^messages/$', 'messages', name="messages"),
    url(r'^search/$', 'search', name="search"),
    url(r'^exchanges/$', 'exchanges', name="exchanges"),
    url(r'^news/$', 'news', name="news"),
    url(r'^edit_profile/$', 'edit_profile', name="edit_profile"),
    # Examples:
    # url(r'^$', 'solidareit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
