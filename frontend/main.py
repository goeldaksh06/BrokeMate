import uvicorn
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime
import time

# Database and Model Imports
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import create_db_and_tables, get_async_session
from models import User, Transaction

# Imports for manual authentication
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware

# --- Simple, Manual Authentication Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "a_very_secret_key_for_your_hackathon" 

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# --- AI Model Setup ---
classifier = None
try:
    from transformers import pipeline
    print("Loading AI classifier model...")
    classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
    print("Model loaded.")
except ImportError:
    print("Transformers library not found. AI classification will be disabled.")

# --- Pydantic Models ---
class UserCreate(BaseModel): email: str; password: str
class UserLogin(BaseModel): email: str; password: str
class TransactionModel(BaseModel): description: str; amount: float
class BudgetModel(BaseModel): amount: float

# --- Server Startup Event ---
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# --- MANUAL AUTHENTICATION ROUTES ---
@app.post("/register")
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    return {"message": "User created successfully"}

@app.post("/login")
async def login(request: Request, user_data: UserLogin, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    request.session['user_id'] = user.id
    return {"message": "Login successful"}

@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logout successful"}

# --- Dependency to get current user from session ---
async def get_current_user(request: Request, session: AsyncSession = Depends(get_async_session)):
    user_id = request.session.get('user_id')
    if not user_id: return None
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# --- FRONTEND SERVING ROUTES ---
@app.get("/", response_class=HTMLResponse)
async def get_dashboard(user: User = Depends(get_current_user)):
    if not user: return RedirectResponse("/login.html")
    with open("index.html", "r") as f: return HTMLResponse(content=f.read())

@app.get("/login.html", response_class=HTMLResponse)
async def get_login_page():
    with open("login.html", "r") as f: return HTMLResponse(content=f.read())

@app.get("/register.html", response_class=HTMLResponse)
async def get_register_page():
    with open("register.html", "r") as f: return HTMLResponse(content=f.read())

# --- PROTECTED API ENDPOINTS ---
@app.get("/summary")
async def get_summary(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    if not user: raise HTTPException(status_code=401)
    result = await session.execute(select(Transaction).where(Transaction.user_id == user.id))
    user_transactions = result.scalars().all()
    total_spent = sum(t.amount for t in user_transactions)
    money_left = user.budget - total_spent
    return { "budget": user.budget, "total_spent": total_spent, "money_left": money_left, "variable_transactions": user_transactions, "user_email": user.email }

@app.post("/transaction")
async def add_transaction(transaction: TransactionModel, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    if not user: raise HTTPException(status_code=401)
    ai_category = "General"
    if classifier:
        categories = ["Food", "Luxury", "Travel", "Utilities", "Shopping", "Education", "Health & Fitness"]
        result = classifier(transaction.description, categories, hypothesis_template="This expense is about {}.")
        ai_category = result['labels'][0]
    
    new_transaction = Transaction(
        description=transaction.description, amount=transaction.amount,
        category=ai_category, user_id=user.id
    )
    session.add(new_transaction)
    await session.commit()
    return new_transaction
    
@app.get("/spending-by-category")
async def get_spending_by_category(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    if not user: raise HTTPException(status_code=401)
    
    result = await session.execute(select(Transaction).where(Transaction.user_id == user.id))
    user_transactions = result.scalars().all()
    
    # --- This is the corrected part ---
    # First, create an empty dictionary
    category_totals = {}
    # Then, loop through the transactions to fill it
    for t in user_transactions:
        category_totals[t.category] = category_totals.get(t.category, 0) + t.amount
    # ------------------------------------
    
    labels = list(category_totals.keys())
    data = list(category_totals.values())
    
    return {"labels": labels, "data": data}

# --- New: Endpoint to update the budget ---
@app.post("/budget")
async def update_budget(budget: BudgetModel, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    if not user: raise HTTPException(status_code=401)
    if budget.amount > 0:
        user.budget = budget.amount
        session.add(user)
        await session.commit()
        return {"message": "Budget updated", "new_budget": user.budget}
    raise HTTPException(status_code=400, detail="Invalid budget amount")

# --- New: Endpoint to delete a transaction ---
@app.delete("/transaction/{transaction_id}")
async def delete_transaction(transaction_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    if not user: raise HTTPException(status_code=401)
    
    result = await session.execute(select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == user.id))
    transaction_to_delete = result.scalar_one_or_none()
    
    if transaction_to_delete is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    await session.delete(transaction_to_delete)
    await session.commit()
    return {"message": "Transaction deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)