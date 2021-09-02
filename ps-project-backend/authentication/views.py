from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from .models import User, AuthToken
from .serializers import UserSerializer
from project_backend.drf_utils import Response
from project_backend.renderer import ApiRenderer

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
@renderer_classes([ApiRenderer])
def signup(request):
    email = request.data.get('email')
    phone_number = request.data.get('phone_number')
    username = request.data.get('username', '')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    address = request.data.get('address', {})
    is_store_owner = request.data.get('is_store_owner', False)
    if email and User.objects.filter(email=email).exists():
        raise APIException("User with same email already exists")
    if phone_number and User.objects.filter(phone_number=phone_number).exists():
        raise APIException("User with same phone number already exists")

    user_data = {'email': email, 'phone_number': phone_number, 'username': username,
                 'first_name': first_name, 'last_name': last_name, 'address': address,
                 'is_store_owner': is_store_owner}
    user = User.objects.create(**user_data)
    if 'password' in request.data and request.data.get('password'):
        user.set_password(request.data.get('password'))
        user.save()
    token = AuthToken.objects.create(user=user)
    res_data = {'token': token.key, 'user': UserSerializer(user).data}
    return Response(res_data, msg="Signup Successful")

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes=[ApiRenderer]
    permission_classes = [IsAuthenticated,]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
@permission_classes([AllowAny,])
@renderer_classes([ApiRenderer])
def verify_user_and_return_token(request):
    user = User.objects.get(email=request.data.get('email'))
    serializer = UserSerializer(user).data
    if user.check_password(request.data.get('password')):
        token = AuthToken.objects.get(user=user)
        res_data =  {'token': token.key, 'user': serializer}
        return Response(data=res_data, msg='User Verification Successful')
    return Response(msg="User verification Failed. Check email or password")