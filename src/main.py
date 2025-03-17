import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crawler.site_crawler import ViteSiteCrawler

def main():
    crawler = ViteSiteCrawler()
    crawler.start()

if __name__ == "__main__":
    main() 