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


def get_all_tables(url):
    """
    Extracts the specified table from a web page and converts it to a pandas DataFrame.

    :param url: The URL of the web page containing the table.
    """
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.119 Safari/537.36'})
        response.encoding = 'utf-8'  # 设置编码为'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')

        if not tables:  # 判断网站有没有任何表格
            print("没有找到任何table标签，两种可能：一是网站本身就没有任何table标签；二是网站的table可能是动态加载数据，可以尝试使用get_all_dynamic_tables方法，或将网页保存至本地并使用get_all_tables_locally方法。")
        else:
            for i, table in enumerate(tables):
                try:
                    # 判断table是否为空
                    if not table.find_all('tr'):  # 如果table没有tr标签就说明该table为空
                        print(f"Table{i+1}为空，两种可能：一是table本身就没有数据；二是网站的table可能是动态加载数据，可以尝试使用get_all_dynamic_tables方法，或将网页保存至本地并使用get_all_tables_locally方法。")
                        continue

                    # 初始化一个空列表来存储数据
                    data = []

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
                                print(f"警告：在处理Table {i + 1}，第 {row_index} 行时，发现列数({col_count})少于表头列数({len(headers)})，已补齐空值处理。")

                            # 3.如果当前行的<td>数量大于表头列数，忽略多余的<td>
                            else:
                                for num in range(len(headers)):
                                    col = cols[num]
                                    if col.name == 'td':
                                        row_data.append(col.text.strip())
                                print(f"警告：在处理Table {i + 1}，第 {row_index} 行时，发现列数({col_count})超出表头列数({len(headers)})，已只保留与表头对应的列。")
                            data.append(row_data)

                    # 如果data列表为空（即没有有效的数据行），则不创建DataFrame
                    if data:
                        # 创建DataFrame
                        df = pd.DataFrame(data, columns=headers)
                        # 打印DataFrame的前几行，以验证数据是否正确
                        print(f"Table {i + 1}:")
                        print(df)
                        print("\n")

                    else:
                        print(f"Table {i+1}没有有效的表格数据来创建DataFrame。")

                except Exception as e:
                    print(f"处理Table {i + 1}时发生错误: {e}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"连接错误: {e}")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"请求或解析网页时发生错误: {e}")


def get_the_table(url, table_index=0):
    """
    Extracts the specified table from a web page and converts it to a pandas DataFrame.

    :param url: The URL of the web page containing the table.
    :param table_index: The index of the table to extract (0-based).
    :return: A pandas DataFrame containing the table data.
    """
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/72.0.3626.119 Safari/537.36'})
        response.encoding = 'utf-8'  # 设置编码为'utf-8'

        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')

        if not tables:  # 判断tables是否为空，也就是网页有没有任何表格数据
            print("没有找到任何table标签，两种可能：一是网站本身就没有任何table标签；二是网站的table可能是动态加载数据，可以尝试使用get_the_dynamic_table方法，或将网页保存至本地并使用get_the_table_locally方法。")

        else:
            # 提取我们想要的表格
            table = tables[table_index]  # 使用传入的索引

            # 判断table是否为空
            if not table.find_all('tr'):  # 如果table没有tr标签就说明该table为空
                print(f"Table{table_index+1}为空，两种可能：一是table本身就没有数据；二是网站的table可能是动态加载数据，可以尝试使用get_the_dynamic_table方法，或将网页保存至本地并使用get_the_table_locally方法。")
            else:
                # 初始化一个空列表来存储数据
                data = []

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
                            print(f"警告：在处理Table {table_index+1}，第 {row_index} 行时，发现列数({col_count})少于表头列数({len(headers)})，已补齐空值处理。")

                        # 3.如果当前行的<td>数量大于表头列数，忽略多余的<td>
                        else:
                            for num in range(len(headers)):
                                col = cols[num]
                                if col.name == 'td':
                                    row_data.append(col.text.strip())
                            print(f"警告：在处理Table {i + 1}，第 {row_index} 行时，发现列数({col_count})超出表头列数({len(headers)})，已只保留与表头对应的列。")
                        data.append(row_data)

                # 如果data列表为空（即没有有效的数据行），则不创建DataFrame
                if data:
                    # 创建DataFrame
                    df = pd.DataFrame(data, columns=headers)
                    # 打印DataFrame的前几行，以验证数据是否正确
                    # print(df.head())
                    return df
                else:
                    print(f"Table {table_index+1}没有有效的表格数据来创建DataFrame。")


    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"连接错误: {e}")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"处理表格时发生错误: {e}")


def get_all_tables_locally(html_file_path):
    """
    从指定的本地HTML文件中读取并打印所有表格数据。

    参数:
    html_file_path (str): 本地HTML文件的路径。

    返回:
    None
    """
    # 读取本地HTML文件
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有的table标签
    tables = soup.find_all('table')

    # 遍历所有的表格
    for i, table in enumerate(tables):
        # 使用pandas读取表格数据
        df_list = pd.read_html(str(table))
        if df_list:
            df = df_list[0]  # 假设每个表格只包含一个DataFrame
            print(f"Table {i + 1}:")
            print(df)
            print("\n")


