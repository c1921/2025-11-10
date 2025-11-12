"""角色生成器模块 - 负责随机生成角色"""
import random
from typing import List
from models import Character, Gender


class CharacterGenerator:
    """角色生成器 - 随机生成角色"""
    
    # 中文姓氏池
    SURNAMES = [
        "王", "李", "张", "刘", "陈", "杨", "黄", "赵", "周", "吴",
        "徐", "孙", "马", "朱", "胡", "郭", "何", "林", "罗", "梁"
    ]
    
    # 男性名字池
    MALE_NAMES = [
        "伟", "强", "磊", "军", "勇", "杰", "涛", "明", "超", "辉",
        "刚", "峰", "平", "鹏", "华", "俊", "浩", "健", "波", "亮"
    ]
    
    # 女性名字池
    FEMALE_NAMES = [
        "芳", "娜", "静", "丽", "敏", "秀", "艳", "莉", "雪", "婷",
        "霞", "玲", "梅", "红", "洁", "燕", "萍", "琳", "娟", "英"
    ]
    
    @staticmethod
    def generate_name(gender: Gender, used_names: set) -> str:
        """生成不重复的随机名字"""
        max_attempts = 100
        
        for _ in range(max_attempts):
            surname = random.choice(CharacterGenerator.SURNAMES)
            if gender == Gender.MALE:
                name = random.choice(CharacterGenerator.MALE_NAMES)
            else:
                name = random.choice(CharacterGenerator.FEMALE_NAMES)
            
            # 可以生成单名或双名
            if random.random() < 0.3:  # 30% 概率双名
                if gender == Gender.MALE:
                    name += random.choice(CharacterGenerator.MALE_NAMES)
                else:
                    name += random.choice(CharacterGenerator.FEMALE_NAMES)
            
            full_name = surname + name
            
            if full_name not in used_names:
                return full_name
        
        # 如果100次都没成功，使用编号
        return f"{surname}{'男' if gender == Gender.MALE else '女'}{len(used_names)}"
    
    @staticmethod
    def generate_characters(count: int, inventory_slots: int = 20) -> List[Character]:
        """
        生成指定数量的随机角色
        
        参数:
            count: 生成数量
            inventory_slots: 背包大小
        
        返回:
            List[Character]: 角色列表
        """
        characters = []
        used_names = set()
        
        for i in range(count):
            # 随机性别（50/50）
            gender = random.choice([Gender.MALE, Gender.FEMALE])
            
            # 生成不重复的名字
            name = CharacterGenerator.generate_name(gender, used_names)
            used_names.add(name)
            
            # 随机生成初始年龄（18-50岁，天数0-364）
            age_years = random.randint(18, 50)
            age_days = random.randint(0, 364)
            
            # 创建角色
            character = Character(name, gender, inventory_slots, age_years, age_days)
            characters.append(character)
            
            print(f"[角色生成] 创建角色: {name} ({'男' if gender == Gender.MALE else '女'})")
        
        return characters

