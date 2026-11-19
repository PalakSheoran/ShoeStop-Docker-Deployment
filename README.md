# ShoeStop – MERN Stack Application Containerization Using Docker and Cloud Deployment 👟

A production-ready full-stack **MERN** (MongoDB, Express, React, Node.js) e-commerce web application for footwear, containerized with **Docker** and **Docker Compose**, served via **Nginx** reverse proxy/web server, and architected for seamless cloud deployment on **Render**.

---

## 🏗️ Architecture Overview

The system architecture implements a decoupled three-tier microservice model running within an isolated Docker bridge network:

```
+-----------------------------------------------------------------------------------------+
|                                    Docker Network                                       |
|                                (shoestop-network / bridge)                              |
|                                                                                         |
|  +--------------------------+     HTTP API      +-----------------------------------+   |
|  |    shoestop-frontend     | ----------------> |         shoestop-backend          |   |
|  |     (nginx:alpine)       |  (JSON over REST) |         (node:18-alpine)          |   |
|  |                          |                   |                                   |   |
|  |  * React 18 / Vite SPA   |                   |  * Express.js REST API            |   |
|  |  * Multi-stage build     |                   |  * Port 5000 (Healthcheck: /health|   |
|  |  * Port 80 -> Host 3000  |                   |  * JWT Auth & CORS Configured     |   |
|  +-------------+------------+                   +-----------------+-----------------+   |
|                |                                                  |                     |
+----------------|--------------------------------------------------|---------------------+
                 |                                                  |
           Browser Client                                   Mongoose Connection
         http://localhost:3000                                      |
                                                 +------------------+------------------+
                                                 |                                     |
                                      (Local Environment)                    (Cloud Deployment)
                                                 v                                     v
                                    +--------------------------+          +-------------------------+
                                    |     shoestop-mongodb     |          |      MongoDB Atlas      |
                                    |        (mongo:6.0)       |          |      (Cloud Database)   |
                                    |  Volume: mongo-data:/db  |          |  mongodb+srv://...      |
                                    +--------------------------+          +-------------------------+
```

---

## 💻 Technology Stack

| Layer | Component | Version | Description |
|---|---|---|---|
| **Frontend** | React.js + Vite | React 18, Vite 4 | Single Page Application with dynamic API discovery |
| **Styling** | Bootstrap / React-Bootstrap | 5.3 / 2.8 | Responsive UI components, product cards, cart views |
| **Web Server** | Nginx | Alpine 1.25+ | High-performance static web server & SPA fallback router |
| **Backend** | Express.js / Node.js | Node 18 LTS | RESTful microservice handling products, cart, auth |
| **Authentication** | JWT & Bcrypt | 9.0 / 5.1 | JSON Web Token stateless authentication & password hashing |
| **Database** | MongoDB | 6.0 / Atlas | Document-based persistence with Mongoose ODM & auto-seeding |
| **Containerization** | Docker | 20.10+ | Multi-stage Dockerfiles for minimal, secure image footprints |
| **Orchestration** | Docker Compose | v2+ | Multi-container coordination with automated health checks |
| **Cloud Platform** | Render | Docker Native | Automated cloud container deployment with Render Blueprint |

---

## 📁 Repository Structure

```
ShoeStop-Docker-Deployment/
├── .env.example                               # Template environment variable file
├── .gitignore                                 # Git ignore rules for node_modules, .env, dist
├── docker-compose.yml                         # 3-tier multi-container orchestration definition
├── render.yaml                                # Automated Render Cloud Blueprint specification
├── README.md                                  # Complete technical documentation
│
├── backend/
│   ├── Dockerfile                             # Lightweight Node.js 18 Alpine production container
│   ├── .dockerignore                          # Excludes node_modules, secrets, git metadata
│   ├── server.js                              # Express application entry point & DB connector
│   ├── package.json                           # Dependencies & startup scripts
│   ├── controllers/                           # Business logic for products, cart, wishlist, auth
│   ├── db/                                    # Mongoose connection logic
│   ├── middlewares/                           # JWT verification middleware
│   ├── modal/                                 # Mongoose Schemas (User, Product, Cart, Fav)
│   └── routes/                                # Express API route declarations
│
└── frontend/
    ├── Dockerfile                             # Multi-stage build (Node builder -> Nginx Alpine)
    ├── .dockerignore                          # Excludes node_modules, build artifacts, env files
    ├── nginx.conf                             # Nginx configuration for React SPA routing
    ├── package.json                           # Frontend dependencies & Vite scripts
    ├── vite.config.js                         # Vite build configuration
    ├── index.html                             # Application HTML template
    └── src/
        ├── config.js                          # Centralized dynamic API base URL resolver
        ├── App.jsx                            # Root component with routing
        ├── main.jsx                           # Application bootstrap
        └── component/                         # Navbar, Banner, Product, Cart, Wishlist, Auth
```

