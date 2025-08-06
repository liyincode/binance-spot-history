# Binance 现货历史数据获取工具

用于从 Binance API 获取现货交易对历史 K 线数据的 Python 脚本，支持可选的技术分析指标。

[English](README.md) | 中文

## 功能特性

- 📊 获取任意 Binance 现货交易对的历史 K 线数据
- 📈 **技术分析**：计算移动平均线（MA）和其他技术指标
- ⏰ 支持多种时间间隔（1分钟、5分钟、1小时、1天等）
- 🔧 通过环境变量和命令行参数进行配置
- 📅 智能默认值的自动日期范围计算
- 🌍 UTC 时区处理，避免数据不一致
- 💡 根据时间间隔粒度智能调整日期时间格式
- 📊 格式化输出，包含价格变化和百分比计算
- 🔐 通过环境变量安全管理 API 密钥

## 可用脚本

- **`get_spot_history.py`** - 基础 K 线数据获取
- **`get_spot_history_with_ma.py`** - 增强版本，支持技术指标（移动平均线）

## 安装

1. 克隆此仓库：
```bash
git clone https://github.com/yourusername/binance-spot-history.git
cd binance-spot-history
```

2. 安装必需依赖：
```bash
# 基础依赖（两个脚本都需要）
pip install python-binance python-dotenv
```

3. 安装可选依赖用于技术分析（仅 `get_spot_history_with_ma.py` 需要）：
```bash
# 选项 A：TA-Lib（推荐，技术指标更准确）
# 首先安装 TA-Lib C 语言库：
brew install ta-lib           # 在 macOS 上
# sudo apt-get install libta-lib-dev  # 在 Ubuntu/Debian 上
# 然后安装 Python 包装器：
pip install TA-Lib numpy
```

**注意**：如果你只打算使用基础的 `get_spot_history.py` 脚本，可以跳过技术分析依赖的安装。

4. 在项目根目录创建 `.env` 文件：
```bash
cp .env.example .env
```

5. 配置你的 `.env` 文件：
```env
BINANCE_API_KEY=你的API密钥
BINANCE_API_SECRET=你的API秘钥
DEFAULT_SYMBOL=BTCUSDT
DEFAULT_DAYS_AGO=3
# 技术分析设置（用于 get_spot_history_with_ma.py）
MA_PERIODS=7,25,99
```

## 获取 Binance API 密钥

