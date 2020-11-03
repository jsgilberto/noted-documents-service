from django.urls import path

from noted_documents.documents import views

urlpatterns = [
    path('documents/', views.list_or_create_document),
    path('documents/<str:slug>/', views.get_document),
    path('documents/<str:slug>/edit/', views.update_document),
    path('documents/<str:slug>/delete/', views.delete_document)
]