from django.urls import reverse
from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    # download_url = serializers.HyperlinkedIdentityField(view_name='download_image', format='html')
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'name', 'image', 'download_url')

    def get_download_url(self, image):
        request = self.context.get('request')
        if image.image and request is not None:
            return request.build_absolute_uri(reverse('download_image', kwargs={'image_id': image.pk}))
        return None

