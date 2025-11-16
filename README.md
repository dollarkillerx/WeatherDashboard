# Weather Dashboard - Simplified Version

## Student Code: M24W0295

## 概述

简化版天气仪表板，使用 Python Flask 直接调用 Open-Meteo API 获取真实天气数据。

**简化了什么？**
- ✅ 移除了 Go 服务
- ✅ 移除了 MQTT broker
- ✅ 移除了复杂的消息队列架构
- ✅ Flask 直接调用 Open-Meteo API
- ✅ 前端直接从 Flask 获取数据

## 系统架构

```
┌─────────────────────┐
│  Open-Meteo API     │  (免费天气 API)
│  api.open-meteo.com │
└──────────┬──────────┘
           │ HTTPS
           ↓
┌─────────────────────┐
│   Python Flask      │  (后端 API)
│   localhost:5001    │
└──────────┬──────────┘
           │ REST API
           ↓
┌─────────────────────┐
│   Vue.js Frontend   │  (前端界面)
│   localhost:5173    │
└─────────────────────┘
```

## 特性

✅ **真实天气数据** - 使用 Open-Meteo API 获取实时天气信息
✅ **9个城市支持** - 东京、京都、大阪、北海道、新德里、北京、上海、纽约、法兰克福
✅ **7天天气预报** - 每日最高/最低温度、湿度、风速
✅ **24小时历史数据** - 温度、湿度、风速趋势图表
✅ **简单架构** - 只需 Python + Vue.js，无需 MQTT 或 Go 服务
✅ **免费 API** - Open-Meteo 完全免费，无需 API Key

## 快速启动

### 前置要求
- Python 3.8+
- Node.js 18+
- 互联网连接（用于访问 Open-Meteo API）

### 1. 启动后端 API
```bash
# 安装依赖（首次运行）
pip install flask flask-cors requests

# 启动 Flask 服务
python3 app.py
```

后端将运行在: **http://localhost:5001**

### 2. 启动前端
```bash
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

前端访问地址: **http://localhost:5173**

就这么简单！无需 MQTT broker，无需 Go 服务。

## 支持的城市

| 城市 | 国家/地区 |
|------|----------|
| Tokyo (东京) | 日本 🇯🇵 |
| Kyoto (京都) | 日本 🇯🇵 |
| Osaka (大阪) | 日本 🇯🇵 |
| Hokkaido (北海道) | 日本 🇯🇵 |
| New Delhi (新德里) | 印度 🇮🇳 |
| Beijing (北京) | 中国 🇨🇳 |
| Shanghai (上海) | 中国 🇨🇳 |
| New York (纽约) | 美国 🇺🇸 |
| Frankfurt (法兰克福) | 德国 🇩🇪 |

## API 端点

### 获取城市列表
```bash
curl http://localhost:5001/api/cities
```

### 获取当前天气
```bash
curl "http://localhost:5001/api/weather/current?city=Tokyo"
```

### 获取24小时历史数据
```bash
curl "http://localhost:5001/api/weather/history?city=Tokyo&limit=24"
```

### 获取天气统计
```bash
curl "http://localhost:5001/api/weather/stats?city=Tokyo"
```

### 获取7天预报
```bash
curl "http://localhost:5001/api/weather/forecast?city=Tokyo"
```

## 功能说明

### 当前天气
显示选定城市的实时天气数据：
- 🌡️ 温度 (°C)
- 💧 湿度 (%)
- 💨 风速 (km/h)
- 🧭 风向 (度)

### 24小时历史图表
展示过去24小时的天气趋势：
- 温度变化曲线
- 湿度变化曲线
- 风速变化曲线

### 7天天气预报
显示未来7天的天气预报：
- 每日最高/最低温度
- 平均湿度
- 最大风速
- 主导风向

### 城市切换
点击顶部的城市选择器，可以切换到任意支持的城市，所有数据会自动更新。

## 技术栈

### 后端
- **Python 3.x** - 编程语言
- **Flask** - Web 框架
- **Flask-CORS** - 跨域支持
- **Requests** - HTTP 客户端

### 前端
- **Vue.js 3** - 前端框架
- **TypeScript** - 类型安全
- **Chart.js** - 图表库
- **Axios** - HTTP 客户端
- **Vite** - 构建工具

### 数据源
- **Open-Meteo API** - 免费天气数据 API（无需 API Key）

## 项目结构

```
WeatherDashboard/
├── app.py                      # Flask 后端 API
├── test_openmeteo.py          # API 测试脚本
├── README.md                   # 本文档
└── frontend/
    ├── src/
    │   ├── App.vue            # 主应用组件
    │   ├── components/        # Vue 组件
    │   │   ├── WeatherCard.vue
    │   │   └── WeatherChart.vue
    │   └── services/
    │       └── weatherApi.ts  # API 客户端
    ├── package.json           # Node.js 依赖
    └── .env                   # 环境变量
