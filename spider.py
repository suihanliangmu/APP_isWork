import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any
import random
import pytz
import base64

# 通用请求头配置
COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
}

# 需要特殊头部的接口配置,雪球Cookie池
XUEQIU_COOKIES = [
    "cookiesu=551744191217108; device_id=d9e86e22778257e0ab65860c4c2a7684; smidV2=202504091733374611ceea9980a464ca9178de5e6ca04d00e36e4b7cef2d990; s=bu126mle9w; __utma=1.910266438.1744377181.1744377181.1744377181.1; __utmz=1.1744377181.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_a_token=8227a6f1f070ca10a573ea273e25da157b017b89; xqat=8227a6f1f070ca10a573ea273e25da157b017b89; xq_r_token=8c19700a9bde6cebd6eb64490168b410844f0b33; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc0NjA2MTE1OSwiY3RtIjoxNzQ0NDI2MDQwMDkzLCJjaWQiOiJkOWQwbjRBWnVwIn0.oWf-rKBcyhOYTDzhfCp0sF8Xk_IzGwJXXkfEVo_XJTLVTqi54kOuyBqGeBMFo7NA11uxdqnhp2yCHJLvLeLyn7TD1qLkTEKZBRiOzUaSqcBHrB0Smz2L7OQe4a76tkL0YzqEYJunwjdX1du3gbASPdmiY44v_HCGQPgqbSk9mrynDteo_s6_RfeRQyHgnNDeglAvJ4vw4xTT8yW6izkKAJw-5NT5Zw50eyQ0ecqwAxEoGOvi7YRiKkF-hny61IT6a8ZDU_7Vq9Zt9G4XNaRgLyXYu3Vsqwc7FVyZz_VYiYT745-bp50k0SnEmVaitnl6KvxtM2XMxbnYx58CWHO5oA; u=551744191217108; Hm_lvt_1db88642e346389874251b5a1eded6e3=1744191218,1744205797,1744376103,1744426082; HMACCOUNT=B46480FFCA5CA39A; acw_tc=1a0c655817444728247145924e0040251573d307bfb1fe652bb2077acc345a; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1744472824; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=pOF5Ic80pgYBcdCt+FvcwYXAjwH9uMVb3G2Xa5doXIAVbfu0li30MLeybDyG6mQaq+bcdlceszlYX0FzrNb/EA%3D%3D; ssxmod_itna=CqRxRDnAKxhx2iD9expxfxiFzCxzxCHPG7DupxjKidKDUDQTLrIyuG4RGxDtXXeezgrBqDlZBqDZDGI3Dqx0oNfijqDQcmQ0Sp5rt8A0wjYmCn3w+HQ7CvmdP6KVAmCvOQlqGLDmKDyz2GjlDGGG4GwDGoD34DiDDPDbRNDAL4D7qDF8CbdXlrDm4GWBeDgBLmioPDjfA2qd6xDGko/D7jbGn3D0u3s6+0xYn3bxGY/364kElp+ZfrDjLeD/S+E6frOE98L9jBIZbn+teGyY5GuUnco66PYMeTrZYh+b0qjB2qBzBp59hDe7pHWvgZKz0XqYeql+1jqqChdeYx=KjirNDDAIyZ9Y44m535SW5vlTMl0tfx434DN4d2bHjRFGgqf7=Uh4nrNi0qPRPDb1n289YqeD; ssxmod_itna2=CqRxRDnAKxhx2iD9expxfxiFzCxzxCHPG7DupxjKidKDUDQTLrIyuG4RGxDtXXeezgrYDAK3E9dD0D7P1e7/b4D/WZDhud=pYWEvXzqHL9=PSSh00pUze5FD"  # Cookie1
    ,"xq_a_token=8227a6f1f070ca10a573ea273e25da157b017b89; xqat=8227a6f1f070ca10a573ea273e25da157b017b89; xq_r_token=8c19700a9bde6cebd6eb64490168b410844f0b33; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc0NjA2MTE1OSwiY3RtIjoxNzQ0NDI4OTMwMTc2LCJjaWQiOiJkOWQwbjRBWnVwIn0.Ni8UuW50WxOr01KwG4gUm8xWqxMef7Z6mc28Yw3PTRMRHWnyHGM_uxATIcvUlwAbMY1TPVT0XSokP9GCZT8uB6d9rxsCCjyY3iYkNKUE7tCqlA1i--Qlnrh7u3BdKnFsvKZ3oUR59S4_KZJ0eN2rsH22rfIOYobSITR6f4sx_eCBIw7AAwyYloxGGU4970PWNAMP5X2lKt9izfTTsjnA9p5XGxX4k2bJ5W98BzDnE4BQnIO-3wppg1dEQd2ZCjBUuiGAeBr79qX7debGIAS3vqB1ldUFrBINN0xskZOAgsx0ksn5OdVP5OQQZfIbRjTkd1Vamx1fi9HwcwQfsowzAQ; cookiesu=331744428981212; u=331744428981212; device_id=5b9b7524068052fd707f86ec5b0d9281; Hm_lvt_1db88642e346389874251b5a1eded6e3=1744428982; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1744428982; HMACCOUNT=C3F890D6F016FA61; ssxmod_itna=iqRx0iGQq7qxhx+h0bDC+rDOD2BGODl4BtGRBDITq7=GFbDCgqtrdQ4BIhZd+wKKhePxDsrDWTYDSxD6FDK4GTh8=0+hkQ0OB7K4KTGwimj=Q8Y2yYY38hhP+K+km2DCvT53rYDHxY=DCMwZ+YYD433Dt4DIDAYDDxDWDYoDxGUbDG=D7g232QuYxi3Db2TDmuNWKcWD0fm5Tln5DDtIlqG2irbqDDNqD9Dq22iqQPD+lMnb0cRNttw5x0tWDBLwf9G5Ec8j=Auwstqbo3rDzuCDtdT7LeH7mlT=oaXxY8hi0S+itRAN+04e7DKBqcrNQBYHY4six+Yx5gYFBYQDGWBKgM+7xDiE5Q+pxQAiCtc2tNxAyP4dip+YvFK5/6I67DCjIdIw1QGzCDCCerCesW5Cl0ZAN4YD; ssxmod_itna2=iqRx0iGQq7qxhx+h0bDC+rDOD2BGODl4BtGRBDITq7=GFbDCgqtrdQ4BIhZd+wKKhexDfiqjCui+eDFoxadzFlODyFrw1dD"  # Cookie2
    ,"xq_a_token=8227a6f1f070ca10a573ea273e25da157b017b89; xqat=8227a6f1f070ca10a573ea273e25da157b017b89; xq_r_token=8c19700a9bde6cebd6eb64490168b410844f0b33; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc0NjA2MTE1OSwiY3RtIjoxNzQ0NDI4OTMwMTc2LCJjaWQiOiJkOWQwbjRBWnVwIn0.Ni8UuW50WxOr01KwG4gUm8xWqxMef7Z6mc28Yw3PTRMRHWnyHGM_uxATIcvUlwAbMY1TPVT0XSokP9GCZT8uB6d9rxsCCjyY3iYkNKUE7tCqlA1i--Qlnrh7u3BdKnFsvKZ3oUR59S4_KZJ0eN2rsH22rfIOYobSITR6f4sx_eCBIw7AAwyYloxGGU4970PWNAMP5X2lKt9izfTTsjnA9p5XGxX4k2bJ5W98BzDnE4BQnIO-3wppg1dEQd2ZCjBUuiGAeBr79qX7debGIAS3vqB1ldUFrBINN0xskZOAgsx0ksn5OdVP5OQQZfIbRjTkd1Vamx1fi9HwcwQfsowzAQ; cookiesu=331744428981212; u=331744428981212; device_id=5b9b7524068052fd707f86ec5b0d9281; Hm_lvt_1db88642e346389874251b5a1eded6e3=1744428982; HMACCOUNT=C3F890D6F016FA61; s=cv16sjcvt1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1744472929; ssxmod_itna=iqRx0iGQq7qxhx+h0bDC+rDOD2BGODl4BtGRBDITq7=GFbDCgqtrdQ4BIh1le+NKs/QYW+kDBd4G84xiNDAc40iDC3WLxFQCwxtq3uiYO4Ce+06rbq/tfn4UwF77gAhSoOQDzmce3K4GLDY=DCMqw+GhiDYYfDBYD74G+DDeDixGmYeDS3xD9DGP3cjTN6eDEDYprxitxrxcaxDLbAnrFsDDBzbiDKqpd=DDlQA7qFevP=7aDYbiFdEy=VGgQAeDMixGXWbkqAQy6M9DrOISQbZY5xB6cxBQNLauzhgbbVQc+KBAP4OLd4hbbR5+GPY0DQDiYb47GbUie/G4er4W+kW4q3YPUhV9BFDDWCCdkOD53ejM12kWe+zh04Ho4y2tRQGl2dKD5lOwg75S25D2hBYGeG4ZnhCn54D; ssxmod_itna2=iqRx0iGQq7qxhx+h0bDC+rDOD2BGODl4BtGRBDITq7=GFbDCgqtrdQ4BIh1le+NKs/QYW+iDG3mhi3O9CgRYyn2u5iDcmDyTUKeD" # Cookie3
    ,"xq_a_token=8227a6f1f070ca10a573ea273e25da157b017b89; xqat=8227a6f1f070ca10a573ea273e25da157b017b89; xq_r_token=8c19700a9bde6cebd6eb64490168b410844f0b33; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc0NjA2MTE1OSwiY3RtIjoxNzQ0NDI4OTMwMTc2LCJjaWQiOiJkOWQwbjRBWnVwIn0.Ni8UuW50WxOr01KwG4gUm8xWqxMef7Z6mc28Yw3PTRMRHWnyHGM_uxATIcvUlwAbMY1TPVT0XSokP9GCZT8uB6d9rxsCCjyY3iYkNKUE7tCqlA1i--Qlnrh7u3BdKnFsvKZ3oUR59S4_KZJ0eN2rsH22rfIOYobSITR6f4sx_eCBIw7AAwyYloxGGU4970PWNAMP5X2lKt9izfTTsjnA9p5XGxX4k2bJ5W98BzDnE4BQnIO-3wppg1dEQd2ZCjBUuiGAeBr79qX7debGIAS3vqB1ldUFrBINN0xskZOAgsx0ksn5OdVP5OQQZfIbRjTkd1Vamx1fi9HwcwQfsowzAQ; cookiesu=331744428981212; u=331744428981212; device_id=5b9b7524068052fd707f86ec5b0d9281; Hm_lvt_1db88642e346389874251b5a1eded6e3=1744428982; HMACCOUNT=C3F890D6F016FA61; smidV2=20250412113621b1554f7b2b218ae970b7bda22163375c00055a1f4ab307620; s=cv16sjcvt1; acw_tc=1a0c66dd17444729296151136e003ca914fd70d6994502ccc4985833bc99d6; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1744472929; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=NqVM0iC9pFOXCxWLom+4CJsH9pTvxeKcLTlGh87Ie1pyDjIuIRcdhNHt0ffqZCBuA2B0iOHV6GXfwohLJJ7tAA%3D%3D; ssxmod_itna=iqRx0iGQq7qxhx+h0bDC+rDOD2BGODl4BtGRBDITq7=GFbDCgqtrdQ4BIh1lePd4DfxHAeQUxGXYxqxiNDAc40iDC3WLxFQCwxtqxuiiO4Ce+06hbq/iKn4tmF77xEhS3OQDzmce3K4GLDY=DCMweB3eD4+3Dt4DIDAYDDxDWDYo4xGUbDG=D7ORQgju3xi3DbrWDmTiWtaaD0fmokCc5DDUveeG2i2bqDDNqY9DP2rrqWPD+eCcbBauNFtwox0tWDBLGR9Go2akU=YnpvtqWrfrDzT1DtLT8umH7jCWNr6Axi8hi9S+i4+b/ieDRDQ05RTr7iiUie/G4er44+k44qYYPUrVRBFDDWh7GVOdqY45O1Uqz++iudeFBKSwDSd43EtDmNz2DBGNVo5MiN/Bqxgq8xGeG4/mh8n54D; ssxmod_itna2=iqRx0iGQq7qxhx+h0bDC+rDOD2BGODl4BtGRBDITq7=GFbDCgqtrdQ4BIh1lePd4DfxHAeQ4xDf+KIe+0GGDFohhEQoDGNfrNeZT4jsYe=TeXr04pjhNz5GphPUwVloZ7KQl8Nr+AMl3L9lONjfbj4LbAA4RDjQdYE/YA5v8GewbXxjLpxdjPuQwxC0fPl/Qh9IDcdTD5y3a3SBnXdVB=iVuDVU0UfDcjkdZbipfGb5MPgeUP+wiXXQQftOn2Ckrbt=MpQoc4gbZRYKYvbytnS3phG8LPdQilhtft94gwfR0DZRDvGXyUNefYANRmwiaXi7GeU0eCq10qsQENlUPf0YWrxD" # Cookie4
    ,"cookiesu=551744191217108; device_id=d9e86e22778257e0ab65860c4c2a7684; s=bu126mle9w; xq_a_token=8227a6f1f070ca10a573ea273e25da157b017b89; xqat=8227a6f1f070ca10a573ea273e25da157b017b89; xq_r_token=8c19700a9bde6cebd6eb64490168b410844f0b33; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc0NjA2MTE1OSwiY3RtIjoxNzQ0NDI2MDQwMDkzLCJjaWQiOiJkOWQwbjRBWnVwIn0.oWf-rKBcyhOYTDzhfCp0sF8Xk_IzGwJXXkfEVo_XJTLVTqi54kOuyBqGeBMFo7NA11uxdqnhp2yCHJLvLeLyn7TD1qLkTEKZBRiOzUaSqcBHrB0Smz2L7OQe4a76tkL0YzqEYJunwjdX1du3gbASPdmiY44v_HCGQPgqbSk9mrynDteo_s6_RfeRQyHgnNDeglAvJ4vw4xTT8yW6izkKAJw-5NT5Zw50eyQ0ecqwAxEoGOvi7YRiKkF-hny61IT6a8ZDU_7Vq9Zt9G4XNaRgLyXYu3Vsqwc7FVyZz_VYiYT745-bp50k0SnEmVaitnl6KvxtM2XMxbnYx58CWHO5oA; u=551744191217108; Hm_lvt_1db88642e346389874251b5a1eded6e3=1744191218,1744205797,1744376103,1744426082; HMACCOUNT=B46480FFCA5CA39A; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1744472824; ssxmod_itna=CqRxRDnAKxhx2iD9expxfxiFzCxzxCHPG7DupxjKidKDUDQTLrIyuG4RGxDtXXeezgrBqDlZBqDZDGI3Dqx0oNfijqDQcmQ0Sp5rt8A0wjYmCn3w+HQ7CvmdP6KVAmCvOQlqGLDmKDyz2GjlDGGG4GwDGoD34DiDDPDbRNDAL4D7qDF8CbdXlrDm4GWBeDgBLmioPDjfA2qd6xDGko/D7jbGn3D0u3s6+0xYn3bxGY/364kElp+ZfrDjLeD/S+E6frOE98L9jBIZbn+teGyY5GuUnco66PYMeTrZYh+b0qjB2qBzBp59hDe7pHWvgZKz0XqYeql+1jqqChdeYx=KjirNDDAIyZ9Y44m535SW5vlTMl0tfx434DN4d2bHjRFGgqf7=Uh4nrNi0qPRPDb1n289YqeD; ssxmod_itna2=CqRxRDnAKxhx2iD9expxfxiFzCxzxCHPG7DupxjKidKDUDQTLrIyuG4RGxDtXXeezgrYDAK3E9dD0D7P1e7/b4D/WZDhud=pYWEvXzqHL9=PSSh00pUze5FD" # Cookie5
]

