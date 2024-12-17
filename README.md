# URL shortener
A simple service for shortening a long URL to a desired length string of symbols (aka short URL). Considers URLs that already exist in DB to avoid redundency and duplicates.

## Used:
- Django
- MongoDB
- Docker

## API Endpoints:
- POST /api/shorten/
- GET /api/{short_url}

## Prequisites
- Docker
- Docker Compose

## Getting Started
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hani-momo/url-shortener-mongo.git
   cd url-shortener-mongo

2. **Create & acrivate virtual env (optional):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
3. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt

4. **Run the Container**
   ```bash
   cd docker
   docker-compose up --build -d

   When done, kill it:
   docker-compose down

## Usage
   ```bash
1. curl -X POST http://localhost:8000/api/shorten/ -H "Content-Type: application/json" -d '{"url": "http://example.com"}'
-> {"shortened_url":"abc123"}
2. curl http://localhost:8000/api/redirect/abc123/
-> {"original_url":"https:/original_url"}
