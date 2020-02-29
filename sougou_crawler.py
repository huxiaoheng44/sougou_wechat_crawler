from selenium import webdriver
import time
#初始化
#需要下载和浏览器匹配的driver文件，并且填写好路径
chrome_driver=r"D:\chromedriver.exe"
browser=webdriver.Chrome(executable_path=chrome_driver)
url = 'https://weixin.sogou.com/weixin'
#关键词
keyword = "关键词"
page_num = 5
url2mes = {}

def open_url(url):
    browser.get(url)  # 打开浏览器预设网址
    time.sleep(0.5)

#写这个纯粹是为了节省下后面的代码量
def get_element(s):
    ele = browser.find_element_by_css_selector(s)
    time.sleep(0.5)
    return ele;

def get_elements(s):
    eles = browser.find_elements_by_css_selector(s)
    time.sleep(0.5)
    return eles;

def write_mes_txt(keyword):
    file_name = keyword+".txt"
    with open(file_name,"a") as f:
        for url in url2mes.keys():
            f.write(url+"\n")
            try:
                l = url2mes[url]
                m = "出处："+l[0]+"   时间："+l[1]+"\n"
                f.write(m)
            except:
                f.write("暂无其他相关信息\n")

#关闭除了关键页面的其他页面，同时提取需要的信息
def clear_urls(current_handle):
    for handle in browser.window_handles:
        if handle == current_handle:
            continue
        else:
            try:
                browser.switch_to.window(handle)
                author = browser.find_element_by_css_selector("#js_name").text
                publish_time = browser.find_element_by_css_selector("#publish_time").text
                url = browser.current_url
                url2mes[str(url)] = [author,publish_time]
                print(url+"\n"+author,publish_time)
                browser.close()
            except:
                print("获取不到页面信息" + url)
                browser.close()
open_url(url)
input = get_element("#query")
input.send_keys(keyword)
search_button = get_element("[uigs=search_article]")
search_button.click()

current_page = 1

while(current_page<=page_num):
    target_boxes = get_elements(".txt-box")
    current_handle = browser.current_window_handle
    # 打开这一页的全部页面
    for target_box in target_boxes:
        link = target_box.find_element_by_css_selector("[target=_blank]")
        link.click()

    clear_urls(current_handle)
    #进入下一页
    browser.switch_to.window(current_handle)
    current_page +=1
    try:
        next_page = browser.find_element_by_css_selector("#sogou_next")
        next_page.click()
    except:
        print("已无下一页")
        break

print(len(url2mes))
write_mes_txt(keyword)

#最后关闭整个webdriver，不关闭的话会一直在后台运行
time.sleep(10)
browser.quit()