def get_fresh_xueqiu_cookie():
    """访问雪球网站获取新的Cookie"""
    session = requests.Session()

    # 访问雪球首页
    try:
        session.get('https://xueqiu.com/', headers=COMMON_HEADERS, timeout=10)

        # 有些网站需要额外访问几个页面才能获得完整Cookie
        session.get('https://xueqiu.com/hq', headers=COMMON_HEADERS, timeout=10)

        # 获取会话中的Cookie
        cookie_dict = session.cookies.get_dict()
        cookie_str = '; '.join([f'{k}={v}' for k, v in cookie_dict.items()])
        return cookie_str
    except Exception as e:
        print(f"获取新Cookie失败: {str(e)}")
        return None

def send_request(url: str, headers: Dict[str, str], params: Dict[str, Any] = None, retry: int = 3) -> requests.Response:
    """带重试机制的通用请求函数"""
    for attempt in range(retry):
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            if attempt == retry - 1:
                raise e
            time.sleep(2 ** attempt)
    return None


def get_baidu_top10() -> List[str]:
    """获取百度实时热榜"""
    url = 'https://top.baidu.com/api/board?platform=wise&tab=realtime'
    try:
        response = send_request(url, COMMON_HEADERS)
        data = response.json()['data']['cards'][0]['content'][0:10]
        return [f"{i + 1}. {item['query']}" for i, item in enumerate(data)]
    except Exception as e:
        return [f"百度数据获取失败"]


