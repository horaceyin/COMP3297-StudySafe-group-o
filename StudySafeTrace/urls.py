from django.urls import path
from StudySafeTrace import views

urlpatterns = [
    path('', views.BaseView.as_view()),
    path('venues/', views.VenuesView.as_view()),
    path('contacts/', views.ContactsView.as_view())
]