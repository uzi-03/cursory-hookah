# Quick Start Guide - Cursory Hookah

Get your hookah gear compatibility app running in minutes!

## Prerequisites

- **Python 3.7+** - [Download here](https://www.python.org/downloads/)
- **Node.js 14+** - [Download here](https://nodejs.org/)
- **npm** (comes with Node.js)

## Quick Setup

1. **Clone and navigate to the project:**
   ```bash
   cd cursory-hookah
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Start the backend:**
   ```bash
   cd backend
   python run.py
   ```
   The Flask API will be available at `http://localhost:5000`

4. **Start the frontend (in a new terminal):**
   ```bash
   cd frontend
   npm start
   ```
   The React app will open at `http://localhost:3000`

## What You'll See

- **Browse All Gear**: View all available hookah products with filtering options
- **My Collection**: Add gear to your personal collection
- **Recommendations**: Get compatible gear suggestions based on your collection

## Sample Data

The app comes pre-loaded with sample hookah gear including:
- Khalil Mamoon and Shika hookahs
- Kaloud and traditional bowls
- Heat management devices
- Various hoses and accessories

## API Endpoints

- `GET /api/gear` - List all gear with optional filters
- `POST /api/user/gear` - Add gear to user collection
- `GET /api/user/gear` - Get user's gear collection
- `GET /api/recommendations` - Get compatible recommendations
- `POST /api/scraper/trigger` - Trigger product scraping

## Next Steps

- Add more product data through the scraper
- Implement user authentication
- Add advanced filtering and sorting
- Integrate with real hookah retailer APIs

## Troubleshooting

**Backend won't start:**
- Make sure Python 3.7+ is installed
- Install dependencies: `pip install -r backend/requirements.txt`

**Frontend won't start:**
- Make sure Node.js 14+ is installed
- Install dependencies: `cd frontend && npm install`

**Database issues:**
- The SQLite database will be created automatically
- Sample data is loaded on first run

## Development

- Backend: Flask with SQLAlchemy and SQLite
- Frontend: React with TypeScript
- API: RESTful endpoints with JSON responses
- Database: SQLite (can be easily migrated to PostgreSQL/MySQL) 