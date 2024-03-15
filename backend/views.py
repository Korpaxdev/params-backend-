from rest_framework import generics

from backend.models import ParameterModel
from backend.serializers import ParameterSerializer


# Create your views here.


class ParametersView(generics.ListAPIView):
    serializer_class = ParameterSerializer
    queryset = ParameterModel.objects.all()