def get_weibo_top10() -> List[str]:
    """获取微博热搜榜"""
    url = 'https://weibo.com/ajax/statuses/hot_band'
    try:
        response = send_request(url, COMMON_HEADERS)
        data = response.json()['data']['band_list'][0:10]
        return [f"{i + 1}. {item['word']}" for i, item in enumerate(data)]
    except Exception as e:
        return [f"微博数据获取失败"]


def get_toutiao_top10() -> List[str]:
    """获取头条热榜"""
    url = "https://www.toutiao.com/hot-event/hot-board/"
    try:
        response = send_request(url, COMMON_HEADERS, {"origin": "toutiao_pc"})
        data = response.json()['data'][0:10]
        return [f"{i + 1}. {item['Title']}" for i, item in enumerate(data)]
    except Exception as e:
        return [f"头条数据获取失败"]


def get_zhihu_top10() -> List[str]:
    """获取知乎热榜"""
    url = 'https://www.zhihu.com/api/v4/search/top_search/tabs/hot/items'
    try:
        response = send_request(url, COMMON_HEADERS)
        data = response.json()['data'][0:10]
        return [f"{i + 1}. {item['query_display']}" for i, item in enumerate(data)]
    except Exception as e:
        return [f"知乎数据获取失败"]


def get_baidu_teleplay_top10() -> List[str]:
    """获取百度电视剧热榜"""
    url = 'https://top.baidu.com/api/board?platform=wise&tab=teleplay'

    try:
        response = send_request(url, COMMON_HEADERS)
        data = response.json()['data']['cards'][0]['content'][0:10]
        results = []
        for i, item in enumerate(data):
            # 处理演员显示逻辑
            actors = item['show'][2].split('：')[-1].split(' / ')[:6]
            actors_str = ' / '.join(actors)
            results.append(f"{item['word']}.演员：{actors_str}")
        return results
    except Exception as e:
        return [f"电视剧数据获取失败"]


