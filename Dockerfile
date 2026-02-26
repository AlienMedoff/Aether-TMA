# docker-compose.yml
version: '3.8'
services:
  aether-runtime:
    build: .
    ports: ["8000:8000"]
    volumes: ["./static:/app/static"]
