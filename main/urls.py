from django.urls import path

from .views import (
    AboutPageView,
    BlogPostDetailView,
    BlogPostListView,
    ContactPageView,
    HiringPageView,
    HomePageView,
    ProjectDetailView,
    ProjectListView,
    ProductDetailView,
    ProductListView,
    RepresentativeListView,
    ServiceDetailView,
    ServiceListView,
    TeamPageView,
)

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path(
        'blog/<slug:slug>/',
        BlogPostDetailView.as_view(),
        name='blog-detail',
    ),
    path('about/', AboutPageView.as_view(), name='about'),
    path('team/', TeamPageView.as_view(), name='team'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path(
        'services/<slug:slug>/',
        ServiceDetailView.as_view(),
        name='service-detail',
    ),
    path('hiring/', HiringPageView.as_view(), name='hiring'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path(
        'representatives/',
        RepresentativeListView.as_view(),
        name='representative-list',
    ),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path(
        'projects/<str:slug>/',
        ProjectDetailView.as_view(),
        name='project-detail',
    ),
    path('products/', ProductListView.as_view(), name='product-list'),
    path(
        'products/<str:slug>/',
        ProductDetailView.as_view(),
        name='product-detail',
    ),
]
