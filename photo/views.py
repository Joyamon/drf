from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from .serializers import ImageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.http import FileResponse
from photo.models import Image


class UploadImageView(APIView):
    authentication_classes = []
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        file_serializer = ImageSerializer(data=request_data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=201)
        else:
            return Response(file_serializer.errors, status=400)


class DownloadImageView(APIView):
    authentication_classes = []

    def get(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        file_path = image.image.path
        return FileResponse(open(file_path, 'rb'))
