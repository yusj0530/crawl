import time

from selenium import webdriver

wd = webdriver.Chrome('D:/Iot2018/chromedriver_win32/chromedriver.exe')
wd.get('http://www.google.com')
time.sleep(10)

html = wd.page_source
print(html)

wd.quit()