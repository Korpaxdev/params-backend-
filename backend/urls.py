from django.urls import path

from backend import views

urlpatterns = [path("parameters/", views.ParametersView.as_view(), name="parameters")]
