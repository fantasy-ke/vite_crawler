from urllib.parse import urljoin, urlparse

class URLHandler:
    def __init__(self, config):
        self.config = config
        self.base_url = config.get('DEFAULT', 'base_url')

    def make_absolute_url(self, url, base_url):
        return urljoin(base_url, url)

    def should_follow_link(self, url, base_url):
        if url.startswith('#'):
            return False
        absolute_url = self.make_absolute_url(url, base_url)
        return urlparse(absolute_url).netloc == urlparse(self.base_url).netloc

    def download_resource(self, resource_path, base_url, session):
        full_url = self.make_absolute_url(resource_path, base_url)
        try:
            response = session.get(full_url)
            return response.content
        except Exception as e:
            print(f"资源下载失败: {full_url} - {str(e)}")
            return None 