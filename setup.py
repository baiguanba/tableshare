
from setuptools import setup, find_packages
VERSION = '1.0.7'
DESCRIPTION = 'A Python library for scraping and sharing table data from web pages.'

setup(
    name='tableshare',
    version=VERSION,  # 请在发布新版本时更新这个版本号
    packages=find_packages(),  # 自动查找所有包
    install_requires=['requests', 'pandas', 'bs4', 'DrissionPage'],# 如果有其他依赖，请在这里添加
    keywords=['python','table','webtable','scrawler'],
    python_requires='>=3.6',  # 指定支持的Python版本
    author='Guanba',  # 替换为你的名字
    author_email='baiguanba@outlook.com',  # 替换为你的电子邮件地址
    description=DESCRIPTION,  # 库的简短描述
    long_description_content_type='text/markdown',  # 指定长描述的格式
    url='https://github.com/baiguanba/tableshare',  # 库的主页或源代码仓库链接
    classifiers=[  # 选择适当的分类器
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license='MIT',  # 你的库使用的许可证
    project_urls={  # 项目链接
        "Bug Tracker": "https://github.com/baiguanba/tableshare/issues"
    },
    scripts=[],  # 如果你的库包含可执行文件，请在这里列出
)
