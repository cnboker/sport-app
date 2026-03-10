services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: fitness_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    environment:
      DATABASE_URL: postgresql://admin:${DB_PASSWORD}@db/fitness_db
    depends_on:
      - db

volumes:
  pgdata: