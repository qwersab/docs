from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.db.models import Q
import os
from datetime import datetime
from .models import User, Product
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, 
    UserUpdateSerializer, ProductSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        # 更新登录时间
        user.login_at = timezone.now()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

class UserInfoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UpdateUserView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class UploadProfilePictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'profile_picture' not in request.FILES:
            return Response(
                {'error': '请选择要上传的图片文件'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        # 删除旧的头像文件（如果存在）
        if user.profile_picture:
            user.profile_picture.delete(save=False)
            
        # 保存新的头像文件
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        
        return Response({
            'message': '头像上传成功',
            'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
        })

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # 验证必填字段
        if not all([old_password, new_password, confirm_password]):
            return Response(
                {'error': '请提供所有必需的密码字段'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证旧密码
        if not user.check_password(old_password):
            return Response(
                {'error': '旧密码不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证新密码和确认密码是否匹配
        if new_password != confirm_password:
            return Response(
                {'error': '新密码和确认密码不匹配'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证新密码长度
        if len(new_password) < 8:
            return Response(
                {'error': '新密码长度不能少于8个字符'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 更新密码
        user.set_password(new_password)
        user.save()

        # 更新session认证，防止用户被登出
        update_session_auth_hash(request, user)

        return Response({
            'message': '密码修改成功'
        })

class CreateProductView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 处理cover_list字段，确保它是字符串格式
        if 'cover_list' in request.data and isinstance(request.data['cover_list'], list):
            request.data['cover_list'] = ','.join(request.data['cover_list'])
            
        return super().create(request, *args, **kwargs)

class ListUserProductsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

class ProductCategoriesView(APIView):
    """获取商品分类列表"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = [
            {'id': id, 'name': name}
            for id, name in Product.CATEGORY_CHOICES
        ]
        return Response(categories)

class UploadProductImageView(APIView):
    """商品图片上传接口 - 支持多图上传"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'images[]' not in request.FILES:
            return Response(
                {'error': '请选择要上传的图片文件'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 获取所有上传的图片
        images = request.FILES.getlist('images[]')
        
        # 验证图片数量
        if len(images) > 10:
            return Response(
                {'error': '一次最多只能上传10张图片'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 允许的文件类型
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        # 存储上传成功的图片URL
        uploaded_urls = []
        # 存储上传失败的图片信息
        failed_uploads = []

        for image in images:
            try:
                # 验证文件类型
                if image.content_type not in allowed_types:
                    failed_uploads.append({
                        'name': image.name,
                        'error': '不支持的图片格式。支持的格式：JPG, PNG, GIF, WEBP'
                    })
                    continue
                    
                # 验证文件大小（限制为5MB）
                if image.size > 5 * 1024 * 1024:
                    failed_uploads.append({
                        'name': image.name,
                        'error': '图片大小不能超过5MB'
                    })
                    continue

                # 生成文件保存路径
                current_date = datetime.now().strftime('%Y%m%d')
                filename = f"{current_date}_{image.name}"
                relative_path = os.path.join('products', str(request.user.id), filename)
                
                # 确保目录存在
                full_path = os.path.join(settings.MEDIA_ROOT, 'products', str(request.user.id))
                os.makedirs(full_path, exist_ok=True)
                
                # 保存文件
                full_file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                with open(full_file_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                        
                # 生成访问URL并添加到成功列表
                image_url = request.build_absolute_uri(settings.MEDIA_URL + relative_path)
                uploaded_urls.append(image_url)

            except Exception as e:
                failed_uploads.append({
                    'name': image.name,
                    'error': str(e)
                })

        # 构建响应数据
        response_data = {
            'message': f'成功上传 {len(uploaded_urls)} 张图片' + 
                      (f'，{len(failed_uploads)} 张上传失败' if failed_uploads else ''),
            'urls': uploaded_urls,
        }
        
        # 如果有上传失败的图片，添加到响应中
        if failed_uploads:
            response_data['failed'] = failed_uploads

        # 如果所有图片都上传失败，返回400状态码
        if not uploaded_urls and failed_uploads:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(response_data)

class ListAllProductsView(generics.ListAPIView):
    """获取所有用户发布的商品列表，支持搜索和过滤"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all().order_by('-create_at')
        
        # 搜索商品名称
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        # 按分类过滤
        category = self.request.query_params.get('category', None)
        if category and category.isdigit():
            queryset = queryset.filter(category_id=int(category))
            
        # 按价格范围过滤
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price and min_price.replace('.', '').isdigit():
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price and max_price.replace('.', '').isdigit():
            queryset = queryset.filter(price__lte=float(max_price))
            
        # 按是否可议价过滤
        is_bargain = self.request.query_params.get('is_bargain', None)
        if is_bargain is not None:
            is_bargain = is_bargain.lower() == 'true'
            queryset = queryset.filter(is_bargain=is_bargain)
            
        # 按新旧程度过滤
        min_old_level = self.request.query_params.get('min_old_level', None)
        max_old_level = self.request.query_params.get('max_old_level', None)
        if min_old_level and min_old_level.isdigit():
            queryset = queryset.filter(old_level__gte=int(min_old_level))
        if max_old_level and max_old_level.isdigit():
            queryset = queryset.filter(old_level__lte=int(max_old_level))
            
        return queryset