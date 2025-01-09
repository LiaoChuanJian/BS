from django.db import models
from accounts.models import UserProfile
# Create your models here.
class RandomManager(models.Manager):
    """
    自定义管理器，用于获取随机排序的查询集
    """
    def get_queryset(self):
        return super(RandomManager, self).get_queryset().order_by('?')


class JDGoods(models.Model):
    """
    京东商品模型
    """
    jd_id = models.CharField(verbose_name='商品ID', blank=True, null=True, default='0', max_length=100)
    jd_name = models.CharField(verbose_name='商品名称', blank=True, null=True, default='0', max_length=1000)
    jd_shop = models.CharField(verbose_name='店铺名称', blank=True, null=True, default='0', max_length=100)
    jd_price = models.FloatField(verbose_name='价格', default=0.0)
    jd_allcomment = models.IntegerField(verbose_name='所有评论', default=0)  # 所有评论数量
    jd_goodcomment = models.IntegerField(verbose_name='好评', default=0)  # 好评数量
    jd_generalcomment = models.IntegerField(verbose_name='中评', default=0)  # 中评数量
    jd_poorcomment = models.IntegerField(verbose_name='差评', default=0)  # 差评数量
    goods_url = models.CharField(verbose_name='商品链接', blank=True, null=True, default='0', max_length=1000)

    def __str__(self):
        return self.jd_name  # 返回商品名称作为字符串表示

    class Meta:
        ordering = ['-id']  # 默认按照 ID 降序排列
        verbose_name = '全部商品'  # 单数形式的可读名称
        verbose_name_plural = '全部商品'  # 复数形式的可读名称


class SearchKey(models.Model):
    """
    用户搜索关键字模型
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # 关联的用户
    key = models.CharField(verbose_name='搜索词', blank=True, null=True, default='0', max_length=100)

    def __str__(self):
        return str(self.user)  # 返回用户的字符串表示

    class Meta:
        ordering = ['-id']  # 默认按照 ID 降序排列
        verbose_name = '搜索词'  # 单数形式的可读名称
        verbose_name_plural = '搜索词'  # 复数形式的可读名称


class MyFollow(models.Model):
    """
    用户关注商品模型
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # 关注的用户
    good = models.ForeignKey(JDGoods, on_delete=models.CASCADE)  # 关注的商品
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')  # 记录最后修改时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 记录创建时间

    def __str__(self):
        return str(self.user)  # 返回用户的字符串表示

    class Meta:
        ordering = ['-id']  # 默认按照 ID 降序排列
        verbose_name = '关注'  # 单数形式的可读名称
        verbose_name_plural = '关注'  # 复数形式的可读名称