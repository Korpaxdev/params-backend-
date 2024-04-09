from rest_framework import serializers

from backend.models import ParameterModel, BufferedParameterModel


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


class ToDeleteParameterListSerializer(serializers.ListSerializer):
    def update(self, instances, validated_data):
        ids = [data["id"] for data in validated_data]
        to_update = instances.filter(id__in=ids)
        for instance in to_update:
            instance.status_delete = True
        instances.bulk_update(to_update, ["status_delete"])
        return to_update


class ToDeleteParameterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        try:
            instance = self.instance.get(id=value)
            if instance.status_delete:
                raise serializers.ValidationError(f"Параметр c ID = {value} уже помечен на удаление")
        except ParameterModel.DoesNotExist:
            raise serializers.ValidationError(f"Параметра с ID = {value} не существует")
        return value

    class Meta:
        model = ParameterModel
        fields = ("id",)
        list_serializer_class = ToDeleteParameterListSerializer


class BufferedParameterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        instance = self.Meta.model(**validated_data, user=user)
        instance.save()
        return instance

    class Meta:
        model = BufferedParameterModel
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
        read_only_fields = ("id", "date")
