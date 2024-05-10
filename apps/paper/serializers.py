from rest_framework import serializers
from .models import Image, Sort

class ImageSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'img_name', 'img_size', 'img_down_link', 'weight', 'sort', 'uploader', 'img_url']

    def get_img_url(self, obj):
        return obj.img_down_link   # 假设 img_down_link 已经是图片的 URL

class SortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sort
        fields = ['id', 'sortName', 'firstPaper']