1. 访问 [Binance API 管理](https://www.binance.com/zh-CN/my/settings/api-management)
2. 创建新的 API 密钥
3. 启用"启用读取"权限（不需要现货交易权限）
4. 将你的 API Key 和 Secret Key 复制到 `.env` 文件中

## 使用方法

### 基础 K 线数据

获取默认交易对（在 .env 中配置）的最近 3 天基础数据：
```bash
python3 get_spot_history.py
```

指定交易对和日期范围：
```bash
python3 get_spot_history.py --symbol ETHUSDT --start 2024-01-01 --end 2024-01-31
```

### 技术分析（移动平均线）

获取包含技术指标的数据（使用默认 MA 周期：7, 25, 99）：
```bash
python3 get_spot_history_with_ma.py
```

指定自定义 MA 周期：
```bash
python3 get_spot_history_with_ma.py --symbol BTCUSDT --ma-periods "5,20,50"
```

禁用 MA 计算（与基础脚本相同）：
```bash
python3 get_spot_history_with_ma.py --no-ma
```

### 不同时间间隔

获取包含技术指标的小时级数据：
```bash
python3 get_spot_history_with_ma.py --symbol BTCUSDT --interval 1h --start 2024-01-01 --end 2024-01-02
```

获取分钟级数据：
```bash
python3 get_spot_history.py --symbol ETHUSDT --interval 5m --start 2024-01-01 --end 2024-01-01
```

### 完整示例

```bash
# 获取 4 小时间隔的基础 K 线数据
python3 get_spot_history.py --symbol ADAUSDT --interval 4h --start 2024-07-01 --end 2024-07-31

# 获取包含自定义 MA 周期的技术分析数据
python3 get_spot_history_with_ma.py --symbol BTCUSDT --interval 1d --ma-periods "10,30,100" --start 2024-07-01 --end 2024-07-31
```

## 支持的时间间隔

- **分钟级**: `1m`, `3m`, `5m`, `15m`, `30m`
- **小时级**: `1h`, `2h`, `4h`, `6h`, `8h`, `12h`
- **天级**: `1d`, `3d`
- **周级**: `1w`
- **月级**: `1M`

## 输出格式

### 基础输出（get_spot_history.py）

```json
[
    {
        "datetime": "2024-07-31",
        "open": 0.706,
        "high": 0.73,
        "low": 0.661,
        "close": 0.667,
        "change": "-0.0390",
        "percentage_change": "-5.52%"
    }
]
```

### 增强输出（包含技术指标，get_spot_history_with_ma.py）

```json
[
    {
        "datetime": "2024-07-31",
        "open": 0.706,
        "high": 0.73,
        "low": 0.661,
        "close": 0.667,
        "volume": 1234567.89,
        "change": "-0.0390",
        "percentage_change": "-5.52%",
        "ma7": 0.684857,
        "ma25": 0.70692,
        "ma99": 0.669121
    }
]
```

**注意**：日期时间格式会根据时间间隔自动调整：
- 日级间隔（`1d`, `3d`, `1w`, `1M`）：`"2024-07-31"`
- 小时级间隔（`1h`, `2h` 等）：`"2024-07-31 14:00"`  
- 分钟级间隔（`1m`, `5m` 等）：`"2024-07-31 14:30:00"`

## 配置选项

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|-------|------|--------|------|
| `BINANCE_API_KEY` | 你的 Binance API 密钥 | - | 是 |
| `BINANCE_API_SECRET` | 你的 Binance API 秘钥 | - | 是 |
| `DEFAULT_SYMBOL` | 默认交易对 | `BTCUSDT` | 否 |
| `DEFAULT_DAYS_AGO` | 默认获取天数 | `3` | 否 |
| `MA_PERIODS` | 移动平均线周期（逗号分隔） | `7,25,99` | 否 |

### 命令行参数

#### 基础脚本（get_spot_history.py）

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--symbol` | 交易对符号 | 来自 `.env` 的值 |
| `--start` | 开始日期 (YYYY-MM-DD) | 自动计算 |
| `--end` | 结束日期 (YYYY-MM-DD) | 自动计算 |
| `--interval` | K线间隔 | `1d` |

#### 增强脚本（get_spot_history_with_ma.py）

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--symbol` | 交易对符号 | 来自 `.env` 的值 |
| `--start` | 开始日期 (YYYY-MM-DD) | 自动计算 |
| `--end` | 结束日期 (YYYY-MM-DD) | 自动计算 |
| `--interval` | K线间隔 | `1d` |
| `--no-ma` | 禁用移动平均线计算 | False |
| `--ma-periods` | 自定义 MA 周期（如 "5,20,50"） | 来自 `.env` 的值 |

## 错误处理

脚本处理各种错误场景：

- **缺少 API 凭证**: 当未配置 API 密钥时显示清晰的错误信息
- **无效交易对**: Binance API 将返回相应的错误信息
- **网络问题**: 处理连接超时和网络错误
- **无效日期格式**: 验证日期输入格式
- **API 速率限制**: 对超出速率限制的场景进行适当的错误处理
- **技术分析依赖**: 
  - 当 TA-Lib 未安装时优雅降级（使用简单 MA 计算）
  - 缺少可选依赖时显示警告信息
  - 验证 MA 周期格式

## 贡献

1. Fork 此仓库
2. 创建你的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 许可证

此项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 免责声明

此脚本仅用于教育和研究目的。请始终确保遵守 Binance 的服务条款和你所在司法管辖区的适用法规。

## 支持

如果你遇到任何问题或有疑问：

1. 查看 [Issues](https://github.com/liyincode/binance-spot-history/issues) 页面
2. 创建一个新的 issue，包含问题的详细信息
3. 包括你的 Python 版本、操作系统和任何错误信息

---

⭐ 如果这个项目对你有帮助，请考虑给它一个星标！
