import datetime
from django.contrib.auth.hashers import make_password, check_password
import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group, User
from drf.token import generate_token
from drf.utils import validate_ip
from drfUser.convert import convert_to_pinyin
from drfUser.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.versioning import QueryParameterVersioning
from django.core.cache import cache
from drfUser.sign import login_sign
from captcha.views import CaptchaStore, captcha_image
import base64
from rest_framework.pagination import PageNumberPagination


class UserView(APIView):
    versioning_class = QueryParameterVersioning  # 版本控制
    authentication_classes = []
    ordering = ('id',)

    def get(self, request):
        """
        获取所有用户
        :param request:
        :return:
        """
        users = User.objects.all().order_by(*self.ordering)
        page = PageNumberPagination()  # 产生一个分页器对象
        page.page_size = 4  # 默认每页显示的多少条记录
        page.page_query_param = 'page'  # 默认查询参数名为 page
        page.page_size_query_param = 'size'  # 前台控制每页显示的最大条数
        page.max_page_size = 10  # 后台控制显示的最大记录条数，防止用户输入的查询条数过大
        ret = page.paginate_queryset(users, request)
        serializer = UserSerializer(ret, many=True)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'Success',
                'page': page.get_paginated_response(serializer.data).data,
                'size': page.page_size,

            }
        )

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='string')
            }
        ),
        responses={200: openapi.Response('Success', UserSerializer), 400: 'Bad Request'}
    )
    @action(methods=['post'], detail=False)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(request.data.get('password'))
            serializer.validated_data['password'] = password
            serializer.save()
            return Response(
                {'data': serializer.data,
                 'status': status.HTTP_200_OK,
                 'message': 'Success'

                 })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewDetails(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(
            {'data': serializer.data,
             'status': status.HTTP_200_OK,
             'message': 'Success'
             }
        )

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data,
                 'status': status.HTTP_200_OK,
                 'message': 'Success'
                 }
            )
        return Response(
            {
                'message': serializer.errors,
                'status': status.HTTP_400_BAD_REQUEST
            }
        )

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(
            {
                'message': 'Success',
                'status': status.HTTP_204_NO_CONTENT,
                'data': []
            }
        )


class GroupView(APIView):
    versioning_class = QueryParameterVersioning

    def get(self, request, **kwargs):
        try:
            if kwargs.get('pk') and request.version == 'v1.0':
                group = Group.objects.get(pk=kwargs['pk'])
                serializer = GroupSerializer(group)
                return Response(
                    {'data': serializer.data,
                     'status': status.HTTP_200_OK,
                     'message': 'Success'
                     }
                )
            elif request.version == 'v1.0':
                group = Group.objects.all()
                serializer = GroupSerializer(group, many=True)
                return Response(
                    {'data': serializer.data,
                     'status': status.HTTP_200_OK,
                     'message': 'Success'
                     }
                )
            elif not request.version:
                return Response(
                    {'data': [],
                     'status': status.HTTP_400_BAD_REQUEST,
                     'message': 'Version is not found'
                     }
                )
        except Group.DoesNotExist:
            return Response(
                {'data': [],
                 'status': status.HTTP_404_NOT_FOUND,
                 'message': 'Data is not exists'
                 }
            )

    def post(self, request, **kwargs):
        if not kwargs.get('pk'):
            serializer = GroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'data': serializer.data,
                     'status': status.HTTP_201_CREATED,
                     'message': 'Success'
                     }
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'data': None,
                 'status': status.HTTP_400_BAD_REQUEST,
                 'message': 'Bad Request'}
            )

    def put(self, request, **kwargs):
        if kwargs.get('pk'):
            group = Group.objects.get(pk=kwargs['pk'])
            serializer = GroupSerializer(group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'data': serializer.data,
                     'status': status.HTTP_200_OK,
                     'message': 'Success'}
                )
        else:
            return Response(
                {
                    'data': 'Group id is required',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Failure'
                }
            )

    def delete(self, request, **kwargs):
        """
        Delete a group
        :param request:
        :param kwargs:
        :return:
        单个删除：
        http://127.0.0.1:8000/user/group/5/
        批量删除
        [
            {"id":5,"name":"精英组" },
            {"id":6,"name":"工人组"},
            {"id":7,"name":"测试组"}
        ]
        """
        if kwargs.get('pk'):
            group = Group.objects.get(pk=kwargs['pk'])
            group.delete()
            return Response(
                {'data': None,
                 'status': status.HTTP_200_OK,
                 'message': 'Success'}
            )
        else:
            for content in request.data:
                Group.objects.get(id=content['id']).delete()
            return Response(
                {'data': 'None',
                 'status': status.HTTP_200_OK,
                 'message': 'Success'
                 }
            )


from django_celery_beat.models import PeriodicTask, CrontabSchedule


