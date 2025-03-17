import os
from pathvalidate import sanitize_filepath, replace_symbol
from urllib.parse import urlparse

class FileHandler:
    def __init__(self, config):
        self.output_dir = config.get('DEFAULT', 'output_dir')

    def get_file_path(self, url, ext=None):
        parsed_url = urlparse(url)
        path = parsed_url.path
        safe_netloc = replace_symbol(parsed_url.netloc, replacement_text="_")
        
        filename = os.path.basename(path) or 'index.html'
        filename = sanitize_filepath(filename)
        dir_path = os.path.dirname(path).lstrip('/')
        
        full_dir = os.path.join(
            self.output_dir,
            safe_netloc,
            dir_path
        )
        
        os.makedirs(full_dir, exist_ok=True)
        return os.path.join(full_dir, filename + (ext or ''))

    def save_html_file(self, url, content):
        file_path = self.get_file_path(url, '.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def save_binary_file(self, url, content):
        file_path = self.get_file_path(url)
        with open(file_path, 'wb') as f:
            f.write(content) 