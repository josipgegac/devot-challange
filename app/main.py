from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user, auth, categories, expenses, database

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Home Budget API")

app.include_router(database.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)

# health check
@app.get("/")
def root():
    return {"status": "ok"}