from django.db import migrations, models


class Migration(migrations.Migration):

    # 定义依赖关系，确保该迁移在指定的迁移后执行
    dependencies = [
        ('accounts', '0002_auto_20220302_1705'),
    ]

    # 当前迁移中执行的操作
    operations = [
        # 修改 UserProfile 模型的 email 字段，添加唯一性约束
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(
                max_length=100,  # 字段最大长度
                blank=True,      # 允许字段为空
                null=True,       # 允许字段在数据库中为 null
                default='',      # 默认值为空字符串
                verbose_name='邮箱',  # 管理界面中显示的字段名称
                unique=True,     # 添加唯一性约束，确保每个 email 只能出现一次
            ),
        ),
        # 修改 UserProfile 模型的 mobile 字段，保持之前配置
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(
                max_length=100,  # 字段最大长度
                blank=True,      # 允许字段为空
                null=True,       # 允许字段在数据库中为 null
                default='',      # 默认值为空字符串
                verbose_name='手机'  # 管理界面中显示的字段名称
            ),
        ),
    ]
