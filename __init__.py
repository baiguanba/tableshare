"""
This module implements the main functionality of tableshare.
Author: Guanba
"""

__author__ = "GuanBa"
__email__ = "baiguanba@outlook.com"
__status__ = "planning"


from DrissionPage import ChromiumOptions
from DrissionPage import WebPage
import requests
from bs4 import BeautifulSoup
import pandas as pd




class TableScraper:
    def __init__(self):
        self.tables = None

    @staticmethod
    def scrape_tables(url, dynamic=False):
        try:
            if dynamic:
                # path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'  # 请改为你电脑内Chrome可执行文件路径
                path = r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"'  # 请改为你电脑内Edge可执行文件路径
                ChromiumOptions().set_browser_path(path).save()
                wp = WebPage()
                wp.listen.start(url)  # 监听Json
                wp.get(url)
                packet = wp.listen.wait()

                # 假设 packet.response.body 包含了 HTML 内容
                html_content = packet.response.body
                # 使用 BeautifulSoup 解析 HTML
                soup = BeautifulSoup(html_content, 'lxml')
            else:
                response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/72.0.3626.119 Safari/537.36'})
                response.encoding = 'utf-8'  # 设置编码为'utf-8'
                # 使用 BeautifulSoup 解析 HTML
                soup = BeautifulSoup(response.text, 'html.parser')

            tables = soup.find_all('table')
            return tables
        except Exception as e:
            print(f"请求或解析网页时发生错误: {e}")
            return None

    @staticmethod # 提取表头
    def extract_headers(table):
        # 提取表头（<th>标签的内容）
        headers = []
        header_row = table.find('tr')
        if header_row and header_row.find_all('th'):  # 确保header_row存在且包含<th>标签
            # 遍历每个<th>标签
            for th in header_row.find_all('th'):
                # 使用get_text()方法来获取包括span标签在内的所有文本
                header_text = th.get_text(strip=True)
                # 如果文本内容为空，则添加默认列名
                if not header_text:
                    header_text = 'Column' + str(len(headers) + 1)
                headers.append(header_text)
        # 如果没有th标签，则设置默认列名,len(table.find_all('tr')[1])是获取第2个tr标签里td的数量
        if not headers:
            headers = ['Column' + str(ii) for ii in range(1, len(table.find_all('tr')[0]) + 1)]
        return headers

    @staticmethod  # 提取table为pandas数据表
    def extract_table_data(table, headers, table_index):
        data = []
        # 提取表格数据（<td>标签的内容）
        for row_index, row in enumerate(table.find_all('tr'), start=1):  # 从1开始计数
            cols = row.find_all(['td', 'th'])
            if cols:
                col_count = len([col for col in cols if col.name == 'td'])
                row_data = []
                # 1.如果当前行的<td>数量与表头列数一致
                if col_count == len(headers):
                    for col in cols:
                        if col.name == 'td':
                            row_data.append(col.text.strip())
                # 2.如果当前行的<td>数量小于表头列数，补齐空值（这部分代码已在之前的回答中提供）
                elif col_count < len(headers):
                    for col in cols:
                        if col.name == 'td':
                            row_data.append(col.text.strip())
                    row_data += [''] * (len(headers) - len(row_data))
                    print(
                        f"警告：在处理Table {table_index + 1}，第 {row_index} 行时，发现列数({col_count})少于表头列数({len(headers)})，已补齐空值处理。")

                # 3.如果当前行的<td>数量大于表头列数，忽略多余的<td>
                else:
                    for num in range(len(headers)):
                        col = cols[num]
                        if col.name == 'td':
                            row_data.append(col.text.strip())
                    print(f"警告：在处理Table {table_index + 1}，第 {row_index} 行时，发现列数({col_count})超出表头列数({len(headers)})，已只保留与表头对应的列。")
                data.append(row_data)

        # 如果data列表为空（即没有有效的数据行），则不创建DataFrame
        if data:
            # 创建DataFrame
            df = pd.DataFrame(data, columns=headers)
            # 打印DataFrame的前几行，以验证数据是否正确
            # print(df.head())
            return df
        else:
            print(f"Table {table_index + 1}没有有效的表格数据来创建DataFrame。")


    @staticmethod  # 抓取单个table
    def get_the_table(url, table_index=0, dynamic=False):
        scraper = TableScraper()
        tables = scraper.scrape_tables(url, dynamic=dynamic)

        if table_index < 0:
            print("table_index 应为非负整数。")
            return
        elif not tables:
            print("未找到任何表格（没有找到任何table标签）。两种可能：一是网站本身就没有任何table标签；二是网站的table可能是动态加载数据，可以尝试将参数调成dynamic=True。")
            return

        elif table_index >= len(tables):
            print(f"超出了范围：序号为 {table_index}表格不存在。")
            return
        else:
            table = tables[table_index]
            headers = scraper.extract_headers(table)
            df = scraper.extract_table_data(table, headers, table_index)

            if df is not None:
                print(f"成功抓取 URL: {url} 中序号为 {table_index} 的表格数据：")
                print(f"Table {table_index + 1}:")
                return df
            else:
                print(f"Table {table_index + 1}:")
                print(f"表格为空，未能提取 URL: {url} 中序号为 {table_index} 的表格数据。")

    @staticmethod  # 打印全部table
    def show_all_tables(url, dynamic=False):
        scraper = TableScraper()
        tables = scraper.scrape_tables(url, dynamic=dynamic)

        if not tables:
            print(
                "未找到任何表格（没有找到任何table标签）。两种可能：一是网站本身就没有任何table标签；二是网站的table可能是动态加载数据，可以尝试将参数调成dynamic=True。")
            return
        else:
            for i, table in enumerate(tables):
                try:
                    headers = scraper.extract_headers(table)
                    df = scraper.extract_table_data(table, headers, i)
                    if df is not None:
                        print(f"成功抓取 URL: {url} 中序号为 {i} 的表格数据：")
                        print(f"Table {i + 1}:")
                        print(df)
                    else:
                        print(f"Table {i + 1}:")
                        print(f"表格为空，未能提取 URL: {url} 中序号为 {i} 的表格数据。")
                except Exception as e:
                    print(f"处理Table {i + 1}时发生错误: {e}")


