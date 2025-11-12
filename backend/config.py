"""游戏配置文件 - 从 JSON 加载配置"""
import json
import os


class GameConfig:
    """游戏配置 - 从 game_config.json 加载"""
    
    # 默认配置（如果 JSON 文件不存在）
    _DEFAULT_CONFIG = {
        "character": {
            "count": 3,
            "inventory_slots": 20,
            "initial_items": {
                "bread": 3,
                "apple": 5,
            },
            "initial_tools": ["axe", "pickaxe"]
        },
        "public_storage": {
            "slots": 100,
            "initial_items": {
                "bread": 20,
                "apple": 30,
                "wood": 50,
                "stone": 40,
                "pickaxe": 2,
                "axe": 2,
            }
        },
        "time": {
            "hour_duration": 0.2
        }
    }
    
    def __init__(self):
        """从 JSON 文件加载配置"""
        config_file = os.path.join(os.path.dirname(__file__), "game_config.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                print(f"[配置] 成功加载配置文件: {config_file}")
            except Exception as e:
                print(f"[配置] ⚠️ 加载配置文件失败: {e}")
                print(f"[配置] 使用默认配置")
                config_data = self._DEFAULT_CONFIG
        else:
            print(f"[配置] ⚠️ 配置文件不存在: {config_file}")
            print(f"[配置] 使用默认配置")
            config_data = self._DEFAULT_CONFIG
        
        # 角色配置
        self.CHARACTER_COUNT = config_data.get("character", {}).get("count", 3)
        self.CHARACTER_INVENTORY_SLOTS = config_data.get("character", {}).get("inventory_slots", 20)
        self.INITIAL_CHARACTER_ITEMS = config_data.get("character", {}).get("initial_items", {})
        self.INITIAL_TOOLS = config_data.get("character", {}).get("initial_tools", [])
        
        # 公共仓库配置
        self.PUBLIC_STORAGE_SLOTS = config_data.get("public_storage", {}).get("slots", 100)
        self.PUBLIC_STORAGE_INITIAL_ITEMS = config_data.get("public_storage", {}).get("initial_items", {})
        
        # 时间配置
        self.HOUR_DURATION = config_data.get("time", {}).get("hour_duration", 0.2)
        
        # 打印配置信息
        print(f"[配置] 角色数量: {self.CHARACTER_COUNT}")
        print(f"[配置] 背包大小: {self.CHARACTER_INVENTORY_SLOTS}")
        print(f"[配置] 公共仓库: {self.PUBLIC_STORAGE_SLOTS} 格")
        print(f"[配置] 时间速度: {self.HOUR_DURATION}s/小时")


# 创建全局配置实例
GameConfig = GameConfig()

