#2020.8.22  糗事百科爬虫
#焦康阳  个人博客:https://jiaokangyang.com
#功能：本次爬虫主要完成对糗事百科的段子爬取


import requests
from pyquery import PyQuery as pq

#先写一个函数进行网页内容爬取,并返回内容
def download_qiushi(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400',

    }
    a = requests.get(url,headers=headers)
    return a.text

#该函数完成对网页内容分析，下载

def get_content(html,page):
    #这块预先设置一个字符串，等会将获取到内容利用format方法填充到里面
    shuchu = """第{}页 作者：{} 性别：{} 年龄：{} 喜欢：{} 评论：{}  \n原文链接：{}\n\n{}\n-----------------\n"""

    url = 'https://www.qiushibaike.com'

    a = pq(html)
    lists = a('.article').items()

    for list in lists:
        #获取作者名字
        author = list('.author a h2').text()
        #获取内容
        content = list('.content span').text()
        #喜欢的人数
        vote = list('.stats .stats-vote .number').text()
        #获取评论数
        comments =  list('.stats .stats-comments .number').text()

        #原文链接
        href = url + str(list('.contentHerf').attr('href'))
        #获取作者的年龄和性别
        author_info = list('.articleGender')
        if author_info is not None:  #这块判断是否为匿名用户
            class_list = author_info.attr('class')  #获取class属性，然后对比是否为男女属性
            if 'womenIcon' in class_list:  #网页源码中女性用的是womenIcon 样式，我们只需对比
                gender = '女'
            elif 'manIcon' in class_list:
                gender = '男'
            else:
                gender = ''

            age = author_info.text()  #获取作者年龄
        else:    #如果没有的话就给性别年龄赋值为空
            gender = ''
            age = ''

        #将获取到内容用format方法填充,并将内容保存到文件
        save_txt(shuchu.format(page,author,gender,age,vote,comments,href,content))

#此方法将文件保存到qiushi,txt文件中
def save_txt(*args):
    for i in args:
        with open('qiushi.txt','a',encoding='utf-8') as f:
            f.write(i)


def main():
    #内容较多，我们设置爬取前三页的内容
    for i in range(1,4):
        url = 'https://qiushibaike.com/text/page{}'.format(i)
        print('开始爬取第%d页'%i)
        html = download_qiushi(url)
        get_content(html, i)
        print('爬取完成')

    print('所有内容爬取完毕，请打开文件查看')

if __name__ == '__main__':
    main()

