from rest_framework import serializers
from models import Car, ModelLookUpI18n


class CarSerializer(serializers.ModelSerializer):
    model = serializers.PrimaryKeyRelatedField(read_only=True)
    model_display = serializers.Field(source='_get_model_display')
    status_label = serializers.Field(source='status_label')
    color = serializers.RelatedField()
    created_since = serializers.Field(source='created_since')
    url = serializers.Field(source='get_absolute_url')
    thumbnail = serializers.Field(source='thumbnail')
    year = serializers.RelatedField(source='model.year')
    created_at_format = serializers.Field(source='created_at_format')
    view_count = serializers.Field()
    available_i18n_models = serializers.Field(source='available_i18n_models')

    class Meta:
        model = Car
        fields = ('id', 'model', 'model_display', 'status', 'status_label', 'description', 'mileage', 'color',
                  'condition', 'asking_price', 'year', 'url', 'thumbnail',
                  'created_since', 'created_at_format', 'view_count', 'available_i18n_models')


class ColorSerializer(serializers.ModelSerializer):
    id = serializers.Field()
    value = serializers.RelatedField()

    class Meta:
        model = ModelLookUpI18n
        fields = ('id', 'value',)