class CreateTaskView(APIView):
    """创建任务视图"""
    authentication_classes = []

    def post(self, request):
        """创建任务 接口传参,示例
        {
           "task_name": "任务名称",
           "arg1": "参数1",
           "arg2": "参数2",
           "task_cron": "*/2 * * * *"
        }
        """
        task_name = request.data.get("task_name")
        cron_value = request.data.get("task_cron")
        cron_list = str(cron_value).split(' ')

        if len(cron_list) != 5:
            return Response(
                {
                    'data': [],
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'cron is not correct, example: */2 * * * *'
                }
            )

        # 创建或更新CrontabSchedule
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=cron_list[0],
            hour=cron_list[1],
            day_of_week=cron_list[2],
            day_of_month=cron_list[3],
            month_of_year=cron_list[4],
            # timezone=pytz.timezone("Asia/Shanghai"),
        )

        if PeriodicTask.objects.filter(name=task_name).exists():
            return Response(
                {
                    'data': [],
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'task name already exists'
                }
            )

        periodic_task = PeriodicTask.objects.create(
            crontab=schedule,
            name=task_name,
            task='drfUser.tasks.run_test_task',
            queue='run_test_task'  # 设置队列名称
        )

        periodic_task.enabled = True
        periodic_task.save()

        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'success'
            }
        )

    def put(self, request):
        """
        禁止定时任务
        """
        pk = request.data
        periodicTask = PeriodicTask.objects.filter(id=pk['id']).first()
        periodicTask.enabled = False  # 设置为禁用状态
        periodicTask.save()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'success'
            }
        )


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # 通过username查询用户
        user = User.objects.filter(username=username).first()
        if not user or not check_password(password, user.password):
            return Response(
                {
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Incorrect username or password',

                }
            )
        token = generate_token(username)
        try:
            cache.set('token', token, 60 * 60 * 24)  # token存到redis
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'User not found',

                }
            )
        User.objects.filter(id=user.id).update(last_login=timezone.now())  # 更新最后登录时间
        login_sign.send(username=username)  # 发送登录信号
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'success',
                'data': {
                    'username': username,
                    'token': token
                }
            }
        )


class ModifyPasswordView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        # 通过username查询用户
        user = User.objects.filter(username=username).first()
        if not user or not check_password(old_password, user.password):
            return Response(
                {
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Incorrect username or password',

                }
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': 'success',
                'data': []
            }
        )


class ResetPasswordView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        # 通过username查询用户
        user = User.objects.filter(username=username).first()
        if not user:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'User not found',
                    'data': []
                }
            )
        username = convert_to_pinyin(username)
        user.set_password(username)
        user.save()
        return Response(
            {
                'status': status.HTTP_200_OK,
                'message': f'password initial success,your password is:{username}',
                'data': []

            }
        )


class LogoutView(APIView):
    authentication_classes = []

    def post(self, request):
        # 清除token
        if cache.get('token'):
            cache.delete('token')
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'success',
                    'data': []
                }
            )
        else:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'User not found',
                    'data': []
                }
            )


class CaptchaView(APIView):
    authentication_classes = []

    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        id = CaptchaStore.objects.filter(hashkey=hashkey).first().id
        image = captcha_image(request, hashkey)
        # 将图片转换为base64
        image_base = base64.b64encode(image.content)
        data = {
            "key": id,
            "image_base": "data:image/png;base64," + image_base.decode("utf-8"),
        }
        return Response(data=data)


from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


class APSSchedulerView(APIView):
    authentication_classes = []

    @staticmethod
    def tick():
        print('定时任务开始执行! The time is: %s' % datetime.now())

    def post(self, request):
        hour = int(request.data.get('hour'))
        minute = int(request.data.get('minute'))
        scheduler = BlockingScheduler()
        scheduler.add_job(self.tick, 'cron', hour=hour, minute=minute)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            raise

        return Response(data={'message': '定时任务添加成功！'})


from django.contrib.gis.geoip2 import GeoIP2
import geoip2
from urllib.parse import urlparse


class IpView(APIView):
    authentication_classes = []

    def details(self, ip):
        g = GeoIP2()
        details = g.city(ip)
        return details

    def get(self, request):
        try:
            ip = request.data.get('ip')
            is_ip = ip.replace('.', '')
            if not ip:
                return Response(data={'message': 'please input ip first'})

            elif is_ip.isdigit():
                if not validate_ip(ip):
                    details = 'address is not valid'
                    return Response(
                        {
                            'data': {
                                'details': details
                            },
                            'success': True,
                            'message': 'Success'
                        }
                    )
                else:
                    details = self.details(ip)
                    return Response(
                        {
                            'data': {
                                'details': details
                            },
                            'success': True,
                            'message': 'Success'
                        }
                    )
            elif 'http' in ip or 'https' in ip:
                ip = urlparse(ip).netloc
                details = self.details(ip)
                return Response(
                    {
                        'data': {
                            'details': details
                        },
                        'success': True,
                        'message': 'Success'
                    }
                )
            else:
                details = self.details(ip)
                return Response(
                    {
                        'data': {
                            'details': details
                        },
                        'success': True,
                        'message': 'Success'
                    }
                )
        except geoip2.errors.AddressNotFoundError:
            details = f'The {ip} address could not be found.'
            return Response(
                {
                    'data': {
                        'details': details
                    },
                    'success': True,
                    'message': 'Success'
                }
            )
