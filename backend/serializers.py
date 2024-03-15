from rest_framework import serializers

from backend.models import ParameterModel


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterModel
        fields = (
            "id",
            "cat_id",
            "data_length",
            "length",
            "name",
            "rus_name",
            "scaling",
            "range",
            "spn",
            "date",
            "status_delete",
        )