def get_the_table_locally(html_file_path, table_index=0):
    """
    从指定的本地HTML文件中读取并返回指定索引的表格数据。

    参数:
    html_file_path (str): 本地HTML文件的路径。
    table_index (int): 要返回的表格的索引，默认为0（第一个表格）。

    返回:
    pd.DataFrame: 指定索引的表格数据。
    """
    try:
        # 读取本地HTML文件
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 查找所有的table标签
        tables = soup.find_all('table')

        # 确保table_index在有效范围内
        if table_index < 0 or table_index >= len(tables):
            raise IndexError("Table index is out of range.")

        # 获取指定索引的table
        target_table = tables[table_index]

        # 使用pandas读取表格数据
        df = pd.read_html(str(target_table))[0]  # 假设每个表格只包含一个DataFrame

        return df

    except FileNotFoundError:
        print("The specified HTML file was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_all_dynamic_tables(url):
    # path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'  # 请改为你电脑内Chrome可执行文件路径
    path = r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"'   # 请改为你电脑内Edge可执行文件路径
    ChromiumOptions().set_browser_path(path).save()
    wp = WebPage()
    wp.listen.start(url)  # 监听Json
    # wp.get('https://www.zhipin.com/web/geek/job?query=PHP&city=101270100')
    wp.get(url)

    packet = wp.listen.wait()

    # 假设 packet.response.body 包含了 HTML 内容
    html_content = packet.response.body
    try:

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'lxml')

        tables = soup.find_all('table')

        if not tables:
            print("没有找到任何table标签，说明网站本身就没有table标签。")
        else:
            for i, table in enumerate(tables):
                try:
                    # 判断table是否为空
                    if not table.find_all('tr'):  # 如果table没有tr标签就说明该table为空
                        print(f"Table{i + 1}为空，说明table本身就没有数据。")
                        continue

                    # 初始化一个空列表来存储数据
                    data = []

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
                                print(f"警告：在处理Table {i + 1}，第 {row_index} 行时，发现列数({col_count})少于表头列数({len(headers)})，已补齐空值处理。")

                            # 3.如果当前行的<td>数量大于表头列数，忽略多余的<td>
                            else:
                                for num in range(len(headers)):
                                    col = cols[num]
                                    if col.name == 'td':
                                        row_data.append(col.text.strip())
                                print(f"警告：在处理Table {i + 1}，第 {row_index} 行时，发现列数({col_count})超出表头列数({len(headers)})，已只保留与表头对应的列。")
                            data.append(row_data)

                    # 创建DataFrame
                    df = pd.DataFrame(data, columns=headers)

                    # 打印DataFrame的前几行，以验证数据是否正确
                    print(f"Table {i + 1}:")
                    print(df)
                    print("\n")

                except Exception as e:
                    print(f"处理Table {i + 1}时发生错误: {e}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"连接错误: {e}")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"请求或解析网页时发生错误: {e}")


def get_the_dynamic_table(url, table_index=0):
    # path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'  # 请改为你电脑内Chrome可执行文件路径
    path = r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"'   # 请改为你电脑内Edge可执行文件路径
    ChromiumOptions().set_browser_path(path).save()
    wp = WebPage()
    wp.listen.start(url)  # 监听Json
    # wp.get('https://www.zhipin.com/web/geek/job?query=PHP&city=101270100')
    wp.get(url)

    packet = wp.listen.wait()

    # 假设 packet.response.body 包含了 HTML 内容
    html_content = packet.response.body
    try:

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'lxml')

        tables = soup.find_all('table')

        if not tables:
            print("没有找到任何table标签，说明网站本身就没有table标签。")


        else:
            # 提取我们想要的表格
            table = tables[table_index]  # 使用传入的索引


            try:
                # 判断table是否为空
                if not table.find_all('tr'):  # 如果table没有tr标签就说明该table为空
                    print(f"Table{table_index + 1}为空，说明table本身就没有数据。")
                # 初始化一个空列表来存储数据
                data = []

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
                            print(f"警告：在处理Table {table_index + 1}，第 {row_index} 行时，发现列数({col_count})少于表头列数({len(headers)})，已补齐空值处理。")

                        # 3.如果当前行的<td>数量大于表头列数，忽略多余的<td>
                        else:
                            for num in range(len(headers)):
                                col = cols[num]
                                if col.name == 'td':
                                    row_data.append(col.text.strip())
                            print(f"警告：在处理Table {i + 1}，第 {row_index} 行时，发现列数({col_count})超出表头列数({len(headers)})，已只保留与表头对应的列。")
                        data.append(row_data)

                # 创建DataFrame
                df = pd.DataFrame(data, columns=headers)

                # 打印DataFrame的前几行，以验证数据是否正确
                print(f"Table {table_index + 1}:")
                print(df)
                print("\n")

            except Exception as e:
                print(f"处理Table {table_index + 1}时发生错误: {e}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"连接错误: {e}")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"请求或解析网页时发生错误: {e}")
