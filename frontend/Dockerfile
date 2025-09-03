# # --- build stage ---
#     FROM node:20-alpine AS build
#     WORKDIR /app
    
#     # install deps
#     COPY package*.json ./
#     RUN npm ci
    
#     # build
#     COPY . .
#     # Vite/CRA both use "npm run build" by default — adjust if yours differs
#     RUN npm run build
    
#     # --- runtime stage: serve static files with nginx ---
#     FROM nginx:1.27-alpine
#     # copy the right build folder:
#     # - Vite defaults to /app/dist
#     # - CRA defaults to /app/build
#     # If you're on CRA, change /app/dist -> /app/build below.
#     COPY --from=build /app/dist /usr/share/nginx/html
    
#     # nginx config: SPA fallback + API proxy to backend
#     COPY nginx.conf /etc/nginx/conf.d/default.conf
    
#     EXPOSE 3000
#     HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
#       CMD wget -qO- http://localhost/ >/dev/null 2>&1 || exit 1
    



# # --- build stage ---
#     FROM node:20-alpine AS build
#     WORKDIR /app
    
#     # install deps
#     COPY package*.json ./
#     # Use --legacy-peer-deps to handle dependency conflicts
#     RUN npm install --legacy-peer-deps
    
#     # build
#     COPY . .
#     # CRA uses "npm run build" and outputs to /build folder
#     RUN npm run build
    
#     # --- runtime stage: serve static files with nginx ---
#     FROM nginx:1.27-alpine
    
#     # CRA builds to /app/build (not /app/dist like Vite)
#     COPY --from=build /app/build /usr/share/nginx/html
    
#     # nginx config: SPA fallback + API proxy to backend
#     COPY nginx.conf /etc/nginx/conf.d/default.conf
    
#     EXPOSE 80
#     HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
#       CMD wget -qO- http://localhost:3000/ >/dev/null 2>&1 || exit 1


# # --- build stage ---
#     FROM node:20-alpine AS build
#     WORKDIR /app
#     COPY package*.json ./
#     RUN npm install --legacy-peer-deps
#     COPY . .
#     RUN npm run build   # CRA -> /app/build
    
#     # --- runtime stage ---
#     FROM nginx:1.27-alpine
#     ARG DEPLOY_TARGET=azure
#     COPY --from=build /app/build /usr/share/nginx/html
#     COPY nginx.conf /etc/nginx/conf.d/default.conf
#     EXPOSE 80
    

# FROM node:20-alpine AS build
# WORKDIR /app
# COPY package*.json ./
# RUN npm install --legacy-peer-deps
# COPY . .
# RUN npm run build

# # --- runtime stage ---
# FROM nginx:1.27-alpine
# ARG DEPLOY_TARGET=azure

# # Install envsubst for environment variable substitution
# RUN apk add --no-cache gettext

# COPY --from=build /app/build /usr/share/nginx/html
# COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# # Set default backend URL (can be overridden)
# ENV BACKEND_URL=https://backend.ashymeadow-e605a82c.uaenorth.azurecontainerapps.io

# EXPOSE 80

# Use nginx's built-in envsubst functionality
# CMD ["nginx", "-g", "daemon off;"]


FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
# use ci if lockfile exists; otherwise install with legacy peer deps
RUN npm ci || npm install --legacy-peer-deps
COPY . .
RUN npm run build   # CRA outputs to /app/build

# --- runtime stage ---
FROM nginx:1.27-alpine
COPY --from=build /app/build /usr/share/nginx/html
# copy our nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80