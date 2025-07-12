# Cursory Hookah - Gear Compatibility & Discovery

A web application for hookah enthusiasts to discover compatible gear and accessories for their setup.

## Features

- **Gear Compatibility Engine**: Find compatible accessories for your hookah setup
- **Product Database**: Comprehensive catalog of hookah products with specifications
- **Smart Recommendations**: AI-powered suggestions based on your current gear
- **User Profiles**: Save your gear collection and preferences
- **Product Scraping**: Automated product data collection from hookah retailers

## Tech Stack

- **Backend**: Flask (Python) with SQLite database
- **Frontend**: React with TypeScript
- **Data Scraping**: BeautifulSoup for product parsing
- **API**: RESTful endpoints for gear management and recommendations

## Project Structure

```
cursory-hookah/
├── backend/                 # Flask API server
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── scrapers/       # Product scraping
│   ├── requirements.txt
│   └── run.py
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API calls
│   │   └── types/          # TypeScript definitions
│   ├── package.json
│   └── public/
└── data/                   # Database and sample data
```

## Getting Started

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `GET /api/gear` - List all available gear
- `POST /api/user/gear` - Add gear to user collection
- `GET /api/user/gear` - Get user's gear collection
- `GET /api/recommendations` - Get compatible recommendations
- `POST /api/scrape` - Trigger product scraping (admin)

## Development Roadmap

- [x] Basic project structure
- [x] Flask backend with SQLite
- [x] React frontend
- [x] Product database models
- [x] Compatibility engine
- [ ] User authentication
- [ ] Advanced filtering
- [ ] Product reviews integration
- [ ] Price tracking
- [ ] Mobile responsive design
