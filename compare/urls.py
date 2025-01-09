from django.conf.urls import url
from django.urls import path, re_path
from .views import *
from compare import views

urlpatterns = [

    url(r"^$", index, name="index"),
    url(r"^main$", main, name="main"),
    url(r"index/", index, name="index"),

    path(r"js_menu", js_menu, name="js_menu"),
    path(r"js_config", js_config, name="js_config"),
    path(r"get_product", get_product, name="get_product"),
    path(r"recommend", recommend, name="recommend"),
    #path(r"bijia", bijia, name="bijia"),
    path(r"follow", follow, name="follow"),
    path(r"my", my, name="my"),
    path(r"start", start, name="start"),
    path(r"pa_suning", pa_suning, name="pa_suning"),
    path(r"go_follow", go_follow, name="go_follow"),
    path(r"go_unfollow", go_unfollow, name="go_unfollow"),
    path(r'crawl/', views.start, name='crawl'),

# 清空compare_jdgoods表中的所有数据
    path(r'search_2/', views.search_3, name='search_2'),
    path(r"bijia/", views.bijia, name="bijia"),

]
