from django.contrib import admin
from .models import JDGoods
# Register your models here.
from django.contrib.auth.hashers import make_password

class JDGoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'jd_id','jd_name','jd_shop','jd_price')
    search_fields = ('jd_id','jd_name','jd_shop')
admin.site.register(JDGoods, JDGoodsAdmin)
admin.site.site_title = "后台管理系统"
admin.site.site_header = "后台管理系统"