from django.urls import path

from backend import views

urlpatterns = [
    path("parameters/", views.ParametersView.as_view(), name="parameters"),
    path("parameters/create/", views.CreateBufferedParameterView.as_view(), name="create_parameter"),
    path("parameters/to-delete/", views.ToDeleteParametersView.as_view(), name="to_delete"),
]
