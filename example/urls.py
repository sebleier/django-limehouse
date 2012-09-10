from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import views


urlpatterns = patterns('',
   url(r'^$', views.homepage, name="homepage"),
   url(r'^blog/', include('blog.urls')),
)



urlpatterns += staticfiles_urlpatterns('/static/')
urlpatterns += static('/jstemplates/', document_root=settings.JSTEMPLATES_ROOT)

