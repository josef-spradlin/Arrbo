# Arrbo — NBA Player Projection Model

Arrbo is a full stack NBA analytics application that projects individual player performance for upcoming games.  
The model estimates Points, Rebounds, Assists, and PRA (Points + Rebounds + Assists) using usage-based modeling and opponent defensive efficiency.
---

## Project Overview

Arrbo generates projections by:

1. Identifying the top five players on each team by Usage Percentage  
2. Evaluating the opponent’s Defensive Efficiency against each player’s position  
3. Applying a weighted calculation to estimate:
   - Points
   - Rebounds
   - Assists
   - PRA (Points + Rebounds + Assists)

The core idea is that higher usage players have more stable and predictable statistical output, which can be adjusted based on matchup difficulty.

---

## Tech Stack

### Backend and Data
- Python
- PostgreSQL
- Docker and Docker Compose
- nba_api
- Selenium
- BeautifulSoup
- psycopg

### Frontend
- Vue 3
- Vite
- TypeScript
- Pinia
- Vue Router
- Tailwind CSS
- DaisyUI
- Axios

---

## Prerequisites

The following must be installed before running the project:

- Git
- Docker Desktop
- Python 3.11 or newer
- Node.js (LTS)

---

## Setup Instructions

Clone the repository and navigate into the project directory:

git clone <repo>

cd Arrbo

Copy-Item .env.example .env
(For Mac/Linux: cp .env.example .env)

Install Python dependencies:

py -m pip install -r requirements.txt

cd ingestion-python

py -m pip install -r requirements.txt

cd ..

Install frontend dependencies:

cd frontend-vue

npm ci

cd ..

## Run the application from the Arrbo root directory by using the run.py script:

Normal start without data ingestion: py run.py up

Start with data ingestion: py run.py up --ingest

Rebuild containers and run ingestion: py run.py up --rebuild --ingest

Stop all running services: py run.py down

Stop all services and reset the database: py run.py down --reset-db




