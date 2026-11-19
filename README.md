# ShoeStop 👟

A full-stack **MERN** e-commerce web application for shoes, containerised with **Docker** and served in production via **Nginx**.

---

## Architecture

```
+-------------------------------------------------------------------+
|                         Docker Host                               |
|                                                                   |
|  +--------------------+          +---------------------------+    |
|  | shoestop-frontend  |          |   shoestop-backend        |    |
|  |   (nginx:alpine)   |   HTTP   |   (node:18-alpine)        |    |
|  |                    +--------->+                           |    |
|  |  React/Vite SPA    |          |  Express REST API         |    |
|  |  Port: 80          |          |  Port: 5000               |    |
|  +--------+-----------+          +-------------+-------------+    |
|           | :3000                              |                  |
|           |                                   | mongoose         |
+-----------+-----------------------------------+------------------+
            |                                   |
        Browser                      +----------v---------+
                                     |   MongoDB Atlas    |
                                     |   (Cloud)          |
                                     +--------------------+

Network: shoestop-network (bridge)
```

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | React.js (Vite)                   |
| Styling    | CSS / component styles            |
| Backend    | Node.js + Express.js              |
| Database   | MongoDB Atlas (cloud-hosted)      |
| Auth       | JSON Web Tokens (JWT)             |
| Server     | Nginx (production static serving) |
| Container  | Docker + Docker Compose           |

---

## Project Structure

```
ShoeStop-Docker-Deployment/
+-- docker-compose.yml          # Orchestrates all services
+-- .env                        # Runtime secrets (NOT committed)
+-- .env.example                # Template for .env
+-- .gitignore
+-- README.md
|
+-- backend/
|   +-- Dockerfile              # node:18-alpine, production deps only
|   +-- .dockerignore
|   +-- server.js               # Express entry point (port 5000)
|   +-- package.json
|   +-- routes/
|   +-- models/
|   +-- middleware/
|
+-- frontend/
    +-- Dockerfile              # Multi-stage: Vite build -> nginx serve
    +-- .dockerignore
    +-- nginx.conf              # SPA fallback + cache headers
    +-- src/
    |   +-- config.js           # Central API base URL config
    |   +-- component/
    +-- package.json
    +-- vite.config.js
```

---

## Prerequisites

- **Docker Desktop** >= 4.x  https://www.docker.com/products/docker-desktop/
- **Git**  https://git-scm.com/
- A **MongoDB Atlas** account and cluster (free tier works fine)

---

## Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd ShoeStop-Docker-Deployment

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your actual MongoDB Atlas URI and secrets

# 3. Build and start all containers
docker compose up --build

# 4. Open the app
#    Frontend  -> http://localhost:3000
#    Backend   -> http://localhost:5000
```

> Stop with Ctrl+C, or run `docker compose down` to also remove containers.

---

## Environment Variables

| Variable     | Description                        | Example                                                        |
|--------------|------------------------------------|----------------------------------------------------------------|
| `MONGO_URI`  | MongoDB Atlas connection string    | `mongodb+srv://user:pass@cluster.mongodb.net/shoestop`         |
| `JWT_SECRET` | Secret key used to sign JWT tokens | `a_long_random_string`                                         |
| `JWT_EXPIRY` | Token expiry duration              | `30d`                                                          |

Create a `.env` file at the project root (see `.env.example`):

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRY=30d
```

---

## MongoDB Atlas Setup

1. Sign up / log in at https://cloud.mongodb.com
2. Create a **free M0 cluster**.
3. Under **Database Access**, add a user with read/write permissions.
4. Under **Network Access**, add `0.0.0.0/0` (allow from anywhere) or your server IP.
5. Click **Connect -> Drivers**, copy the connection string and paste it as `MONGO_URI` in `.env`.
6. Replace `<password>` in the string with your database user password.

---

## Docker Commands Reference

```bash
# Start in background (detached)
docker compose up -d --build

# View running containers
docker compose ps

# Stream logs for all services
docker compose logs -f

# Stream logs for one service
docker compose logs -f backend
docker compose logs -f frontend

# Restart a single service
docker compose restart backend

# Stop and remove containers (keeps images)
docker compose down

# Stop, remove containers AND images
docker compose down --rmi all

# Rebuild a single service image
docker compose build backend

# Open a shell inside a container
docker exec -it shoestop-backend sh
docker exec -it shoestop-frontend sh
```

---

## Application URLs

| Service      | URL                        |
|--------------|----------------------------|
| Frontend     | http://localhost:3000       |
| Backend API  | http://localhost:5000       |

---

## Troubleshooting

### Containers exit immediately
```bash
docker compose logs backend
docker compose logs frontend
```
- Ensure `.env` exists and `MONGO_URI` is correct.
- Verify your Atlas cluster is running and network access allows your IP.

### ECONNREFUSED / backend unreachable from browser
- The frontend SPA runs **in the browser**, so API calls go to `localhost:5000`
  (the Docker port-forwarded address), not inside the Docker network. Expected behaviour.

### Port already in use
```bash
# Find what occupies port 5000 or 3000
netstat -ano | findstr :5000
# Change the left-hand port in docker-compose.yml, e.g. "5001:5000"
```

### Image build fails (npm install errors)
- Clear Docker build cache: `docker compose build --no-cache`

### MongoDB authentication failed
- Double-check the username/password in `MONGO_URI`.
- Ensure the Atlas database user has the correct role.

---

## Cloud Deployment (Render)

**Render** is the recommended platform for free-tier cloud hosting.

1. Push your repository to GitHub.
2. Create a **Web Service** on https://render.com for the backend:
   - Build command: `npm install`
   - Start command: `node server.js`
   - Add env vars (`MONGO_URI`, `JWT_SECRET`, `JWT_EXPIRY`) in the Render dashboard.
3. Create a **Static Site** for the frontend:
   - Build command: `npm install && npm run build`
   - Publish directory: `dist`
   - Set `VITE_API_URL` to your Render backend URL (e.g. `https://shoestop-api.onrender.com`).
4. Update MongoDB Atlas **Network Access** to allow Render IPs (or `0.0.0.0/0`).

> **Tip:** Render free tier spins down after 15 min of inactivity. Use an uptime monitor to keep it warm.

---

## License

MIT (c) ShoeStop
