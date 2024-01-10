from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import os
from .serializers import ImageSerializer
from rest_framework.views import APIView
from django.http import FileResponse, HttpResponse
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


class CatImageView(APIView):
    authentication_classes = []

    def get(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=404)

        image_path = image.image.path
        image_name = image.name
        response = FileResponse(open(image_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{image_name}"'
        return response


class DownloadImageView(APIView):
    def get(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=404)

        image_path = image.image.path
        image_name = image.name
        file_extension = '.png'  # 文件扩展名

        with open(image_path, 'rb') as file:
            image_data = file.read()
        # 保存文件到本地
        file_path = os.path.join(image_name + file_extension)
        with open(image_path, 'rb') as file:
            with open(file_path, 'wb') as outfile:
                outfile.write(file.read())
        return FileResponse(open(file_path, 'rb'), as_attachment=True)