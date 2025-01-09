from django.shortcuts import render
import os
import csv
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.forms.models import model_to_dict
from django.http import JsonResponse
from selenium.webdriver.common.by import By

from .json_response import *
import pandas as pd
from .models import JDGoods, SearchKey, MyFollow
from .jd import *
# Create your views here.
#主页视图

# 首页视图
@login_required
def index(request):
    return render(request, "index.html", locals())


# 主页面视图
def main(request):
    return render(request, "main.html", locals())


# 从苏宁抓取数据的视图
def pa_suning(request):
    if request.method == 'POST':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 设置无头模式
        options.add_argument('--window-size=1920x1080')  # 设置窗口大小

        res = webdriver.Chrome(options=options)  # 使用指定的选项启动浏览器
        res.get('https://list.suning.com/')  # 打开苏宁商品列表页面
        search_box = res.find_element(By.ID, "searchKeywords")  # 查找搜索框
        search_box.send_keys(request.POST.get('key'), Keys.ENTER)  # 输入搜索关键字并回车

        # 下拉滚动页面以加载所有商品
        for _ in range(3):
            res.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            sleep(3)

        html = res.page_source  # 获取当前页面的HTML源码
        tree = etree.HTML(html)  # 解析HTML
        li_list = tree.xpath('//div[@id="product-list"]/ul/li')  # 找到所有商品的li元素
        list_all = []  # 存储所有商品信息

        # 遍历商品列表，提取信息
        for div in li_list:
            try:
                title = ''.join(
                    [x.strip() for x in div.xpath('.//div[@class="title-selling-point"]/a/text()') if x.strip() != ' '])
                price = ''.join(
                    [x.strip() for x in div.xpath('.//div[@class="price-box"]/span//text()') if x.strip() != ' '])
                ping = ''.join(
                    [x.strip() for x in div.xpath('.//div[@class="info-evaluate"]/a/i/text()') if x.strip() != ' '])
                dianpu = ''.join(
                    [x.strip() for x in div.xpath('.//div[@class="store-stock"]/a/text()') if x.strip() != ' '])
                links = ''.join(
                    [x.strip() for x in div.xpath('.//div[@class="title-selling-point"]/a/@href') if x.strip() != ' '])

                print(title, price, ping, dianpu, links)  # 输出提取的商品信息

                # 将商品信息保存到数据库
                JDGoods.objects.create(
                    jd_name=title,
                    jd_shop=dianpu,
                    jd_price=int(float(price.replace('¥', ''))),  # 去掉人民币符号并转为整型
                    jd_allcomment=ping.replace('+', ''),
                    jd_goodcomment=ping.replace('+', ''),
                    goods_url=links
                ).save()
                list_all.append(price)
            except Exception as e:
                print("Error occurred:", e)

        res.quit()  # 关闭浏览器
        return JsonResponse({'success': True, 'result': '已完成爬取内容：%s，成功插入 %d 条数据' % (
        request.POST.get('key'), len(list_all))})
    else:
        return render(request, 'crawl2.html')

# 商品推荐视图
def recommend(request):
    if request.method == 'POST':
        sort_key = request.POST.get('sort_key')
        # 根据排序键返回商品
        if sort_key == 'price':
            all_goods = JDGoods.objects.order_by('jd_price').values()
        elif sort_key == 'score':
            all_goods = JDGoods.objects.order_by('-jd_goodcomment').values()
        else:
            all_goods = JDGoods.objects.all().order_by('?').values()

        all_goods = list(all_goods)
        return JsonResponse({"code": 0, "all_goods": all_goods})
    else:
        all_goods = JDGoods.objects.all().order_by('?')[:10]
        # 为推荐商品构建数据
        for goods in all_goods:
            goods.goods_url = 'https://item.jd.com/' + goods.jd_id + '.html'  # 添加JD商品链接
        return render(request, "recommend.html", locals())


@login_required
def my(request):
    return render(request, "my.html", locals())

