from selenium import webdriver
import time
# http://chromedriver.chromium.org/
item_list = [('ZHG5630000', 6), ('LSFY210002', 1)]


def launch():
    browser = webdriver.Chrome()
    browser.get('http://elc.vipsale.cn/Shop/Product.aspx')
    return browser


def login(browser):
    browser.find_element_by_id('txtUserID').send_keys('elcfin129')
    browser.find_element_by_id('txtPwd').send_keys('571262')
    check_code = input('输入验证码:')
    browser.find_element_by_id('txtVerify').send_keys(check_code)
    browser.find_element_by_id('btnSignIn').click()
    time.sleep(5)
    browser.find_element_by_id('allow').click()


def try_to_buy(browser):
    for item in item_list:
        sku = item[0]
        want_qty = item[1]
        # 输入数量检索
        browser.find_element_by_id('txtSearch').clear()
        browser.find_element_by_id('txtSearch').send_keys(sku)
        browser.find_element_by_id('btnSearch').click()
        time.sleep(1)
        while True:
            alert_text = ''
            # 获取库存
            qty = browser.find_element_by_xpath(f'//*[@id="{sku}"]/table/tbody/tr[2]/td[1]').text
            print(f"{sku}数量:{qty}")
            qty = int(qty)
            if qty > 0:
                order_count = browser.find_element_by_xpath(f'//*[@id="{sku}"]/table/tbody/tr[2]/td[2]/input')
                order_count.clear()
                if want_qty > qty:
                    want_qty = qty
                order_count.send_keys(want_qty)
                # 点击 加入购物车
                browser.find_element_by_xpath(f'//*[@id="{sku}"]/table/tbody/tr[3]/td/input').click()
                for i in range(5):
                    try:
                        alert = browser.switch_to_alert()
                        alert_text = alert.text
                        print(alert.text)
                        alert.accept()
                        break
                    except Exception as e:
                        time.sleep(0.1)
            if alert_text != '本次内卖尚未开始，敬请期待!':
                break
            time.sleep(1)


if __name__ == '__main__':
    _browser = launch()
    login(_browser)
    input('等待... 按回车继续.')
    try_to_buy(_browser)
