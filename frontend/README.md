# Weather Dashboard - Vue.js Frontend

## Overview

This is the frontend application for the Weather Dashboard system, built with Vue 3, TypeScript, and Vite. It provides a real-time interactive dashboard for monitoring weather data.

## Features

- **Real-time Data Display**: Auto-refreshing weather metrics every 2 seconds
- **Interactive Weather Cards**: Display current temperature, humidity, wind speed, and wind direction
- **Historical Charts**: Visualize weather trends using Chart.js
- **Statistical Analysis**: Show min, max, and average values for each metric
- **Connection Status**: Visual indicator for API connectivity
- **Responsive Design**: Mobile-friendly layout that works on all screen sizes
- **Error Handling**: Graceful error messages with retry functionality

## Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Chart.js** - Data visualization library
- **Axios** - HTTP client for API requests
- **Tailwind CSS** - Utility-first CSS framework

## Prerequisites

- Node.js 18+ or pnpm
- Python Flask backend running on port 5000
- Golang mock server publishing data via MQTT

## Installation

```bash
# Install dependencies
pnpm install

# Or using npm
npm install
```

## Development

```bash
# Start development server
pnpm dev

# Or using npm
npm run dev
```

The application will be available at `http://localhost:3000`

## Building for Production

```bash
# Build for production
pnpm build

# Preview production build
pnpm preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── WeatherCard.vue      # Individual weather metric card
│   │   └── WeatherChart.vue     # Chart component for historical data
│   ├── services/
│   │   └── weatherApi.ts        # API service layer
│   ├── App.vue                  # Main application component
│   ├── main.ts                  # Application entry point
│   └── style.css                # Global styles
├── public/                      # Static assets
├── .env                         # Environment variables
├── .env.example                 # Environment variables template
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript configuration
└── package.json                 # Dependencies and scripts
```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:5000
```

## API Endpoints Used

The frontend communicates with the Python Flask backend via these endpoints:

- `GET /api/health` - Health check
- `GET /api/weather/current` - Get current weather data
- `GET /api/weather/history?limit=50` - Get historical weather data
- `GET /api/weather/stats` - Get weather statistics

## Components

### WeatherCard.vue

Displays a single weather metric with:
- Large value display
- Icon representation
- Min/Max/Avg statistics
- Gradient background
- Hover animation

**Props:**
- `title` - Card title
- `value` - Current value
- `unit` - Unit of measurement
- `icon` - Emoji icon
- `stats` - Optional statistics object

### WeatherChart.vue

Displays historical data in a line chart with:
- Smooth animations
- Interactive tooltips
- Responsive sizing
- Custom color schemes

**Props:**
- `title` - Chart title
- `labels` - X-axis labels (timestamps)
- `datasets` - Chart.js dataset configuration

## Features in Detail

### Auto-Refresh

The dashboard automatically fetches new data every 2 seconds:
- Current weather data
- Historical data (last 50 readings)
- Statistical summaries

### Connection Status

Visual indicator shows:
- **Green**: Connected to backend
- **Red**: Connection lost

### Error Handling

- Displays user-friendly error messages
- Retry button for failed connections
- Console logging for debugging

### Responsive Design

Breakpoints:
- Desktop: 1400px max-width container
- Tablet: 2-column grid
- Mobile: Single column layout

## Development Tips

### Adding New Weather Metrics

1. Add the metric to the TypeScript interface in `weatherApi.ts`
2. Create a new `WeatherCard` component instance in `App.vue`
3. Add corresponding chart if needed

### Customizing Colors

Update the gradient colors in `WeatherCard.vue`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Chart colors are defined in `App.vue` datasets.

### Changing Refresh Interval

Modify the interval in `App.vue`:
```typescript
refreshInterval = window.setInterval(async () => {
  // ... fetch data
}, 2000); // Change this value (in milliseconds)
```

## Troubleshooting

### CORS Errors

Ensure Flask backend has CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

### API Connection Failed

1. Verify Flask backend is running on port 5000
2. Check `VITE_API_BASE_URL` in `.env`
3. Verify Golang mock server is publishing data

### Charts Not Displaying

1. Check browser console for errors
2. Ensure historical data is available
3. Verify Chart.js is properly imported

## Performance

- **Initial Load**: ~1-2 seconds
- **Data Refresh**: ~50-100ms per cycle
- **Chart Rendering**: ~100-200ms
- **Bundle Size**: ~200KB (gzipped)

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

When adding new features:
1. Follow Vue 3 Composition API patterns
2. Use TypeScript for type safety
3. Add proper error handling
4. Ensure responsive design
5. Update this README

## License

Part of the Weather Dashboard project - M24W0295
