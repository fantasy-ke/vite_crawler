# Vite Crawler

一个用于爬取Vite中文文档的Python爬虫工具。

## 功能特点

- 支持Vite中文文档网站数据爬取
- 可配置爬取深度和参数
- 支持本地HTML文件保存
- 支持离线浏览文档

## 安装要求

- Python 3.7+
- PyInstaller (用于打包exe文件)
- 相关依赖包（requirements.txt中列出）

## 安装步骤

1. 克隆仓库

```
git clone https://github.com/fantasy-ke/vite_crawler.git
```

2. 安装依赖

```
pip install -r requirements.txt
```

## 使用方法

### 基本用法

直接运行Python脚本:
```
python vite_crawler.py
```

### ini配置说明
配置文件(config.ini)包含以下参数:
```
[DEFAULT]
# 爬虫起始URL
base_url = https://vitejs.cn/vite3-cn/guide/

# 文档保存目录
output_dir = ./vite_html

# 最大爬取深度
max_depth = 5

# 浏览器标识
user_agent = Mozilla/5.0
```

### 打包使用

使用PyInstaller打包成exe:
```
pyinstaller vite_crawler.spec
```

打包后的部署文件结构：
```
dist/
├── vite_crawler.exe   # 主程序
└── config.ini         # 配置文件(需要根据实际情况修改)
```

### 运行说明

1. 首次运行会在output_dir指定目录下创建HTML文件
2. 程序会自动爬取指定深度的所有文档页面
3. 爬取完成后可直接打开HTML文件离线浏览

## 注意事项

1. 请遵守目标网站的robots.txt规则
2. 建议设置适当的请求延迟，避免对目标服务器造成压力
3. 使用前请确保有适当的权限访问目标网站
4. 爬取过程中请保持网络连接稳定

## 许可证

MIT License

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 联系方式

如有问题，请通过Issue与我们联系。
