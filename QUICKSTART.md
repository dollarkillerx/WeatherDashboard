# Quick Start Guide

## 快速启动指南

### 1. 启动 MQTT Broker (终端 1)
```bash
# 使用 Docker
docker run -it -p 1883:1883 eclipse-mosquitto:latest

# 或者使用本地 mosquitto
mosquitto -p 1883
```

### 2. 启动 Go 天气数据服务 (终端 2)
```bash
# 编译
go build -o weather-server main.go

# 运行
./weather-server
```

### 3. 启动 Flask API 后端 (终端 3)
```bash
# 安装依赖（首次运行）
pip install flask flask-cors paho-mqtt requests

# 启动服务
python3 app.py
```

### 4. 启动前端界面 (终端 4)
```bash
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

### 5. 访问应用
打开浏览器访问: **http://localhost:5173**

## 主要功能

### ✅ 已完成的改动

1. **真实天气数据**
   - ✓ Go 服务从 Open-Meteo API 获取实时天气数据
   - ✓ 支持 9 个城市的天气查询
   - ✓ 每 10 秒更新一次数据

2. **城市选择器**
   - ✓ 东京 (Tokyo)
   - ✓ 京都 (Kyoto)
   - ✓ 大阪 (Osaka)
   - ✓ 北海道 (Hokkaido)
   - ✓ 新德里 (New Delhi)
   - ✓ 北京 (Beijing)
   - ✓ 上海 (Shanghai)
   - ✓ 纽约 (New York)
   - ✓ 法兰克福 (Frankfurt)

3. **7 天天气预报**
   - ✓ 显示最高/最低温度
   - ✓ 平均湿度
   - ✓ 最大风速
   - ✓ 风向信息

4. **实时图表**
   - ✓ 温度历史曲线
   - ✓ 湿度历史曲线
   - ✓ 风速历史曲线

## 测试 API

### 获取城市列表
```bash
curl http://localhost:5001/api/cities
```

### 获取东京 7 天预报
```bash
curl http://localhost:5001/api/weather/forecast?city=Tokyo
```

### 获取北京 7 天预报
```bash
curl http://localhost:5001/api/weather/forecast?city=Beijing
```

### 获取当前天气
```bash
curl http://localhost:5001/api/weather/current
```

## 架构说明

```
Open-Meteo API
      ↓
Go Service (获取真实天气) → MQTT Broker → Flask API → Vue.js Frontend
      ↓                                        ↑
Open-Meteo API (7天预报) ──────────────────────┘
```

## 文件修改说明

### 修改的文件
1. `main.go` - Go 服务改为调用 Open-Meteo API
2. `app.py` - Flask API 添加城市和预报支持
3. `frontend/src/App.vue` - 添加城市选择器和7天预报
4. `frontend/src/services/weatherApi.ts` - 添加新的 API 方法

### 新增的文件
1. `test_openmeteo.py` - API 集成测试脚本
2. `USAGE.md` - 详细使用文档
3. `QUICKSTART.md` - 本快速启动指南

## 常见问题

**Q: 前端显示 "No weather data available yet"**
A: 确保 MQTT broker 和 Go 服务都在运行

**Q: 7天预报不显示**
A: 检查网络连接，Open-Meteo API 需要互联网访问

**Q: 切换城市后预报没更新**
A: 等待几秒钟，或刷新页面

## 技术栈

- **Backend**: Python Flask + Go
- **Frontend**: Vue.js 3 + TypeScript
- **Message Queue**: MQTT (mosquitto)
- **Weather API**: Open-Meteo (免费，无需 API Key)
- **Charts**: Chart.js

## 下一步

1. 运行 `python3 test_openmeteo.py` 测试 API 连接
2. 访问 http://localhost:5173 查看仪表板
3. 在顶部选择不同的城市
4. 查看实时数据和 7 天预报
