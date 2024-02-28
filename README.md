# TableShare

[![PyPI Package](https://img.shields.io/pypi/v/tableshare.svg)](https://pypi.org/project/tableshare/)

TableShare is a lightweight Python library for extracting table data from web pages and converting it into pandas DataFrame. It supports scraping tables from online resources.

## Installation

You can install TableShare via pip:

```bash
pip install tableshare
```

## Usage
### Scraping Tables from Online Resources


#### 1.show all tables
```python
from tableshare import TableScraper as ts
url = 'http://example.com/table-page' 
df = ts.show_all_tables(url)
print(df)
```

#### 2.get a specific table
```python
from tableshare import TableScraper as ts
url = 'http://example.com/table-page' 
df = ts.get_the_table(url)
print(df)
```

### Scraping Dynamic Tables from Online Resources
#### 1.show all dynamic tables online
```python
from tableshare import TableScraper as ts
url = 'http://example.com/table-page' 
df = ts.show_all_tables(url, dynamic=True)
print(df)
```

#### 2.get the dynamic table online
```python
from tableshare import TableScraper as ts
url = 'http://example.com/table-page' 
df = ts.get_the_table(url, dynamic=True)
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
