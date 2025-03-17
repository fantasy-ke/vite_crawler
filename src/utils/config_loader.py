import configparser
import os
import sys

class ConfigLoader:
    DEFAULT_CONFIG = {
        'base_url': 'https://vitejs.cn/vite3-cn/guide/',
        'output_dir': './vite_html',
        'max_depth': '5',
        'user_agent': 'Mozilla/5.0'
    }

    @staticmethod
    def load_config():
        config = configparser.ConfigParser()
        
        # 首先检查可执行文件目录下的config文件夹中的配置文件
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            external_config = os.path.join(exe_dir, 'config', 'config.ini')
            # 确保config文件夹存在
            os.makedirs(os.path.dirname(external_config), exist_ok=True)
            
            if os.path.exists(external_config):
                try:
                    config.read(external_config, encoding='utf-8')
                    # 验证配置文件是否有效
                    if 'DEFAULT' in config and 'base_url' in config['DEFAULT']:
                        print(f"使用外部配置文件: {external_config}")
                        return config
                    else:
                        print(f"外部配置文件格式无效: {external_config}")
                except Exception as e:
                    print(f"读取外部配置文件失败: {e}")

        # 如果没有外部配置文件，则使用打包的配置
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(sys.executable)
            config_path = os.path.join(base_path, 'config', 'config.ini')
        else:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'config',
                'config.ini'
            )

        # 尝试读取内置配置
        if os.path.exists(config_path):
            try:
                config.read(config_path, encoding='utf-8')
                print(f"使用内置配置文件: {config_path}")
            except Exception as e:
                print(f"读取内置配置文件失败: {e}")
                config['DEFAULT'] = ConfigLoader.DEFAULT_CONFIG
        else:
            config['DEFAULT'] = ConfigLoader.DEFAULT_CONFIG
            print("使用默认配置")

        # 在可执行文件目录的config文件夹中创建或更新外部配置文件
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            external_config = os.path.join(exe_dir, 'config', 'config.ini')
            try:
                # 确保config文件夹存在
                os.makedirs(os.path.dirname(external_config), exist_ok=True)
                with open(external_config, 'w', encoding='utf-8') as f:
                    config.write(f)
                print(f"已{'更新' if os.path.exists(external_config) else '创建'}外部配置文件: {external_config}")
            except Exception as e:
                print(f"创建外部配置文件失败: {e}")

        return config 