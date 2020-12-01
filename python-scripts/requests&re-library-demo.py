import requests
import re


def try_url(id_):
    url = 'http://photo.uestc.edu.cn/index/detail?cateId=7&pictureId=' + str(id_) + '&referrer=52dc0196f424c4d45258' \
                                                                                'a3bde21700c0'
           # url信息
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/73.0.3683.86 Safari/537.36'}
           # http头信息
    try:
        r = requests.get(url, headers=headers) # 用get方式请求网站信息
        r.raise_for_status() # 通过.raise_for_status() 来抛出异常，如果异常，则尝试失败，跳转except
        r.encoding = r.apparent_encoding # 将编码方式更改为 “从内容分析出的编码方式”
        print(r.text) # 打印response信息
        return r.text # 返回response信息
    except requests.HTTPError:
        print(requests.HTTPError) # 若抛出异常，则打印异常信息


def get_real_url(html):
    result = re.search('pic-show.*?\'(.*?)\'.*?', html, re.S) # 在html信息中寻找"pic-show.*?\'(.*?)\'.*?"
    if result is None: # 如果没有找到，则返回0
        return 0
    real_url = result.group(1) # 找到了则返回相关信息
    return real_url


def get_pic(real_url, number):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/73.0.3683.86 Safari/537.36'}
    real_url_ = 'http://photo.uestc.edu.cn' + str(real_url)
    try:
        pic = requests.get(real_url_, headers=headers) # 用get方式请求网站信息
        pic.raise_for_status() # 通过.raise_for_status() 来抛出异常，如果异常，则尝试失败，跳转except
        write_(pic.content, number) #  write_函数
    except requests.HTTPError:
        print(requests.HTTPError) # 若抛出异常，则打印异常信息


def write_(content, number):
    file_path = 'pic/{}.jpg'.format(number) # 保存的文件名
    with open(file_path, 'wb') as f: # 保存文件
        f.write(content)
    print('{}complete!'.format(number)) # 打印提示信息


def main(number): 
    html = try_url(number) # 返回相应的t.test，即http的response
    real_url = get_real_url(html) # 寻找图片的地址
    if not real_url == 0:
        get_pic(real_url, number) # 保存图片
    else:
        print('{}failed!'.format(number))


if __name__ == '__main__':
    main(38) # 程序从这里开始
    # main(num) -> |  try_url(num)       return 请求信息
    #         	   |  get_real_url(html) return 图片的地址
    #              |  get_pic(real_url, number) -> |  requests.get(real_url_, headers=headers) 请求网站信息
    #                                              |  write_(content, number) 保存文件

