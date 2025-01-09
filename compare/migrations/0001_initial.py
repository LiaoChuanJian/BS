from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True  # 表示这是一个初始迁移

    # 定义依赖关系，确保在用户模型创建后运行此迁移
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 创建 JDGoods 模型，用于存储京东商品信息
        migrations.CreateModel(
            name='JDGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jd_id', models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='京东ID')),
                ('jd_name', models.CharField(blank=True, default='0', max_length=1000, null=True, verbose_name='商品名称')),
                ('jd_shop', models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='店铺名称')),
                ('jd_price', models.FloatField(default=0.0, verbose_name='价格')),
                ('jd_allcomment', models.IntegerField(default=0, verbose_name='所有评论')),
                ('jd_goodcomment', models.IntegerField(default=0, verbose_name='好评')),
                ('jd_generalcomment', models.IntegerField(default=0, verbose_name='中评')),
                ('jd_poorcomment', models.IntegerField(default=0, verbose_name='差评')),
                ('goods_url', models.CharField(blank=True, default='0', max_length=1000, null=True, verbose_name='商品链接')),
            ],
            options={
                'verbose_name': '京东商品',  # 在管理界面中显示的单数形式
                'verbose_name_plural': '京东商品',  # 在管理界面中显示的复数形式
                'ordering': ['-id'],  # 默认按照 ID 降序排列
            },
        ),
        # 创建 SearchKey 模型，用于存储用户搜索的关键词
        migrations.CreateModel(
            name='SearchKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='搜索词')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),  # 关联 User 模型
            ],
            options={
                'verbose_name': '搜索词',  # 在管理界面中显示的单数形式
                'verbose_name_plural': '搜索词',  # 在管理界面中显示的复数形式
                'ordering': ['-id'],  # 默认按照 ID 降序排列
            },
        ),
    ]
