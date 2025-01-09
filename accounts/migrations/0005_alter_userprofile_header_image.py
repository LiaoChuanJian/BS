from django.db import migrations, models

class Migration(migrations.Migration):

    # 定义依赖关系，确保此迁移在指定的用户资料迁移之后执行
    dependencies = [
        ('accounts', '0004_userprofile_header_image'),
    ]

    # 当前迁移中执行的操作
    operations = [
        # 修改 UserProfile 模型中的 header_image 字段
        migrations.AlterField(
            model_name='userprofile',
            name='header_image',
            field=models.ImageField(
                upload_to='img',                    # 上传图片保存到 'img/' 目录
                max_length=100,                     # 文件名最大字符数
                blank=True,                         # 允许该字段为空
                null=True,                          # 允许该字段在数据库中为 null
                default='default.jpg',              # 默认图像为 'default.jpg'
                verbose_name='头像'                 # 管理界面中显示的字段名称
            ),
        ),
    ]
