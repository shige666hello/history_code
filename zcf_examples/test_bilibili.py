import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
import re

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
    with open('Bilibili视频目录.txt', 'w', encoding='utf-8') as file:
        for index in video_data.get('pages', []):
            log = 'P{0} {1}'.format(count, index.get('part'))
            file.write(log + '\n')
            print(log)
            count += 1

if __name__ == '__main__':
    url = "https://www.bilibili.com/video/BV1MT411x7GH/?spm_id_from=333.337.search-card.all.click&vd_source=ce46b2e276d2fb10e8e4310fa193edb2"
    print("测试URL:", url)
    
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
    
    # 保存HTML文件用于调试
    with open('debug_bilibili.html', 'w', encoding='utf-8') as f:
        f.write(res.text)
    print("已保存HTML到 debug_bilibili.html")
    
    print_directory(res.text) 