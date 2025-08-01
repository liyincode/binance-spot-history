# Binance 现货历史数据获取工具

一个用于从 Binance API 获取现货交易对历史 K 线数据的 Python 脚本。

[English](README.md) | 中文

## 功能特性

- 📊 获取任意 Binance 现货交易对的历史 K 线数据
- ⏰ 支持多种时间间隔（1分钟、5分钟、1小时、1天等）
- 🔧 通过环境变量和命令行参数进行配置
- 📅 智能默认值的自动日期范围计算
- 🌍 UTC 时区处理，避免数据不一致
- 📈 格式化输出，包含价格变化和百分比计算
- 🔐 通过环境变量安全管理 API 密钥

## 安装

1. 克隆此仓库：
```bash
git clone https://github.com/yourusername/binance-spot-history.git
cd binance-spot-history
```

2. 安装所需依赖：
```bash
pip install python-binance python-dotenv
```

3. 在项目根目录创建 `.env` 文件：
```bash
cp .env.example .env
```

4. 配置你的 `.env` 文件：
```env
BINANCE_API_KEY=你的API密钥
BINANCE_API_SECRET=你的API秘钥
DEFAULT_SYMBOL=BTCUSDT
DEFAULT_DAYS_AGO=3
```

## 获取 Binance API 密钥

1. 访问 [Binance API 管理](https://www.binance.com/zh-CN/my/settings/api-management)
2. 创建新的 API 密钥
3. 启用"启用读取"权限（不需要现货交易权限）
4. 将你的 API Key 和 Secret Key 复制到 `.env` 文件中

## 使用方法

### 基本使用

获取默认交易对（在 .env 中配置）的最近 3 天数据：
```bash
python3 get_spot_history.py
```

### 指定交易对

获取特定交易对的数据：
```bash
python3 get_spot_history.py --symbol ETHUSDT
```

### 指定日期范围

获取特定日期范围的数据：
```bash
python3 get_spot_history.py --symbol BTCUSDT --start 2024-01-01 --end 2024-01-31
```

### 不同时间间隔

获取小时级数据而不是日级数据：
```bash
python3 get_spot_history.py --symbol BTCUSDT --interval 1h --start 2024-01-01 --end 2024-01-02
```

### 完整示例

```bash
python3 get_spot_history.py --symbol ADAUSDT --interval 4h --start 2024-07-01 --end 2024-07-31
```

## 支持的时间间隔

- **分钟级**: `1m`, `3m`, `5m`, `15m`, `30m`
- **小时级**: `1h`, `2h`, `4h`, `6h`, `8h`, `12h`
- **天级**: `1d`, `3d`
- **周级**: `1w`
- **月级**: `1M`

## 输出格式

脚本输出 JSON 格式的数据，包含以下字段：

```json
[
    {
        "datetime": "2024-07-31 08:00:00",
        "open": 0.706,
        "high": 0.73,
        "low": 0.661,
        "close": 0.667,
        "change": "-0.0390",
        "percentage_change": "-5.52%"
    }
]
```

## 配置选项

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|-------|------|--------|------|
| `BINANCE_API_KEY` | 你的 Binance API 密钥 | - | 是 |
| `BINANCE_API_SECRET` | 你的 Binance API 秘钥 | - | 是 |
| `DEFAULT_SYMBOL` | 默认交易对 | `BTCUSDT` | 否 |
| `DEFAULT_DAYS_AGO` | 默认获取天数 | `3` | 否 |

### 命令行参数

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--symbol` | 交易对符号 | 来自 `.env` 的值 |
| `--start` | 开始日期 (YYYY-MM-DD) | 自动计算 |
| `--end` | 结束日期 (YYYY-MM-DD) | 自动计算 |
| `--interval` | K线间隔 | `1d` |

## 错误处理

脚本处理各种错误场景：

- **缺少 API 凭证**: 当未配置 API 密钥时显示清晰的错误信息
- **无效交易对**: Binance API 将返回相应的错误信息
- **网络问题**: 处理连接超时和网络错误
- **无效日期格式**: 验证日期输入格式
- **API 速率限制**: 对超出速率限制的场景进行适当的错误处理

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

1. 查看 [Issues](https://github.com/yourusername/binance-spot-history/issues) 页面
2. 创建一个新的 issue，包含问题的详细信息
3. 包括你的 Python 版本、操作系统和任何错误信息

---

⭐ 如果这个项目对你有帮助，请考虑给它一个星标！
