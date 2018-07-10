from django.conf.urls import url
from django.contrib import admin

from projeto.boards import views
app_name='forum'


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^boards/new/$', views.new_board, name='new_board'),
    url(r'^admin/', admin.site.urls),
]