import requests
import cchardet
import json
import csv


def download(url):
    # 设置用户代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    # 获得编码信息
    encoding = cchardet.detect(response.content)['encoding']
    html = response.content.decode(encoding)
    # 验证返回状态码是否为200
    if response.status_code == 200:
        return html

    
def parse_html(html):
    html = html["shuju"]
    for item in html:
        yield {
            'CATA_ID': item["CATA_ID"],
            '震级(M)': item["M"],
            '发震时刻(UTC+8)': item["O_TIME"],
            '纬度(°)': item["EPI_LAT"],
            '经度(°)': item["EPI_LON"],
            '深度(千米)': item["EPI_DEPTH"],
            '参考位置': item["LOCATION_C"],
            '具体链接': f'http://news.ceic.ac.cn/{item["CATA_ID"]}.html',
        }

        
def save_to_csv(item):
    with open('最近一年世界地震情况.csv', 'a', encoding='utf_8_sig',newline='') as f:
        # 'a'为追加模式（添加）
        # utf_8_sig 格式导出 csv 不乱码 
        fieldnames = ['CATA_ID', '震级(M)', '发震时刻(UTC+8)', '纬度(°)', '经度(°)', '深度(千米)', '参考位置', '具体链接']
        writer = csv.DictWriter(f,fieldnames = fieldnames)
        # w.writeheader()
        writer.writerow(item)

    
def main(page):
    # 可知一年的地震信息共有59页
    #for i in range(60):
    url = f"http://www.ceic.ac.cn/ajax/speedsearch?num=6&&page={page}"
    html = download(url)[1:-1]
    # 字符串转字典
    html = json.loads(html)
    # print(html["shuju"])
    for item in parse_html(html):
        # print(item)
        save_to_csv(item)

        
if __name__ == '__main__':
    for page in range(60):
        main(page)