from django.conf.urls import url, include
from django.contrib import admin
import doi.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(doi.urls)),
]
