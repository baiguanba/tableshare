# TableShare

[![PyPI Package](https://img.shields.io/pypi/v/tableshare.svg)](https://pypi.org/project/tableshare/)

TableShare is a lightweight Python library for extracting table data from web pages and converting it into pandas DataFrame. It supports scraping tables from online resources.

## Installation

You can install TableShare via pip:

```bash
pip install tableshare
```

## Usage
### 获取静态网站数据


#### 1.展示所有静态网页数据表show all tables
```python
import tableshare as ts
url = 'http://example.com/table-page' 
df = ts.show_all_tables(url) # 默认参数dynamic是false
print(df)
```

#### 2.获取静态网页指定序号数据表get a specific table
```python
import tableshare as ts
url = 'http://example.com/table-page' 
df = ts.get_the_table(url,0) # 以0为例，0是table序列号
print(df)
```

### 获取动态网站数据
#### 1.展示所有动态网页数据表show all dynamic tables online
```python
import tableshare as ts
url = 'http://example.com/table-page' 
df = ts.show_all_tables(url, dynamic=True)
print(df)
```

#### 2.获取所有动态网页数据表get the dynamic table online
```python
import tableshare as ts
url = 'http://example.com/table-page' 
df = ts.get_the_table(url, 0, dynamic=True) # 以0为例，0是table序列号
print(df)
```

## Features
Scrape single or multiple tables from web pages.
Scrape single or multiple tables with JS dynamic loaded table data.
Convert scraped table data into pandas DataFrame for further analysis and processing.

## Notes
Make sure the target website's robots.txt allows crawler access when scraping online resources.
For dynamically loaded table data, you may need to use tools like Selenium to retrieve the complete page content.
If you encounter any issues or have suggestions for improvement while using TableShare, please submit an issue or pull request on the GitHub repository.

## License
TableShare is released under the MIT license. For more information, please see the LICENSE file.

## Contact
If you have any questions or need assistance, please contact us via:

Email: baiguanba@outlook.com

GitHub Repository: https://github.com/baiguanba/tableshare

PyPI Package: https://pypi.org/project/tableshare/

## Support
If you find TableShare useful and would like to support its development, please consider starring the repository on GitHub.