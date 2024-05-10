from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image, Sort
from .serializers import ImageSerializer, SortSerializer
from rest_framework import viewsets
from .tools import BianPic



class HelloWorldView(viewsets.ViewSet):
    def list(self, request):
        # 返回Hello World响应
        return Response({'message': 'Hello, World!'})

class PushImagesView(APIView):
    def post(self, request):
        request_data = request.data
        start = request_data.get('start', None)
        end = request_data.get('end', None)
        obj = BianPic()
        image_url = obj.url_constructor(start, end)
        imageDatas = []
        for i in image_url:
            imageDatas.extend(obj.get_one_page_all_links(i))
            print(f'第{i}页已获取完成')

        for data in imageDatas:
            img_name = data['img_name']
            img_size = data['img_size']
            img_down_link = data['img_down_link']
            print(img_down_link)

            # 检查是否已存在，如果不存在则添加
            existing_image = Image.objects.filter(img_down_link=img_down_link).first()
            if existing_image is None:
                new_image = Image(img_name=img_name, img_size=img_size, img_down_link=img_down_link)
                print(new_image)
                new_image.save()

        return Response("Data stored successfully!")

class UpWeightView(APIView):
    def post(self, request):
        request_data = request.data
        image_id = request_data.get('id', '1')
        sort = request_data.get('sort', 'download')
        weight = 1
        if sort == 'download':
            weight = 2
        elif sort == 'share':
            weight = 1

        try:
            existedImage = Image.objects.get(id=image_id)
            existedImage.weight += weight
            existedImage.save()
            print(f'Id:{existedImage.id}的图片，权重提升{weight},当前权重{existedImage.weight}')
            return Response('Success')
        except Image.DoesNotExist:
            return Response('Image not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetHotsView(APIView):
    def post(self, request):
        images = Image.objects.order_by('-weight').all()[:20]
        image_list = []
        for image in images:
            image_data = {
                'image_id': image.id,
                'img_name': image.img_name,
                'img_size': image.img_size,
                'img_down_link': image.img_down_link,
                'img_weight': image.weight,
                'sortName': image.sort.sortName if image.sort else None,
            }
            image_list.append(image_data)

        return Response(image_list)

import random

class GetSortInfoView(APIView):
    def post(self, request):
        data = request.data
        sortName = data.get('sortName')
        firstPaper = data.get('firstPaper')
        existedSort = Sort.objects.filter(sortName=sortName).first()
        if not existedSort:
            newSort = Sort(sortName=sortName, firstPaper=firstPaper)
            newSort.save()
            return Response('类型新建成功', status=status.HTTP_201_CREATED)
        return Response('类型已存在', status=status.HTTP_200_OK)

class GetSortInfoListView(APIView):
    def post(self, request):
        sorts = Sort.objects.all().order_by('-id')
        sortList = SortSerializer(sorts, many=True).data
        return Response(sortList)


class DeleteSortInfo(APIView):
    def post(self, request):
        # 获取请求中的 'id' 参数
        id = request.data.get('id')
        # 检查 'id' 是否存在
        if id is None:
            return Response({'error': '未提供ID参数'}, status=status.HTTP_400_BAD_REQUEST)
        # 尝试获取 Sort 对象
        sort = Sort.objects.filter(id=id).first()
        # 如果 Sort 对象不存在，返回错误信息
        if sort is None:
            return Response({'error': 'Sort不存在'}, status=status.HTTP_404_NOT_FOUND)
        # 删除 Sort 对象
        sort.delete()
        #返回成功响应
        return Response({'message': 'Sort删除成功'}, status=status.HTTP_200_OK)

class GetImagesView(APIView):
    def post(self, request):
        images = Image.objects.all().order_by('-id')
        random_images = random.sample(list(images), min(40, len(images)))
        image_list = ImageSerializer(random_images, many=True).data
        return Response(image_list)

class SearchingPaperView(APIView):
    def post(self, request):
        requestData = request.data
        keyword = requestData.get('keyword', '原神').lower()
        images = Image.objects.filter(img_name=keyword).order_by('-id')[:40]
        image_list = ImageSerializer(images, many=True).data
        return Response(image_list)