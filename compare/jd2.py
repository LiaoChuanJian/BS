from selenium import webdriver
import time

def main_jd(pname):
    products = []  # 用于存储提取的商品信息
    count = 0  # 当前页数计数
    url = "http://www.jd.com/"  # 京东首页 URL
    driver = webdriver.Chrome()  # 创建 Chrome 浏览器实例

    def search_product(key):  # 向搜索框输入内容
        search_box = driver.find_element_by_id('key')  # 获取搜索框元素
        search_box.send_keys(key)  # 输入搜索关键字

    def click_search():  # 点击搜索按钮
        search_button = driver.find_element_by_class_name('button')  # 获取搜索按钮元素
        search_button.click()  # 点击搜索按钮

    def get_page_number():  # 获取总的页数
        try:
            pagenum_text = driver.find_element_by_class_name('p-skip').text  # 获取页面跳转文本
            return int(pagenum_text.split("/")[1].strip())  # 提取总页数
        except Exception as e:
            print("获取页数时出现错误:", e)
            return 0  # 如果出现错误，返回 0 页

    def page_next():  # 翻到下一页
        next_button = driver.find_element_by_class_name('pn-next')  # 获取下一页按钮元素
        next_button.click()  # 点击下一页按钮

    driver.get(url)  # 打开京东首页
    driver.maximize_window()  # 最大化浏览器窗口
    search_product(pname)  # 搜索产品
    click_search()  # 点击搜索按钮
    time.sleep(3)  # 等待页面加载完成
    driver.execute_script("window.scrollBy(0, 8000)")  # 下拉滚动条，以便加载所有商品信息
    time.sleep(1)

    # 循环获取商品信息，直到达到最大页数
    while count < get_page_number():
        products_info = driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]')  # 获取商品信息元素
        for div in products_info:
            try:
                # 提取商品名称、价格、店铺名称和评论
                name = div.find_element_by_xpath('.//div[@class="p-name p-name-type-2"]')
                price = div.find_element_by_xpath('.//div[@class="p-price"]//i')
                shop = div.find_element_by_xpath('.//div[@class="p-shop"]')
                commit = div.find_element_by_xpath('.//div[@class="p-commit"]//a')

                products.append((name.text, price.text, shop.text, commit.text))  # 将信息添加到列表
            except Exception as e:
                print("提取过程中出现错误:", e)

        pagenum = count + 1
        print('第' + str(pagenum) + '页已提取')
        page_next()  # 翻到下一页

        time.sleep(3)  # 等待页面加载
        driver.execute_script("window.scrollBy(0, 8000)")  # 下拉滚动条
        time.sleep(1)
        count += 1  # 增加页数计数

        if count == 5:  # 限制最大提取页数为5
            break

    driver.quit()  # 关闭浏览器
    return products  # 返回提取的商品信息
