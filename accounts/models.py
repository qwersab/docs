from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(unique=True, null=True)
    login_at = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # 添加related_name解决冲突
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='accounts_user_set',
        related_query_name='accounts_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_set',
        related_query_name='accounts_user'
    )

class Product(models.Model):
    # 商品分类常量
    CATEGORY_BOOK = 1
    CATEGORY_PHONE = 2
    CATEGORY_CLOTHING = 3
    CATEGORY_OTHER = 4

    CATEGORY_CHOICES = [
        (CATEGORY_BOOK, '书本'),
        (CATEGORY_PHONE, '手机'),
        (CATEGORY_CLOTHING, '衣服'),
        (CATEGORY_OTHER, '其他'),
    ]

    name = models.CharField(max_length=200, null=True, verbose_name='商品名')
    category_id = models.IntegerField(
        choices=CATEGORY_CHOICES,
        null=True,
        verbose_name='商品分类id'
    )
    cover_list = models.TextField(null=True, verbose_name='商品封面列表')
    detail = models.TextField(null=True, verbose_name='商品简介')
    inventory = models.IntegerField(null=True, default=1, verbose_name='库存')
    is_bargain = models.BooleanField(null=True, default=False, verbose_name='是否支持砍价')
    old_level = models.IntegerField(null=True, verbose_name='新旧程度')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='价格')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='发布者')
    create_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-create_at']

    def __str__(self):
        return self.name or '未命名商品'

    def clean(self):
        # 验证分类ID
        if self.category_id and self.category_id not in dict(self.CATEGORY_CHOICES):
            raise ValidationError({
                'category_id': f'无效的分类ID: {self.category_id}'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def category_name(self):
        """获取分类名称"""
        return dict(self.CATEGORY_CHOICES).get(self.category_id, '未知分类')