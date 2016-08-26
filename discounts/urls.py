from agreements.views import json_view, home
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^$', home),
    url(r'^agreements/calendar', json_view),
    url(r'^admin/', admin.site.urls),
]
