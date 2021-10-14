from rest_framework.serializers import ModelSerializer

from .models import Ad


class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = ('advertiser', 'title', 'imgUrl', 'link',)