---

## ⚙️ Environment Variables Reference

| Variable | Target | Purpose | Local Default | Production Example |
|---|---|---|---|---|
| `port` / `PORT` | Backend | Internal listening port | `5000` | `5000` |
| `mongoURI` / `MONGO_URI` | Backend | MongoDB connection string | `mongodb://mongodb:27017/shoestop` | `mongodb+srv://user:pass@cluster.mongodb.net/shoestop` |
| `JWT_SECRET` | Backend | Secret key for signing auth tokens | `shoestop_jwt_secret_key_2026` | High-entropy random secret |
| `expiry` | Backend | Token validity duration | `30d` | `30d` |
| `VITE_API_URL` | Frontend | Backend public API endpoint | `http://localhost:5000` | `https://shoestop-backend.onrender.com` |

---

## 🚀 Quick Start — Local Docker Deployment

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (running with WSL2 or Hyper-V)
- [Git](https://git-scm.com/)

### 2. Setup Environment
```bash
# Clone the repository
git clone https://github.com/PalakSheoran/ShoeStop-Docker-Deployment.git
cd ShoeStop-Docker-Deployment

# Create local environment file from template
cp .env.example .env
```

### 3. Build & Run with Docker Compose
```bash
docker compose up --build
```

### 4. Access the Application
- **Frontend Web UI**: [http://localhost:3000](http://localhost:3000)
- **Backend API Root**: [http://localhost:5000](http://localhost:5000)
- **Backend Healthcheck**: [http://localhost:5000/health](http://localhost:5000/health)
- **Products API**: [http://localhost:5000/api/getproducts](http://localhost:5000/api/getproducts)

---

## ☁️ Cloud Deployment on Render (1-Click Blueprint)

This project includes a native `render.yaml` infrastructure-as-code file for 1-click cloud deployment.

### Steps:
1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** > **Blueprint**.
3. Connect your GitHub repository: `PalakSheoran/ShoeStop-Docker-Deployment`.
4. Enter your **MongoDB Atlas Connection String** when prompted for `mongoURI`.
5. Click **Apply**.
6. Render will automatically:
   - Build the backend Docker container and expose port `5000`.
   - Build the frontend multi-stage Docker container with Nginx.
   - Automatically inject the public backend URL into the frontend build via `fromService`.
   - Provide public URLs with free SSL/TLS certificates!

---

## 🧪 Verification & API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/` | API status check | No |
| `GET` | `/health` | Container healthcheck probe | No |
| `GET` | `/api/getproducts` | Fetch all available footwear items | No |
| `POST` | `/api/addproduct` | Seed or add footwear items | No |
| `POST` | `/signup` | Register a new user | No |
| `POST` | `/login` | Authenticate user & issue JWT | No |
| `GET` | `/api/addcart` | Retrieve user cart items | Yes (`Bearer <token>`) |
| `POST` | `/api/addcart` | Add product to user cart | Yes (`Bearer <token>`) |
| `DELETE`| `/api/addcart/:id` | Remove item from cart | No |
| `GET` | `/api/addfav` | Retrieve user wishlist items | Yes (`Bearer <token>`) |
| `POST` | `/api/addfav` | Add product to wishlist | Yes (`Bearer <token>`) |

---

## 🛡️ Security Implementation
- **Zero Secret Baking**: Sensitive credentials (`mongoURI`, `JWT_SECRET`) are strictly passed via environment variables at runtime and never embedded in Docker images.
- **Dockerignore Hardening**: `.dockerignore` files prevent local `.env` files, build caches, and `.git` trees from being included in image layers.
- **Non-Root Nginx**: Nginx runs in production on port 80 with immutable static asset caching for optimal security and performance.
