from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.auth_utils import get_password_hash
from app.database import engine, Base
from app.models import User, Category, Expense

def rebuild_database(db: Session):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


    db.query(Expense).delete()
    db.query(Category).delete()
    db.query(User).delete()
    db.commit()

    user1 = User(
        username="alice",
        email="alice@example.com",
        password_hash=get_password_hash("password1"),
        balance=1000.0,
    )

    user2 = User(
        username="bob",
        email="bob@example.com",
        password_hash=get_password_hash("password2"),
        balance=1500.0,
    )

    user3 = User(
        username="carol",
        email="carol@example.com",
        password_hash=get_password_hash("password3"),
        balance=2000.0,
    )

    db.add_all([user1, user2, user3])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    db.refresh(user3)

    bob_food = Category(name="Food", user_id=user2.id)
    bob_transport = Category(name="Transport", user_id=user2.id)
    bob_entertainment = Category(name="Entertainment", user_id=user2.id)
    bob_utilities = Category(name="Utilities", user_id=user2.id)

    db.add_all([bob_food, bob_transport, bob_entertainment, bob_utilities])
    db.commit()

    bob_expenses = [
        Expense(amount=23.5, date=datetime.utcnow() - timedelta(days=2), description="Groceries", category_id=bob_food.id, user_id=user2.id),
        Expense(amount=10.0, date=datetime.utcnow() - timedelta(days=1), description="Bus ticket", category_id=bob_transport.id, user_id=user2.id),
        Expense(amount=45.0, date=datetime.utcnow(), description="Cinema", category_id=bob_entertainment.id, user_id=user2.id),
        Expense(amount=70.0, date=datetime.utcnow() - timedelta(days=5), description="Restaurant lunch", category_id=bob_food.id, user_id=user2.id),
        Expense(amount=120.5, date=datetime.utcnow() - timedelta(days=10), description="Electricity bill", category_id=bob_utilities.id, user_id=user2.id),
        Expense(amount=30.0, date=datetime.utcnow() - timedelta(days=4), description="Gasoline", category_id=bob_transport.id, user_id=user2.id),
    ]
    db.add_all(bob_expenses)

    carol_food = Category(name="Food", user_id=user3.id)
    carol_utilities = Category(name="Utilities", user_id=user3.id)
    carol_travel = Category(name="Travel", user_id=user3.id)
    carol_entertainment = Category(name="Entertainment", user_id=user3.id)

    db.add_all([carol_food, carol_utilities, carol_travel, carol_entertainment])
    db.commit()

    carol_expenses = [
        Expense(amount=120.0, date=datetime.utcnow() - timedelta(days=7), description="Restaurant", category_id=carol_food.id, user_id=user3.id),
        Expense(amount=75.5, date=datetime.utcnow() - timedelta(days=3), description="Electricity bill", category_id=carol_utilities.id, user_id=user3.id),
        Expense(amount=340.0, date=datetime.utcnow() - timedelta(days=1), description="Train tickets", category_id=carol_travel.id, user_id=user3.id),
        Expense(amount=50.0, date=datetime.utcnow() - timedelta(days=9), description="Groceries", category_id=carol_food.id, user_id=user3.id),
        Expense(amount=25.0, date=datetime.utcnow() - timedelta(days=2), description="Streaming service", category_id=carol_entertainment.id, user_id=user3.id),
        Expense(amount=400.0, date=datetime.utcnow() - timedelta(days=12), description="Plane tickets", category_id=carol_travel.id, user_id=user3.id),
        Expense(amount=90.0, date=datetime.utcnow() - timedelta(days=5), description="Concert tickets", category_id=carol_entertainment.id, user_id=user3.id),
    ]
    db.add_all(carol_expenses)

    db.commit()
    db.close()

    print("Database seeded successfully!")

