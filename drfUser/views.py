from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group, User
from drfUser.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password


class UserView(APIView):

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
            user = User.objects.get(username=request.data['username'])
            token = Token.objects.create(user=user)
            return Response(
                {'data': serializer.data,
                 'token': token.key,
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


    def get(self, request, **kwargs):
        if kwargs.get('pk'):
            group = Group.objects.get(pk=kwargs['pk'])
            serializer = GroupSerializer(group)
            return Response(
                {'data': serializer.data,
                 'status': status.HTTP_200_OK,
                 'message': 'Success'
                 }
            )
        else:
            group = Group.objects.all()
            serializer = GroupSerializer(group, many=True)
            return Response(
                {'data': serializer.data,
                 'status': status.HTTP_200_OK,
                 'message': 'Success'
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
