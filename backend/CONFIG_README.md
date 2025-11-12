# 游戏配置说明

## 配置文件位置

`backend/game_config.json`

## 配置说明

### 完整配置示例

```json
{
  "character": {
    "count": 30,                    // 初始角色数量
    "inventory_slots": 20,          // 角色背包大小（格子数）
    "initial_items": {              // 每个角色初始获得的物品
      "bread": 3,                   // 面包 x3
      "apple": 5                    // 苹果 x5
    },
    "initial_tools": ["axe", "pickaxe"]  // 随机分配的工具列表
  },
  "public_storage": {
    "slots": 100,                   // 公共仓库大小（格子数）
    "initial_items": {              // 公共仓库初始物品
      "bread": 20,
      "apple": 30,
      "wood": 50,
      "stone": 40,
      "pickaxe": 2,
      "axe": 2
    }
  },
  "time": {
    "hour_duration": 0.2            // 游戏中每小时的真实时长（秒）
  }
}
```

## 配置项详解

### 角色配置 (character)

| 配置项 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `count` | 整数 | 游戏初始生成的角色数量 | 3 |
| `inventory_slots` | 整数 | 每个角色的背包格子数 | 20 |
| `initial_items` | 对象 | 每个角色初始获得的物品 | `{"bread": 3, "apple": 5}` |
| `initial_tools` | 数组 | 随机分配给角色的工具 | `["axe", "pickaxe"]` |

**可用物品ID列表：**
- 食物：`bread`（面包）、`apple`（苹果）、`cooked_meat`（熟肉）、`berry`（浆果）
- 材料：`wood`（木材）、`stone`（石头）、`wheat`（小麦）
- 工具：`axe`（斧头）、`pickaxe`（镐子）

### 公共仓库配置 (public_storage)

| 配置项 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `slots` | 整数 | 公共仓库的总格子数 | 100 |
| `initial_items` | 对象 | 公共仓库初始存放的物品 | 见上方示例 |

### 时间配置 (time)

| 配置项 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `hour_duration` | 小数 | 游戏中每小时对应的真实秒数 | 0.2 |

**时间速度示例：**
- `0.2` = 每小时 200 毫秒（快速模式，适合测试）
- `1.0` = 每小时 1 秒（正常速度）
- `5.0` = 每小时 5 秒（慢速模式）

## 修改配置

### 方法1：直接编辑 JSON 文件

1. 打开 `backend/game_config.json`
2. 修改你想要的配置项
3. 保存文件
4. 重启游戏服务器

### 方法2：使用文本编辑器

推荐使用支持 JSON 语法的编辑器：
- VS Code
- Sublime Text
- Notepad++

## 常见配置场景

### 测试模式（少量角色，快速时间）

```json
{
  "character": {
    "count": 2,
    "inventory_slots": 20,
    "initial_items": {
      "bread": 10,
      "apple": 10
    },
    "initial_tools": ["axe", "pickaxe"]
  },
  "time": {
    "hour_duration": 0.1
  }
}
```

### 大型部落模式（多角色）

```json
{
  "character": {
    "count": 50,
    "inventory_slots": 30,
    "initial_items": {
      "bread": 5,
      "apple": 5
    },
    "initial_tools": ["axe", "pickaxe"]
  },
  "public_storage": {
    "slots": 500,
    "initial_items": {
      "bread": 100,
      "apple": 100,
      "wood": 200,
      "stone": 200
    }
  }
}
```

### 困难模式（资源稀缺）

```json
{
  "character": {
    "count": 5,
    "inventory_slots": 10,
    "initial_items": {
      "bread": 1,
      "apple": 1
    },
    "initial_tools": ["axe"]
  },
  "public_storage": {
    "slots": 50,
    "initial_items": {
      "bread": 5,
      "apple": 5
    }
  }
}
```

## 故障排除

### 配置文件格式错误

如果 JSON 格式有误，游戏会：
1. 显示警告信息
2. 自动使用默认配置
3. 继续运行

**常见错误：**
- ❌ 多余的逗号：`"count": 3,}`
- ❌ 缺少引号：`{count: 3}`
- ❌ 注释（JSON不支持）：`"count": 3 // 角色数量`

### 配置文件不存在

如果 `game_config.json` 不存在，游戏会使用内置的默认配置。

### 配置未生效

确保：
1. JSON 文件格式正确
2. 已保存文件
3. 已重启游戏服务器

## 启动信息

启动游戏时会看到配置加载信息：

```
[配置] 成功加载配置文件: D:\Github\2025-11-10\backend\game_config.json
[配置] 角色数量: 30
[配置] 背包大小: 20
[配置] 公共仓库: 100 格
[配置] 时间速度: 0.2s/小时
```

## 技术说明

- 配置文件编码：`UTF-8`
- 配置加载时机：服务器启动时
- 热重载：不支持（需要重启服务器）
- 验证：自动回退到默认值

