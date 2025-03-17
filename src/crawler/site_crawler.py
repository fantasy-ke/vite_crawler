from bs4 import BeautifulSoup
import requests
from ..utils.config_loader import ConfigLoader
from ..utils.file_handler import FileHandler
from .url_handler import URLHandler

class ViteSiteCrawler:
    def __init__(self):
        self.config = ConfigLoader().load_config()
        self.file_handler = FileHandler(self.config)
        self.url_handler = URLHandler(self.config)
        self.visited_urls = set()
        self.session = self._init_session()

    def _init_session(self):
        session = requests.Session()
        session.headers.update({
            "User-Agent": self.config.get('DEFAULT', 'user_agent')
        })
        return session

    def start(self):
        self._download_recursively(self.config.get('DEFAULT', 'base_url'))
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
                self.file_handler.save_binary_file(url, response.content)
        except Exception as e:
            print(f"处理失败: {url} - {str(e)}")

    def _process_html(self, url, html_content):
        self.file_handler.save_html_file(url, html_content)
        soup = BeautifulSoup(html_content, 'lxml')
        self._process_resources(soup, url)

    def _process_resources(self, soup, url):
        # 处理CSS和JS
        for tag in soup.find_all(['link', 'script']):
            if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
                self.url_handler.download_resource(tag['href'], url, self.session)
            elif tag.name == 'script' and 'src' in tag.attrs:
                self.url_handler.download_resource(tag['src'], url, self.session)

        # 处理图片
        for tag in soup.find_all('img'):
            if 'src' in tag.attrs:
                self.url_handler.download_resource(tag['src'], url, self.session)

        # 处理链接
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if self.url_handler.should_follow_link(href, url):
                self._download_recursively(self.url_handler.make_absolute_url(href, url)) 