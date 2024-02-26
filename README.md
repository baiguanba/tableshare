# TableShare

TableShare is a lightweight Python library for extracting table data from web pages and converting it into pandas DataFrame. It supports scraping tables from online resources and local HTML files.

## Installation

You can install TableShare via pip:

```bash
pip install tableshare
```

## Usage
### Scraping Tables from Online Resources


#### 1.Fetch all tables
```python
import tableshare as ts
url = 'http://example.com/table-page' 
df = ts.fetch_all_tables(url)
print(df)
```

#### 2.Fetch a specific table
```python
import tableshare as ts
url = 'http://example.com/table-page' 
df = ts.fetch_table(url, table_index=0)
print(df)
```

### Scraping Tables from Local HTML Files
#### 1.Fetch all tables from a local file
```python
import tableshare as ts
html_file_path = 'path_to_your_local_file.html'
df = ts.fetch_all_tables_locally(html_file_path)
print(df)
```

#### 2.Fetch a specific table from a local file
```python
import tableshare as ts
html_file_path = 'path_to_your_local_file.html'
df = ts.fetch_table_locally(html_file_path, table_index=0)
print(df)
```

## Features
Scrape single or multiple tables from web pages.
Scrape single or multiple tables from local HTML files.
Convert scraped table data into pandas DataFrame for further analysis and processing.

## Notes
Make sure the target website's robots.txt allows crawler access when scraping online resources.
For dynamically loaded table data, you may need to use tools like Selenium to retrieve the complete page content.
When working with local files, ensure the file path is correct and the file is readable.
Contributing
If you encounter any issues or have suggestions for improvement while using TableShare, please submit an issue or pull request on the GitHub repository.

## License
TableShare is released under the MIT license. For more information, please see the LICENSE file.

## Contact
If you have any questions or need assistance, please contact us via:

Email: baiguanba@outlook.com

GitHub Repository: https://github.com/baiguanba/tableshare

## Support
If you find TableShare useful and would like to support its development, please consider starring the repository on GitHub.
