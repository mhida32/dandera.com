from django.urls import path
from . import views


urlpatterns = [
    path('', views.news_list_view, name='news_list'),
    path('news/<int:news_id>/', views.news_detail_view,name='news_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name='logout'),
]

# example windows
(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'C:/python25/lib/site-packages/project/media/', 'show_indexes': True}),

