import requests
import re
import sys


def login(username, password):
    url = "https://pass.neu.edu.cn/tpass/login?service=https://ipgw.neu.edu.cn/srun_cas.php?ac_id=1"

    response = requests.get(url)
    text = response.text

    u = username
    p = password
    lt = re.search(r'id="lt" name="lt" value="(.+)"', text).groups()[0]
    execution = re.search(r'name="execution" value="(.+)"', text).groups()[0]
    _eventId = re.search(r'name="_eventId" value="(.+)"', text).groups()[0]
    ul = len(u)
    pl = len(p)
    rsa = u + p + lt

    data = {"rsa": rsa, "ul": str(ul), "pl": str(pl),
            "lt": lt, "execution": execution, "_eventId": _eventId}

    total = str('').join(list(data.keys()) + list(data.values()))
    content_length = len(data.keys()) * 2 - 1 + len(total)
    cookie = 'Language=zh_CN; jsessionid_tpass=' + requests.utils.dict_from_cookiejar(response.cookies)[
        'jsessionid_tpass']

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
               "Connection": "keep-alive",
               "Content-Length": str(content_length),
               "Content-Type": "application/x-www-form-urlencoded",
               "Cookie": cookie,
               "Host": "pass.neu.edu.cn",
               "Origin": "https://pass.neu.edu.cn",
               "Referer": "https://pass.neu.edu.cn/tpass/login?service=https://ipgw.neu.edu.cn/srun_cas.php?ac_id=1",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}

    redirect_url = requests.post(url, headers=headers, data=data, allow_redirects=False).headers['Location']

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Host": "ipgw.neu.edu.cn",
        "Referer": "https://pass.neu.edu.cn/tpass/login?service=https%3A%2F%2Fipgw.neu.edu.cn%2Fsrun_cas.php%3Fac_id%3D1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}

    response = requests.post(redirect_url, headers=headers, allow_redirects=False)

    session_for_srun_cas_php = requests.utils.dict_from_cookiejar(response.cookies)['session_for%3Asrun_cas_php']
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
               "Connection": "keep-alive",
               "Cookie": "session_for%3Asrun_cas_php=" + session_for_srun_cas_php,
               "Host": "ipgw.neu.edu.cn",
               "Referer": "https://pass.neu.edu.cn/tpass/login?service=https%3A%2F%2Fipgw.neu.edu.cn%2Fsrun_cas.php%3Fac_id%3D1",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}

    requests.get("https://ipgw.neu.edu.cn/srun_cas.php?ac_id=1", headers=headers)
    # 查询流量信息
    url = 'https://ipgw.neu.edu.cn/include/auth_action.php?k=85614'
    data = {"action": "get_online_info", "key": "85614"}  # key在js里为随机数，所以直接固定一个随机数
    total = str('').join(list(data.keys()) + list(data.values()))
    content_length = len(data.keys()) * 2 - 1 + len(total)
    headers = {"Accept": "*/*",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
               "Connection": "keep-alive", "Content-Length": str(content_length),
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Cookie": "session_for:srun_cas_php=" + session_for_srun_cas_php,
               "Host": "ipgw.neu.edu.cn",
               "Origin": "https://ipgw.neu.edu.cn",
               "Referer": "https://ipgw.neu.edu.cn/srun_cas.php?ac_id=1",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
               "X-Requested-With": "XMLHttpRequest"}

    response = requests.post(url, headers=headers, data=data)
    result = response.text.split(',')
    print('登录账号：' + u)
    print('当前IP：' + result[5])
    print('已用流量：' + "{:.2f}".format(int(result[0]) / 1024 / 1024) + ' M')
    print('已用时长：' + "{:.2f}".format(int(result[1]) / 3600) + ' 小时')
    print('账户余额：' + result[2] + " 元")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        login(sys.argv[1], sys.argv[2])
    else:
        print('Usage: python neu-ipgw.py username password')
