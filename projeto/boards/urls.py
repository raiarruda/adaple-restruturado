from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from projeto.boards import views
app_name='boards'


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('boards/<int:pk>/', views.board_topics, name='board_topics'),
    path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),
]
