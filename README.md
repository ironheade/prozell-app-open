## ProZell Kostenrechner

Installation ohne Docker:

Vorraussetzungen: Python & Node (Yarn)

Installation (in CMD Fenster)

1. in package.json, change   "proxy": "http://backend:5000" to   "proxy": "http://localhost:5000"
2. ~/prozell-app yarn install
3. ~/prozell-app npm run build-api

Start (In separaten CMD Fenstern)

1. ~/prozell-app yarn start
2. ~/prozell-app yarn start-api

Installation mit Docker:

Installation (in CMD Fenster)

1. in package.json, change   "proxy": "http://localhost:5000" to   "proxy": "http://backend:5000"
2. ~/prozell-app docker build -t ironheade/prozell-frontend
3. ~/prozell-app/api docker build -t ironheade/prozell-backend

Start (in CMD Fenster)

1. ~/prozell-app docker-compose up