```

## 开发说明

### 依赖安装
```bash
# Python 依赖
pip install flask flask-cors requests

# Node.js 依赖
cd frontend && npm install
```

### 开发模式
```bash
# 终端 1: 启动后端
python3 app.py

# 终端 2: 启动前端
cd frontend && npm run dev
```

### 生产构建
```bash
# 构建前端
cd frontend
npm run build

# 构建产物在 frontend/dist 目录
```

## 环境变量

### 前端配置 (`frontend/.env`)
```bash
# API 基础 URL
VITE_API_BASE_URL=http://localhost:5001
```

可以根据需要修改后端地址。

## 测试

### 测试 Open-Meteo API 集成
```bash
python3 test_openmeteo.py
```

预期输出:
```
✓ Successfully fetched current weather
✓ Successfully fetched 7-day forecast
✓ All tests passed!
```

### 测试 Flask API
```bash
# 健康检查
curl http://localhost:5001/api/health

# 获取东京天气
curl "http://localhost:5001/api/weather/current?city=Tokyo" | python3 -m json.tool
```

## 常见问题

**Q: 为什么数据不实时更新？**
A: Open-Meteo API 的数据通常每小时更新一次，不是实时数据。前端每30秒自动刷新一次。

**Q: 可以添加更多城市吗？**
A: 可以！在 `app.py` 的 `CITIES` 字典中添加城市名称和坐标即可。

**Q: API 有调用限制吗？**
A: Open-Meteo 免费 API 有合理使用限制，一般个人使用足够。

**Q: 历史数据只有24小时吗？**
A: 是的，为了简化，当前版本只显示24小时数据。可以修改 `fetch_hourly_history` 函数的 `past_days` 参数来获取更多历史数据。

**Q: 需要 API Key 吗？**
A: 不需要！Open-Meteo API 完全免费，无需注册或 API Key。

**Q: 端口 5000 被占用怎么办？**
A: 我们已经使用端口 5001。如果还有冲突，可以在 `app.py` 中修改端口号。

## 与原版本的对比

| 特性 | 原版本 | 简化版 |
|------|--------|--------|
| 后端语言 | Python + Go | 只需 Python |
| 消息队列 | MQTT (mosquitto) | 无需 |
| 数据源 | Go 生成的 mock 数据 | Open-Meteo 真实数据 |
| 启动步骤 | 3个服务 (MQTT, Go, Python) | 1个服务 (Python) |
| 复杂度 | 高 | 低 |
| 学习曲线 | 陡峭 | 平缓 |

## 数据流

```
用户浏览器 → Vue.js Frontend → Flask API → Open-Meteo API
                    ↑                           ↓
                    └───────────────────────────┘
                        返回真实天气数据
```

## 许可证

本项目仅供学习使用。

---

**Powered by Open-Meteo API** - https://open-meteo.com
**Student Code**: M24W0295
