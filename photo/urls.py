from django.urls import path
from photo import views

urlpatterns = [
    path('upload/', views.UploadImageView.as_view(), name='upload_image'),
    path('cat/<int:image_id>/', views.CatImageView.as_view(), name='download_image'),
    path('download/<int:image_id>/', views.DownloadImageView.as_view(), name='download_image'),
]
