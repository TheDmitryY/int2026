server:
	uv run uvicorn backend.src.main:app

build:
	 docker build -t betterme:latest -f backend/docker/Dockerfile .
