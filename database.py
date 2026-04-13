import pandas as pd
import os

DB_FILE = "users.csv"

def init_db():
    if not os.path.exists(DB_FILE) or os.stat(DB_FILE).st_size == 0:
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(DB_FILE, index=False)
        print("Database Initialized!")

def signup_user(user, pwd):
    init_db() 
    df = pd.read_csv(DB_FILE)
    if user in df['username'].values:
        return False
    new_data = pd.DataFrame([[user, pwd]], columns=["username", "password"])
    new_data.to_csv(DB_FILE, mode='a', header=False, index=False)
    return True

def login_user(user, pwd):
    init_db()
    df = pd.read_csv(DB_FILE)
    if df.empty:
        return False
    user_record = df[(df['username'] == user) & (df['password'] == pwd)]
    return not user_record.empty