from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, filters as searchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from django_filters import rest_framework as filters

from .models import User, AuthToken
from .serializers import UserSerializer
from project_backend.utils import Response
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
    if not request.data.get('password'):
        return JsonResponse(
        {'status': False, 'data': None, 'msg': 'Password not provided. Authentication Failed'}, status=400)

    user_data = {'email': email, 'phone_number': phone_number, 'username': username,
                 'first_name': first_name.title(), 'last_name': last_name.title(), 'address': address,
                 'is_store_owner': is_store_owner}
    user = User.objects.create(**user_data)
    user.set_password(request.data.get('password'))
    user.save()
    token = AuthToken.objects.create(user=user)
    res_data = {'token': token.key, 'user': UserSerializer(user).data}
    return Response(res_data, msg="Signup Successful")

class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    renderer_classes=[ApiRenderer]
    permission_classes = [IsAuthenticated,]
    filter_backends = [filters.DjangoFilterBackend, searchFilter.SearchFilter]
    filterset_fields = ['first_name', 'last_name', 'email', 'phone_number', 'is_store_owner']
    search_fields = ['first_name', 'last_name', 'email', '^phone_number']

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [ApiRenderer]
    permission_classes = [IsAuthenticated,]

    def put(self, request, *args, **kwargs):
        user: User = request.user
        if user.id == self.kwargs.get('pk'):
            email = request.data.get('email', '')
            if email and email != user.email:
                raise APIException('Cannot change Email')
            return self.partial_update(request, *args, **kwargs)
        else:
            raise APIException('You don\'t have necessary permissions')


@api_view(["POST"])
@permission_classes([AllowAny,])
@renderer_classes([ApiRenderer])
def login_user(request):
    try:
        user = User.objects.get(email=request.data.get('email'))
    except User.DoesNotExist:
        raise APIException("User Doesnot Exist")
    serializer = UserSerializer(user).data
    if not request.data.get('password'):
        return JsonResponse(
            {'status': False, 'data': None, 'msg': 'Password not provided. Authentication Failed'}, status=400)
    if user.check_password(request.data.get('password')):
        token = AuthToken.objects.get(user=user)
        res_data =  {'token': token.key, 'user': serializer}
        return Response(data=res_data, msg='User Verification Successful')
    return JsonResponse(
        {'status': False, 'data': None, 'msg': 'User verification Failed. Check email or password'}, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated,])
@renderer_classes([ApiRenderer])
def verify_token(request):
    try:
        res_data = {'user': UserSerializer(request.user).data, 'token': AuthToken.objects.get(user=request.user).key}
        return Response(res_data, msg="Token verified Successfully")
    except Exception:
        raise APIException("Invalid Token")

class AdminUserList(generics.ListAPIView):
    queryset = User.objects.filter(is_admin=True).order_by('first_name')
    serializer_class = UserSerializer
    renderer_classes = [ApiRenderer]
    permission_classes = (IsAuthenticated,)