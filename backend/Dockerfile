# Use official Node.js LTS Alpine image for a small footprint
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first for layer caching
COPY package*.json ./

# Install only production dependencies (skip devDependencies like nodemon)
RUN npm install --omit=dev

# Copy the rest of the application source
# .dockerignore ensures .env, node_modules, and .git are excluded
COPY . .

# Expose the application port
EXPOSE 5000

# Start the server with node (not nodemon) for production
CMD ["node", "server.js"]
