import configparser
import os
import sys

class ConfigLoader:
    @staticmethod
    def load_config():
        config = configparser.ConfigParser()
        
        # 确定配置文件路径
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            config_path = os.path.join(exe_dir, 'config.ini')
        else:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'config',
                'config.ini'
            )

        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
            print(f"使用配置文件: {config_path}")
        else:
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        return config 