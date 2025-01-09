from django.db import migrations, models


class Migration(migrations.Migration):

    # 定义依赖关系，确保该迁移在指定的用户资料迁移后执行
    dependencies = [
        ('accounts', '0003_auto_20220302_1708'),
    ]

    # 当前迁移中执行的操作
    operations = [
        # 为 UserProfile 模型添加新的字段 header_image
        migrations.AddField(
            model_name='userprofile',
            name='header_image',
            field=models.ImageField(
                upload_to='',         # 上传图片的存储路径，可以根据需要自定义
                max_length=100,       # 图片文件名的最大字符数
                blank=True,           # 允许字段为空
                null=True,            # 允许字段在数据库中为 null
                default='default.jpg',  # 默认为 'default.jpg'
                verbose_name='头像'    # 管理界面中显示的字段名称
            ),
        ),
    ]
