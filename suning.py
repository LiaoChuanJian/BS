from lxml import etree
from time import sleep
from selenium import webdriver
import csv
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# 初始化 Chrome 浏览器
res = webdriver.Chrome()

# 打开苏宁易购首页
res.get('https://list.suning.com/')

# 找到搜索框并输入 '智能手表'，模拟按下回车键
search_box = res.find_element(By.ID, "searchKeywords")
search_box.send_keys("智能手环", Keys.ENTER)

# 定义滑动页面的 JavaScript 代码
js = 'window.scrollTo(0, document.body.scrollHeight)'

# 循环滑动页面，以加载更多内容
for _ in range(3):
    res.execute_script(js)  # 执行滑动
    sleep(3)  # 等待页面加载

# 获取当前页面的 HTML 源代码
html = res.page_source

# 使用 lxml 解析 HTML
tree = etree.HTML(html)

# 使用 XPath 表达式找到商品列表
li_list = tree.xpath('//div[@id="product-list"]/ul/li')

# 存储所有商品信息的列表
list_all = []

# 遍历每个商品信息
for div in li_list:
    try:
        # 获取商品名称
        title = ''.join(
            [x.strip() for x in div.xpath('.//div[@class="title-selling-point"]/a/text()') if x.strip() != ' '])

        # 获取价格
        price = ''.join([x.strip() for x in div.xpath('.//div[@class="price-box"]/span//text()') if x.strip() != ' '])

        # 获取评论数
        ping = ''.join([x.strip() for x in div.xpath('.//div[@class="info-evaluate"]/a/i/text()') if x.strip() != ' '])

        # 获取店铺名
        dianpu = ''.join([x.strip() for x in div.xpath('.//div[@class="store-stock"]/a/text()') if x.strip() != ' '])

        # 获取产品链接
        links = ''.join(
            [x.strip() for x in div.xpath('.//div[@class="title-selling-point"]/a/@href') if x.strip() != ' '])

        # 打印获取到的信息
        print(f"名称: {title}")
        print(f"价格: {price}")
        print(f"评论数: {ping}")
        print(f"店铺名: {dianpu}")
        print(f"链接: {links}\n")

        # 将信息添加到列表中
        list_all.append({
            "title": title,
            "price": price,
            "ping": ping,
            "dianpu": dianpu,
            "links": links
        })
    except Exception as e:
        print(f'爬取商品时发生错误: {e}')

# 退出浏览器
res.quit()
