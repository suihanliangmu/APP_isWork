import requests
from bs4 import BeautifulSoup
import json


def get_baidu_top5():
    url = 'https://top.baidu.com/board?tab=realtime'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.select('.category-wrap_iQLoo')[0:5]

        results = []
        for i, item in enumerate(items, 1):
            title = item.select_one('.c-single-text-ellipsis').text.strip()
            hot = item.select_one('.hot-index_1Bl1a').text
            results.append(f"{i}. {title} ({hot})")
        return json.dumps(results,ensure_ascii=False)
    except Exception as e:
        return json.dumps([f"百度数据获取失败：{str(e)}"])


print(get_baidu_top5())
# 保存为JSON文件
with open('hot.json', 'w',encoding='utf-8') as f:
    f.write(get_baidu_top5())
