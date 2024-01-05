import datetime
import json
from django.contrib.auth.hashers import make_password, check_password
import pytz
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group, User

from drf.authentication import CustomAuthentication
from drfUser.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.versioning import QueryParameterVersioning
from django.core.cache import cache


class UserView(APIView):
    versioning_class = QueryParameterVersioning  # 版本控制
    authentication_classes = []

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(
            {'data': serializer.data,
             'status': status.HTTP_200_OK,
             'message': 'Success',
             }
        )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(request.data.get('password'))
            serializer.validated_data['password'] = password
            serializer.save()
            # user = User.objects.get(username=request.data['username'])
            # token = Token.objects.create(user=user)
            return Response(
                {'data': serializer.data,
                 # 'token': token.key,
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
            timezone=pytz.timezone("Asia/Shanghai")
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
            task='drfUser.tasks.run_test',
        )

        periodic_task.enabled = True
        periodic_task.save()

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
        token = PasswordResetTokenGenerator().make_token(user=user)
        try:
            cache.set('token', token, 60 * 60 * 24)  # token存到redis
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'User not found',

                }
            )
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