# 比价功能处理视图
@csrf_exempt
def bijia(request):
    if request.method == 'POST':
        # 从前端获取搜索数据
        search_data = json.loads(request.body.decode()).get('search_data', '')
        # 进行数据库比价搜索
        qs = JDGoods.objects.filter(jd_name__contains=str(search_data))
        price_goods = qs.order_by('-jd_price').values('jd_name', 'goods_url', 'jd_price', 'jd_shop')[:6]

        # 提取商品名称和价格
        price_x = [goods['jd_shop'] for goods in price_goods]
        price_y = [goods['jd_price'] for goods in price_goods]
        goods_list = list(price_goods)

        # 同上，获取各类商品的统计数据
        goodcomment_goods = qs.order_by('-jd_goodcomment').values('jd_name', 'goods_url', 'jd_goodcomment', 'jd_shop')[
                            :6]
        goodcomment_x = [goods['jd_shop'] for goods in goodcomment_goods]
        goodcomment_y = [goods['jd_goodcomment'] for goods in goodcomment_goods]
        goodcomment_list = list(goodcomment_goods)

        price_min_goods = qs.order_by('jd_price').values('jd_name', 'goods_url', 'jd_price', 'jd_shop')[:6]
        price_min_x = [goods['jd_shop'] for goods in price_min_goods]
        price_min_y = [goods['jd_price'] for goods in price_min_goods]
        price_min_list = list(price_min_goods)

        good_goods = qs.order_by('-jd_goodcomment').values('jd_name', 'goods_url', 'jd_goodcomment', 'jd_shop')[:6]
        good_goods_x = [goods['jd_shop'] for goods in good_goods]
        good_goods_y = [goods['jd_goodcomment'] for goods in good_goods]
        good_goods_list = list(good_goods)

        bad_goods = qs.order_by('-jd_poorcomment').values('jd_name', 'goods_url', 'jd_poorcomment', 'jd_shop')[:6]
        bad_goods_x = [goods['jd_shop'] for goods in bad_goods]
        bad_goods_y = [goods['jd_poorcomment'] for goods in bad_goods]
        bad_goods_list = list(bad_goods)

        # 构造结果字典
        result = {
            'price_goods': goods_list,
            'price_x': price_x,
            'price_y': price_y,
            'goodcomment_goods': goodcomment_list,
            'goodcomment_x': goodcomment_x,
            'goodcomment_y': goodcomment_y,
            'price_min_goods': price_min_list,
            'price_min_x': price_min_x,
            'price_min_y': price_min_y,
            'good_goods': good_goods_list,
            'good_goods_x': good_goods_x,
            'good_goods_y': good_goods_y,
            'bad_goods': bad_goods_list,
            'bad_goods_x': bad_goods_x,
            'bad_goods_y': bad_goods_y
        }
        return JsonResponse(result)
    else:
        # 默认返回一些商品的初始数据
        price_goods = JDGoods.objects.filter().order_by('-jd_price')[:6]
        price_x = [good.jd_shop for good in price_goods]
        price_y = [good.jd_price for good in price_goods]

        goodcomment_goods = JDGoods.objects.filter().order_by('-jd_goodcomment')[:6]
        goodcomment_x = [good.jd_shop for good in goodcomment_goods]
        goodcomment_y = [good.jd_goodcomment for good in goodcomment_goods]

        price_goods2 = JDGoods.objects.filter().order_by('jd_price')[:6]
        price_min_x = [good.jd_shop for good in price_goods2]
        price_min_y = [good.jd_price for good in price_goods2]

        good_goods = JDGoods.objects.filter().order_by('-jd_goodcomment')[:6]
        good_goods_x = [good.jd_shop for good in good_goods]
        good_goods_y = [good.jd_goodcomment for good in good_goods]

        bad_goods = JDGoods.objects.filter().order_by('-jd_poorcomment')[:6]
        bad_goods_x = [good.jd_shop for good in bad_goods]
        bad_goods_y = [good.jd_poorcomment for good in bad_goods]

        return render(request, "bijia.html", locals())


@login_required
def follow(request):
    user = request.user
    all_goods = []
    follow_goods = MyFollow.objects.filter(user=user).select_related('good')  # 预取关注的商品
    for good in follow_goods:
        all_goods.append(good.good)
    return render(request, "follow.html", {'all_goods': all_goods})


def js_menu(request):
    return success_no_wrapper(settings.JS_MENU)


def js_config(request):
    return success_no_wrapper(settings.JS_CONFIG)


def get_product(request):
    page = int(request.GET.get("page", "0"))  # 获取当前页码，默认值为 0
    limit = int(request.GET.get("limit", "10"))  # 获取每页显示条数，默认值为 10
    key = request.GET.get("key", "")  # 获取搜索关键字
    all_goods = JDGoods.objects.all()

    if key:
        all_goods = all_goods.filter(jd_name__icontains=key)  # 根据关键字过滤商品

    all_goods_page = all_goods[(page - 1) * limit: page * limit]  # 分页查询
    last = [model_to_dict(good) for good in all_goods_page]  # 转换为字典列表

    return success_by_count(last, str(all_goods.count()))  # 返回数据及总数