def get_xueqiu_hot_stocks() -> List[str]:
    """获取雪球热股榜"""
    url = 'https://stock.xueqiu.com/v5/stock/hot_stock/list.json'
    fresh_cookie = get_fresh_xueqiu_cookie()
    cookie = random.choice(XUEQIU_COOKIES) if (fresh_cookie is None) else fresh_cookie
    headers = {**COMMON_HEADERS, 'Referer': 'https://xueqiu.com/','Cookie':cookie}

    try:
        response = send_request(url, headers, params={'size': 8, '_type': 10, 'type': 10})
        data = response.json()['data']['items'][0:10]
        return [
            f"{i + 1}. code:{item['code']}.name:{item['name']} .percent:{item['percent']}"
            for i, item in enumerate(data)
        ]
    except Exception as e:
        return [f"热股数据获取失败"]

def get_beijing_time():
    """获取北京时间"""
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def format_output(data: Dict[str, List[str]]) -> Dict[str, Any]:
    """格式化输出数据结构"""
    return {
        "代码执行完成时间": get_beijing_time(),
        "微博": data['weibo'],
        "百度": data['baidu'],
        "头条": data['toutiao'],
        "知乎": data['zhihu'],
        "电视剧": data['teleplay'],
        "热股": data['stocks']
    }

