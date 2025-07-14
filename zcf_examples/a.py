import requests
import json
import os
from datetime import datetime

from bs4 import BeautifulSoup
import re

# 参考链接:
#   https://zhuanlan.zhihu.com/p/117569614
#   https://blog.csdn.net/weixin_42914706/article/details/129112667
# pyinstaller --onefile --name=获取哔哩哔哩视频目录信息 D:\knowledge\python_reptile\python_reptile_scrapy\GetVideoCatalog.py

def print_directory(data):
    print("开始解析页面内容...")
    print(f"页面内容长度: {len(data)} 字符")
    
    # 检查是否包含B站特征
    if "bilibili" not in data.lower():
        print("警告: 页面内容不包含bilibili特征，可能是反爬页面")
    
    # 尝试多种正则模式
    patterns = [
        r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});',
        r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;',
        r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*</script>',
        r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;?\s*</script>'
    ]
    
    result = None
    for i, pattern in enumerate(patterns):
        print(f"尝试正则模式 {i+1}: {pattern}")
        match = re.search(pattern, data, re.DOTALL)
        if match:
            result = match.group(1)
            print(f"模式 {i+1} 匹配成功")
            break
    
    if not result:
        print("所有正则模式都未匹配到视频信息")
        print("页面内容片段:")
        print(data[:1000])
        return
    
    try:
        json_data = json.loads(result)
    except Exception as e:
        print("JSON解析失败:", e)
        print("原始内容片段:", result[:500])
        return
    
    video_data = json_data.get('videoData')
    if not video_data:
        # 有些页面结构不同，尝试输出json结构帮助调试
        print("未找到videoData字段，json结构如下：")
        print(json.dumps(json_data, ensure_ascii=False, indent=2)[:1000])
        return
    
    count = 1
    with open(name + '.txt', 'w', encoding='utf-8') as file:
        for index in video_data.get('pages', []):
            log = 'P{0} {1}'.format(count, index.get('part'))
            file.write(log + '\n')
            print(log)
            count += 1


if __name__ == '__main__':
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    # name = 'Bilibili视频目录_{0}'.format(current_time)
    global name
    name = 'Bilibili视频目录'
    file_name = name + '.html'
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            print("文件创建成功")
    file_size = os.path.getsize(file_name)
    if file_size == 0:
        url = input("请输入网址:")
        print("网址: ", url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        try:
            res = requests.get(url, headers=headers, timeout=10)
            print(f"请求状态码: {res.status_code}")
            print(f"响应头: {dict(res.headers)}")
        except Exception as e:
            print("请求失败:", e)
            exit(1)
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(res.text)
        print_directory(res.text)
    else:
        with open(file_name, 'r', encoding='utf-8') as f:
            read = f.read()
        print_directory(read)
# https://www.bilibili.com/video/BV1wh411d7it/
