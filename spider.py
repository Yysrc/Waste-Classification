import requests
import re
import time
import csv

comments_ID = []


# 爬取该主题首页每个博文的ID，以便接下来打开每个网页，找到具体的内容。因为对于简单的博文，可能在首页就能显示全部内容，但大多数都是要打开才能看到具体内容的。
def get_title_id():
    Headers = {
        'Cookie': "SINAGLOBAL=2508429828824.155.1697468141541; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWFPIZXJbnaAkwHJ35Q_CPv5JpX5KMhUgL.FoMRe0nEe02cShz2dJLoIpXLxKBLBo.L1KLki--Xi-z4iK.4PEH8SFHF1C-41Btt; _s_tentry=www.weibo.com; Apache=952833484829.9602.1702908507661; ULV=1702908507705:8:2:1:952833484829.9602.1702908507661:1701827172366; SCF=AowP0yD3U1FLWpeyt483ACrwA181BUL9s2D7CdQ2voknpLcxrvP-lb4DYC2YhHZIan96KXg808kELT336ISw-c0.; SUB=_2A25IhCl-DeRhGeFG6FoT8y_Kzz6IHXVr-CS2rDV8PUNbmtANLXLYkW9NebAaKVjCymQKffwuc8JPf-RFbQIKtRau; ALF=1705502253; SSOLoginState=1702910254; PC_TOKEN=ae8514427b",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        'Referer': "https://s.weibo.com/"
    }

    for Page in range(1, 40):  # 每个页面大约有10个话题
        time.sleep(1)

        # 该链接通过抓包获得
        remark_url = "https://s.weibo.com/weibo?q=%23%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%23&page=" + str(
            Page)
        response = requests.get(url=remark_url, headers=Headers)
        try:
            text = response.text
            # 与mid进行匹配
            comment_ID = re.findall('(?<=mid=")\d{16}', text)
            # 把新找到的一个ID加入到列表中
            comments_ID.extend(comment_ID)
        except:
            print(Page, "页id获取有误!")
    print(comments_ID)


# 爬取该主题下每个博文的详细内容
def spider_title(comment_ID):
    Headers = {
        'Cookie': "_T_WM=8bf931cbdc6618736bb5702173a25e1e; WEIBOCN_FROM=1110006030; SCF=AowP0yD3U1FLWpeyt483ACrwA181BUL9s2D7CdQ2voknpLcxrvP-lb4DYC2YhHZIatCWMYNhjyoW-5S_ItRdKJM.; SUB=_2A25IhCl-DeRhGeFG6FoT8y_Kzz6IHXVr-CS2rDV6PUNbktANLW7ykW1NebAaKTTG468vmR6d_XYEYi3HGQBGhdv1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWFPIZXJbnaAkwHJ35Q_CPv5JpX5KMhUgL.FoMRe0nEe02cShz2dJLoIpXLxKBLBo.L1KLki--Xi-z4iK.4PEH8SFHF1C-41Btt; SSOLoginState=1702910254; ALF=1705502254; MLOGIN=1; XSRF-TOKEN=696bb5; mweibo_short_token=2becc82345; M_WEIBOCN_PARAMS=oid%3D4980405986134377%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%2523%25E5%259E%2583%25E5%259C%25BE%25E5%2588%2586%25E7%25B1%25BB%2523%26fid%3D100103type%253D1%2526q%253D%2523%25E5%259E%2583%25E5%259C%25BE%25E5%2588%2586%25E7%25B1%25BB%2523%26uicode%3D10000011",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        'Referer': "https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%23%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%23"
    }

    article_url = 'https://m.weibo.cn/detail/' + comment_ID
    print("article_url = ", article_url)
    time.sleep(1)

    try:
        html_text = requests.get(url=article_url, headers=Headers).text
        # 楼主ID
        title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]
        # 楼主昵称
        title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]
        # 楼主性别
        title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]
        # 话题内容
        find_title = re.findall('.*?"text": "(.*?)",.*?', html_text)[0]
        title_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', find_title)  # 正则匹配掉html标签
        # position是记录
        position = (title_user_id, title_user_NicName, title_user_gender, title_text)

        # 写入数据
        writer.writerow((position))
        print('写入博文信息数据成功！')

    except:
        print('博文网页解析错误，或微博不存在或暂无查看权限！')
        pass


# 存取的是微博博文的信息（不包含评论）
path = 'D:/Desktop/垃圾分类/content.csv'
# 如果没有，就新建一个excel文件
csvfile = open(path, 'a', newline='', encoding='utf-8-sig')
writer = csv.writer(csvfile)

# 只爬取微博特定话题下相关博文的信息
writer.writerow(('楼主ID', '楼主昵称', '楼主性别', '话题内容'))
get_title_id()
for comment_ID in comments_ID:
    spider_title(comment_ID)