# 新增混淆函数
def simple_obfuscate(data: str) -> str:
    """轻度混淆处理"""
    # 步骤1: 反转字符串
    reversed_str = data[::-1]
    # 步骤2: 每隔3个字符插入随机干扰符
    obfuscated = []
    for i, char in enumerate(reversed_str):
        obfuscated.append(char)
        if (i+1) % 3 == 0:
            obfuscated.append(chr(random.randint(97, 122)))  # 随机小写字母
    return ''.join(obfuscated)



def main():
    """主执行函数"""
    result_data = {
        'weibo': get_weibo_top10(),
        'baidu': get_baidu_top10(),
        'toutiao': get_toutiao_top10(),
        'zhihu': get_zhihu_top10(),
        'teleplay': get_baidu_teleplay_top10(),
        'stocks': get_xueqiu_hot_stocks()
    }

    # 生成格式化输出
    formatted_data = format_output(result_data)

    # 写入JSON文件,由于gitee经常显示文件可能违规，特做处理
    json_str = json.dumps(formatted_data, ensure_ascii=False)
    encoded_data = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    obfuscated_data = simple_obfuscate(encoded_data)  # 新增混淆

    # 写入Base64编码后的文件
    with open('hot_data.txt', 'w', encoding='utf-8') as f:
        f.write(obfuscated_data)

    print("数据爬取完成并已保存至hot_data.txt")


if __name__ == "__main__":
    time.sleep(random.randint(3, 9))  # 随机暂停3~9s,避免反爬机制监测
    main()
