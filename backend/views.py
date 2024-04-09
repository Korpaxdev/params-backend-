from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from backend.models import ParameterModel, BufferedParameterModel
from backend.serializers import ParameterSerializer, ToDeleteParameterSerializer, BufferedParameterSerializer


# Create your views here.


class ParametersView(generics.ListAPIView):
    serializer_class = ParameterSerializer
    queryset = ParameterModel.objects.all()


class ToDeleteParametersView(generics.GenericAPIView):
    serializer_class = ToDeleteParameterSerializer
    queryset = ParameterModel.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs):
        instances = self.get_queryset()
        serializer = self.serializer_class(instances, data=request.data, allow_empty=False, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreateBufferedParameterView(generics.CreateAPIView):
    serializer_class = BufferedParameterSerializer
    queryset = BufferedParameterModel.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}, many=True, allow_empty=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
