from django.conf.urls import patterns, include, url
from pta import views
from django.contrib import admin
from django.conf.urls.static import static
from ptaAPP import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pta/', include('pta.urls')),
    url(r'^', include('pta.urls')),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, }),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