@login_required
@csrf_exempt
def go_follow(request):
    datas = json.loads(request.body)  # 解析请求体
    user = request.user
    gid = datas["gid"]  # 商品ID

    good = JDGoods.objects.filter(id=gid).first()  # 查询商品
    if not good:
        return error("商品已不存在")

    myFollow, created = MyFollow.objects.get_or_create(user=user, good=good)  # 创建关注记录
    if not created:
        return error("您已经关注过了")  # 如果已存在记录

    return success("成功！")


@login_required
@csrf_exempt
def go_unfollow(request):
    datas = json.loads(request.body)
    user = request.user
    gid = datas["gid"]

    good = JDGoods.objects.filter(id=gid).first()
    if not good:
        return error("商品已不存在")

    myFollow = MyFollow.objects.filter(user=user, good=good)
    if myFollow.exists():
        myFollow.delete()  # 删除关注记录
        return success("成功！")
    else:
        return error("没有关注商品")


@login_required
@csrf_exempt
def search(request):
    search_word = request.POST.get("search_word", "")  # 从请求中获取搜索词
    JDGoods.objects.filter(jd_name__icontains=search_word)  # 模糊搜索商品名称
    return render(request, "index.html")


def start(request):
    if request.method == 'POST':  # 如果请求方式是 POST
        key = request.POST.get('key', None)  # 获取商品关键字
        all_good = jingdong_spider(key)  # 调用爬虫函数获取商品信息
        count = 0  # 统计成功插入的商品数量

        for good in all_good:
            if len(good) != 9:  # 跳过格式不正确的商品
                continue

            # 如果商品ID存在则更新，否则创建新的商品
            db_good, created = JDGoods.objects.get_or_create(jd_id=good[0])
            db_good.jd_name = good[1]
            db_good.jd_shop = good[2]

            try:
                db_good.jd_price = float(good[3])  # 转换价格为浮点数
            except ValueError:
                db_good.jd_price = 0.0  # 默认价格为0

            # 处理商品评论数量的字符串格式
            try:
                db_good.jd_allcomment = int(''.join(filter(str.isdigit, good[4])) or '0')
                db_good.jd_goodcomment = int(''.join(filter(str.isdigit, good[5])) or '0')
                db_good.jd_generalcomment = int(good[6].replace("+", ""))
                db_good.jd_poorcomment = int(good[7].replace("+", ""))
            except Exception as e:
                print(f"Error processing comments: {e}")
                db_good.jd_allcomment = db_good.jd_goodcomment = db_good.jd_generalcomment = db_good.jd_poorcomment = 0

            db_good.goods_url = good[8]  # 商品链接
            db_good.save()  # 保存到数据库
            count += 1  # 更新成功插入计数

        return JsonResponse({'success': True, 'result': '已完成爬取内容：%s，成功插入 %d 条数据' % (key, count)})
    else:  # 处理GET请求
        return render(request, 'crawl.html')


def get_goods_data(keyword):
    goods_list = []  # 存储抓取的商品数据
    headers = {
        # 模拟浏览器请求的请求头
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    # 从京东获取商品数据
    jd_url = f'https://search.jd.com/Search?keyword={keyword}&enc=utf-8'  # 准备请求链接
    res = requests.get(jd_url, headers=headers)  # 发起请求
    soup = BeautifulSoup(res.text, 'html.parser')  # 解析HTML
    jd_goods_list = soup.select('.gl-item')  # CSS选择获取商品信息

    for jd_goods in jd_goods_list:
        goods = JDGoods()  # 实例化商品对象
        goods.jd_name = jd_goods.select_one('.p-name a em').text.strip()  # 商品名称
        goods.jd_price = jd_goods.select_one('.p-price strong i').text.strip()  # 商品价格
        goods.jd_shop = jd_goods.select_one('.p-shop span a').text.strip()  # 店铺名称
        goods.goods_url = f'https://item.jd.com/{jd_goods.attrs["data-sku"]}.html'  # 商品链接
        goods_list.append(goods)  # 添加到商品列表

    return goods_list  # 返回商品列表


def search_3(request):
    keyword = request.GET.get('keyword', '')  # 从请求参数获取关键字
    goods_list = get_goods_data(keyword)  # 获取商品数据

    for goods in goods_list:
        goods.save()  # 保存商品到数据库

    return JsonResponse({'成功': [goods.to_dict() for goods in goods_list]})  # 返回成功消息和商品数据