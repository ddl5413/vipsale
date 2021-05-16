from selenium import webdriver
import json
import time
import datetime
# http://chromedriver.chromium.org/
option = {}


def launch():
    browser = webdriver.Chrome()
    browser.get('http://elc.vipsale.cn/Shop/Product.aspx')
    return browser


def login(browser):
    user = option['user']
    browser.find_element_by_id('txtUserID').send_keys(user['account'])
    browser.find_element_by_id('txtPwd').send_keys(user['password'])
    check_code = input('输入验证码:')
    browser.find_element_by_id('txtVerify').send_keys(check_code)
    browser.find_element_by_id('btnSignIn').click()
    time.sleep(5)
    browser.find_element_by_id('allow').click()


def try_to_buy(browser):
    item_list = []
    for item in option['items']:
        item_list.append((item['sku'], item['want']))
    # 购买列表非空时无限循环
    while len(item_list) > 0:
        now = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"{now}: 本次循环商品: {item_list}")
        # 没有买够数量的商品列表
        item_list_sub = []
        for item in item_list:
            success = False
            while not success:
                try:
                    # 输入数量检索
                    browser.find_element_by_id('txtSearch').clear()
                    browser.find_element_by_id('txtSearch').send_keys(item[0])
                    browser.find_element_by_id('btnSearch').click()
                    time.sleep(1)
                    want = buy_item(browser, item)
                    if want > 0:
                        item_list_sub.append((item[0], want))
                    success = True
                except Exception as e:
                    print(e)
                    success = False
                    time.sleep(1)
        item_list = item_list_sub


def buy_item(browser, item):
    sku = item[0]
    want = item[1]
    while True:
        qty = browser.find_element_by_xpath(f'//*[@id="{sku}"]/table/tbody/tr[2]/td[1]').text
        print(f"商品: {sku}, 库存: {qty}")
        qty = int(qty)
        if qty > 0:
            # 输入购买数量
            order_count = browser.find_element_by_xpath(f'//*[@id="{sku}"]/table/tbody/tr[2]/td[2]/input')
            order_count.clear()
            buy = min(qty, want)
            order_count.send_keys(buy)
            # 点击 加入购物车
            browser.find_element_by_xpath(f'//*[@id="{sku}"]/table/tbody/tr[3]/td/input').click()
            alert_text = dismiss_alert(browser)
            if alert_text == '本次内卖尚未开始，敬请期待!':
                time.sleep(1)
                continue
            elif alert_text == '产品订购成功':
                print(f'成功购买商品{sku}, {buy}件')
                # 返回未能满足的求购数量
                return want - buy
            else:
                print(f'商品{sku}存在问题，放弃购买')
                return 0
        else:
            return want


def dismiss_alert(browser):
    alert_text = ''
    for i in range(5):
        try:
            alert = browser.switch_to.alert
            alert_text = alert.text
            print(f"alert:{alert.text}")
            alert.accept()
            break
        except Exception as e:
            time.sleep(0.1)
    return alert_text


def load_config():
    global option
    with open("config.json") as config_file:
        option = json.load(config_file)['option']


if __name__ == '__main__':
    try:
        _browser = launch()
        load_config()
        login(_browser)
        input('等待... 按回车继续.')
        try_to_buy(_browser)
    finally:
        input('购买完成... 按回车继续.')
        _browser.close()
