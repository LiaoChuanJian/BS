import os
import requests
from bs4 import BeautifulSoup
import re
import os

def gethttptext(url):
    try:

        kv = {
            # cookie需换成自己的
            'cookie': '__jdv=76161171|www.bing.com|-|referral|-|1736435001165; __jdu=17364350011641735523862; PCSYCityID=CN_810000_811000_0; areaId=52993; ipLoc-djd=52993-52994-0-0; shshshfpa=dcb9a0b4-68cf-123d-5020-c71af0f26eda-1736435007; shshshfpx=dcb9a0b4-68cf-123d-5020-c71af0f26eda-1736435007; shshshfpb=BApXSOhafSPFATw6kmoj8ieLprm1LNN8ABnQCVyho9xJ1MoPeYoG2; __jda=95931165.17364350011641735523862.1736435001.1736435001.1736435001.1; __jdc=95931165; wlfstk_smdl=zsaf97unxzopxz9txf6tciidrs2fqr0p; pinId=WyP8a91jpalKTqCWenyQIg; pin=jd_pGIluJTuuXrP; unick=jd_202nk8u9t2k996; ceshi3.com=000; _tp=kW%2B3TUWkc%2BI8F%2Fl39GFbRg%3D%3D; mba_muid=17364350011641735523862; mba_sid=17364351450795237255702635069.0; o2State=; 3AB9D23F7A4B3CSS=jdd03EVK7PAEGU5BKW2CCLD4GYFDBBSU7V2E5C7GV7N7G3XWXBNLFMRPUE43K36NAB4BXYWCGFX64RCLYFW3LLNHZSYKYHMAAAAMUJOMZVPYAAAAACDCN7GPCIHSVJYX; __jdb=95931165.6.17364350011641735523862|1.1736435001; 3AB9D23F7A4B3C9B=EVK7PAEGU5BKW2CCLD4GYFDBBSU7V2E5C7GV7N7G3XWXBNLFMRPUE43K36NAB4BXYWCGFX64RCLYFW3LLNHZSYKYHM',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print("提取失败", e)
        return ""


# 爬取京东中商品数据
def jingdong_spider(item_name):
    item_list = []
    for i in range(0,4):

        # 列表存储ID,标题,价格,图片url
        # item_list = []
        if i == 0:
            url = "https://search.jd.com/Search?keyword=" + item_name + "&qrst=1&stock=1&pvid=d038ffe9573b4bf58a4ea5ed68450047&page=" + str(
                2 * i + 1) + "&click=0"
        else:
            url = "https://search.jd.com/Search?keyword=" + item_name + "&qrst=1&stock=1&pvid=d038ffe9573b4bf58a4ea5ed68450047&page=" + str(
                2 * i + 1) + "&s=" + str(60 * (i - 1) + 56) + "&click=0"

        page_html = gethttptext(url)

        # 直接提取
        soup = BeautifulSoup(page_html, 'html.parser')

        data_list = soup.findAll(name="li", attrs={"class": "gl-item"})

        for item in data_list:

            item = str(item).replace('\n', '')

            # print(item)

            # 使用正则表达式提取ID
            jd_id = re.findall(r'strong class="J_(.+?)" ', item)

            jd_id = jd_id[0]
            # print(jd_id)
            goods_url = "https://item.jd.com/" + str(jd_id) + ".html"
            goods_html = gethttptext(goods_url)
            goods_soup = BeautifulSoup(goods_html, 'html.parser')
            goods_item = str(goods_soup).replace('\n', '')
            print(jd_id)
            jd_name = re.findall(r'<div class="sku-name"' + '(.+?)' + '</div>', goods_item)
            if jd_name:
                if jd_name[0]:
                    if '</img>' in jd_name[0]:
                        jd_name = re.findall(r'">' + '(.+?)' + '</img>', jd_name[0])[0].strip()
                    else:
                        jd_name = re.findall(r'>(.+)', jd_name[0])[0].strip()
                else:
                    jd_name = ''
            else:
                jd_name = ''
            # 使用正则表达式提取价格
            jd_price = re.findall(r'data-price="' + jd_id + r'".*?>(.+?)</i>', item)[0]

            # 提取店铺名
            jd_shop = re.findall(r'<div class="p-shop"' + '(.+?)' + '</div>', item)[0]
            try:
                jd_shop = re.findall(r'title="(.+?)">', jd_shop)[0]
            except:
                pass

            # print(jd_shop)
            # 提取评价数
            comment_url = "https://club.jd.com/comment/productCommentSummaries.action?" + "referenceIds=" + str(jd_id)
            comment_html = gethttptext(comment_url)
            comment_soup = BeautifulSoup(comment_html, 'html.parser')
            comment_soup = str(comment_soup).replace('\n', '')
            # 总评
            jd_allcomment = re.findall(r'"CommentCountStr":"' + '(.+?)' + '"', comment_soup)[0].replace('Íò', '万')

            # 好评
            jd_goodcomment = re.findall(r'"GoodCountStr":"' + '(.+?)' + '"', comment_soup)[0].replace('Íò', '万')

            # 中评
            jd_generalcomment = re.findall(r'"GeneralCountStr":"' + '(.+?)' + '"', comment_soup)[0].replace('Íò', '万')

            # 差评
            jd_poorcomment = re.findall(r'"PoorCountStr":"' + '(.+?)' + '"', comment_soup)[0].replace('Íò', '万')

            res = [jd_id, jd_name, jd_shop, jd_price, jd_allcomment, jd_goodcomment, jd_generalcomment, jd_poorcomment,
                   goods_url]
            item_list.append(res)
            print(res)
    return item_list


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 从京东爬取商品函数
    jingdong_spider("电脑")
