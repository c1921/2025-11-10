class GameTime:
    """游戏时间系统"""
    def __init__(self):
        self.day = 1
        self.hour = 0
        self.running = False
        self.base_hour_duration = 1  # 基础每小时1s
        self.speed = 1  # 速度倍率：1, 2, 5
        self.hour_duration = self.base_hour_duration / self.speed

    def tick(self):
        """时间推进"""
        self.hour += 1
        if self.hour >= 24:
            self.hour = 0
            self.day += 1

    def get_time_string(self) -> str:
        """获取格式化的时间字符串"""
        return f"第{self.day}天 {self.hour}时"

    def get_time_dict(self) -> dict:
        """获取时间数据"""
        return {
            "day": self.day,
            "hour": self.hour,
            "time_string": self.get_time_string(),
            "running": self.running,
            "speed": self.speed
        }

    def set_speed(self, speed: int):
        """设置时间流速"""
        if speed in [1, 2, 5]:
            self.speed = speed
            self.hour_duration = self.base_hour_duration / self.speed
            return True
        return False
