from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    # 定义迁移依赖关系，确保在用户模型和 Compare 应用的初始迁移后执行
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compare', '0001_initial'),
    ]

    operations = [
        # 为 JDGoods 模型添加管理器 randoms
        migrations.AlterModelManagers(
            name='jdgoods',
            managers=[
                ('randoms', django.db.models.manager.Manager()),  # 自定义管理器，用于随机获取 JDGoods
            ],
        ),
        # 创建 MyFollow 模型，用于记录用户关注的商品
        migrations.CreateModel(
            name='MyFollow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),  # 记录最后修改时间
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),  # 记录创建时间
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compare.jdgoods', verbose_name='关注的商品')),  # 关联 JDGoods 模型
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关注的用户')),  # 关联用户模型
            ],
            options={
                'verbose_name': '关注',  # 在管理界面中显示的单数形式
                'verbose_name_plural': '关注',  # 在管理界面中显示的复数形式
                'ordering': ['-id'],  # 默认按照 ID 降序排列
            },
        ),
    ]
