from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('submit-article/', views.submit_article, name='submit_article'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('profile/', views.profile, name='profile'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('search/', views.search, name='search'),
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
]