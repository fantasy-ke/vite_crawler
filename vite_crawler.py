import os
import requests
import sys
from bs4 import BeautifulSoup
import configparser  # 必须添加此行
from urllib.parse import urljoin, urlparse
from pathvalidate import sanitize_filepath

class ViteSiteCrawler:
    def __init__(self):
        self.config = self.load_config()
        self.base_url = self.config.get('DEFAULT', 'base_url')
        self.output_dir = self.config.get('DEFAULT', 'output_dir')
        self.visited_urls = set()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def load_config(self):
        config = configparser.ConfigParser()

        # 优先读取可执行文件同目录的 config.ini
        if getattr(sys, 'frozen', False):
            # 打包后的运行路径
            exe_dir = os.path.dirname(sys.executable)
            config_path = os.path.join(exe_dir, 'config.ini')
        else:
            # 开发环境路径
            config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

        # 如果外部配置存在则使用，否则使用打包内置的
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
            print(f"使用外部配置文件: {config_path}")
        else:
            # 兼容旧逻辑（临时目录）
            config_path = os.path.join(sys._MEIPASS, 'config.ini')
            config.read(config_path, encoding='utf-8')
            print(f"使用内置配置文件: {config_path}")

        return config

    def start(self):
        self._download_recursively(self.base_url)
        print("下载完成！")

    def _download_recursively(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)

        print(f"正在处理: {url}")
        try:
            response = self.session.get(url)
            response.encoding = 'utf-8'
            content_type = response.headers.get('Content-Type', '')

            if 'text/html' in content_type:
                self._process_html(url, response.text)
            else:
                self._save_binary_file(url, response.content)
        except Exception as e:
            print(f"处理失败: {url} - {str(e)}")

    def _process_html(self, url, html_content):
        # 保存当前HTML文件
        file_path = self._get_file_path(url, ext=".html")
        self._save_text_file(file_path, html_content)

        # 解析并下载关联资源
        soup = BeautifulSoup(html_content, 'lxml')
        self._process_css_js(soup, url)
        self._process_images(soup, url)
        self._process_links(soup, url)

    def _process_css_js(self, soup, url):
        for tag in soup.find_all(['link', 'script']):
            if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
                self._download_resource(tag['href'], url)
            elif tag.name == 'script' and 'src' in tag.attrs:
                self._download_resource(tag['src'], url)

    def _process_images(self, soup, url):
        for tag in soup.find_all('img'):
            if 'src' in tag.attrs:
                self._download_resource(tag['src'], url)

    def _process_links(self, soup, url):
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            if self._is_same_domain(full_url) and not self._is_fragment(href):
                self._download_recursively(full_url)

    def _download_resource(self, resource_path, base_url):
        full_url = urljoin(base_url, resource_path)
        if full_url in self.visited_urls:
            return
        try:
            response = self.session.get(full_url)
            content_type = response.headers.get('Content-Type', '')
            ext = self._get_extension(content_type, resource_path)
            file_path = self._get_file_path(full_url, ext)
            self._save_binary_file(file_path, response.content)
            self.visited_urls.add(full_url)
        except Exception as e:
            print(f"资源下载失败: {full_url} - {str(e)}")

    def _get_file_path(self, url, ext=None):
        parsed_url = urlparse(url)
        path = parsed_url.path
        if not ext:
            ext = os.path.splitext(path)[1] or '.html'
        filename = os.path.basename(path) or 'index.html'
        filename = sanitize_filepath(filename)
        dir_path = os.path.dirname(path)
        if dir_path == '/':
            dir_path = ''

        full_dir = os.path.join(self.output_dir, parsed_url.netloc, dir_path.lstrip('/'))
        os.makedirs(full_dir, exist_ok=True)
        return os.path.join(full_dir, filename + ext if not os.path.splitext(filename)[1] else filename)

    def _save_text_file(self, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _save_binary_file(self, file_path, content):
        with open(file_path, 'wb') as f:
            f.write(content)

    def _is_same_domain(self, url):
        return urlparse(url).netloc == urlparse(self.base_url).netloc

    def _is_fragment(self, url):
        return url.startswith('#')

    def _get_extension(self, content_type, path):
        mime_map = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/svg+xml': '.svg',
            'text/css': '.css',
            'application/javascript': '.js',
            'font/woff2': '.woff2',
            'application/font-woff': '.woff',
            'application/pdf': '.pdf'
        }
        ext = os.path.splitext(path)[1]
        return mime_map.get(content_type, ext) or ext

if __name__ == "__main__":
    # 使用示例
    crawler = ViteSiteCrawler()
    crawler.start()