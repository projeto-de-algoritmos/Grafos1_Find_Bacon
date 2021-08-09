from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_from_kevin_bacon_wikipedia_page, name='search_home'),
    path('search/<page>/', views.page_search_result, name='search_result'),
    path('graph-pages/', views.available_pages, name='graph_available_pages')
]