import requests
from pynocaptcha import CloudFlareCracker
import pandas as pd
import time
import random
import string

# 平台注册地址 https://goo.su/0np0os1 获取令牌
USER_TOKEN = ""
# cf和这个平台都支持 ipv6代理
difficulty = "hard"

session = requests.session()
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "referer": "https://testnet.lenscan.io/faucet",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "trpc-accept": "application/jsonl",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "x-trpc-source": "nextjs-react"
}

# 读取Excel文件
df = pd.read_excel('len领水.xlsx')  # 替换为你的Excel文件名
addresses = df['Address'].tolist()  # 地址列名为'Address'

# 添加起始和结束地址的选择
print(f"\n总共有 {len(addresses)} 个地址")
while True:
    try:
        start_index = int(input("请输入起始地址序号（从1开始）: ")) - 1  # 转换为0基索引
        end_index = int(input("请输入结束地址序号: "))
        
        if 0 <= start_index < len(addresses) and 0 < end_index <= len(addresses) and start_index < end_index:
            break
        else:
            print(f"输入无效！请输入1到{len(addresses)}之间的数字，且起始序号要小于结束序号")
    except ValueError:
        print("请输入有效的数字！")

# 获取选定范围的地址
selected_addresses = addresses[start_index:end_index]

def generate_session_id(length=10):
    """生成随机会话ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_proxy_ip(proxy_url):
    """检查代理IP"""
    try:
        
        response = requests.get('http://ipv6.lookup.test-ipv6.com/ip/', proxies={
            'http': proxy_url,
            'https': proxy_url
        }, timeout=10)
        return f"IP: {response.text.strip()}"
    except Exception as e:
        return f"获取代理IP信息失败: {str(e)}"

def get_new_proxy():
    """获取新的代理配置"""
    # 代理配置参数
    # https://goo.su/V64GMH 注册创建ipv6频道
    host = ""
    port = ""
    channel_id = "" #频道id
    proxy_type = "ipv6"  # 固定为ipv6类型
    country = ""  # 地区代码
    session_duration = "0m"  # 每次请求新的会话
    session_id = generate_session_id()  # 生成随机会话ID
    password = "" # 频道密码

    # 构建代理URL
    username = f"{channel_id}-{proxy_type}-country_{country}-r_{session_duration}-s_{session_id}"
    proxy_url = f"http://{username}:{password}@{host}:{port}"
    
    print(f"使用代理会话ID: {session_id}")
    return proxy_url

# 循环处理选定的地址
for index, address in enumerate(selected_addresses, start_index + 1):
    print(f"\n正在处理第 {index}/{len(addresses)} 个地址: {address}")
    
    # 为每个新地址获取新的代理
    current_proxy = get_new_proxy()
    
    try:
        resp = requests.post("http://api.nocaptcha.cn/api/wanda/lenscan/universal", headers={
            "User-Token": USER_TOKEN
        }, json={
            "difficulty": difficulty,
        }).json()
        print("验证码响应:", resp)

        data = resp["data"]
        sessionId = data["sessionId"]
        moves = data["moves"]

        cracker = CloudFlareCracker(
            internal_host=True,
            user_token=USER_TOKEN,
            href="https://testnet.lenscan.io/faucet",
            sitekey="0x4AAAAAAA1z6BHznYZc0TNL",
            debug=False,
            show_ad=False,
            proxy=current_proxy,  # 使用新的代理
            timeout=60
        )
        ret = cracker.crack()
        print("CloudFlare验证结果:", ret)
        token = ret.get("token")

        url = "https://testnet.lenscan.io/api/trpc/faucet.claim"
        params = {"batch": "1"}

        data = {
            "0": {
                "json": {
                    "address": address,
                    "cfToken": token,
                    "gameChallenge": {
                        "sessionId": sessionId,
                        "moves": moves
                    }
                }
            }
        }

        response = session.post(url, json=data, headers=headers, params=params, proxies={
            "all": current_proxy  # 使用新的代理
        })

        print("领取结果:", response.text)
        
    except Exception as e:
        print(f"处理地址 {address} 时发生错误: {str(e)}")
    
    if index < end_index:  # 如果不是最后一个地址
        print(f"\n当前地址 {address} 处理完成。等待10秒后自动处理下一个地址...")
        time.sleep(10)  # 延长等待时间到10秒，避免请求过于频繁

print("\n所有选定地址处理完成！")
