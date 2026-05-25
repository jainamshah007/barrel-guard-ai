# =============================================================
# BARREL-GUARD AI — Foreign Object Detection Platform
# Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
# Unauthorized copying, modification, or distribution of
# this file, via any medium, is strictly prohibited.
# =============================================================

FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

