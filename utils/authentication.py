import pandas as pd
import hashlib

USER_DATA_FILE = 'data/user_data.csv'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password, role):
    user_data = pd.read_csv(USER_DATA_FILE)
    hashed_password = hash_password(password)
    user = user_data[(user_data['Username'] == username) & (user_data['Password'] == hashed_password) & (user_data['Role'] == role)]
    return not user.empty

def signup_user(name, username, password, role, location):
    user_data = pd.read_csv(USER_DATA_FILE)
    if username in user_data['Username'].values:
        return False
    hashed_password = hash_password(password)
    new_user = pd.DataFrame([[name, username, hashed_password, role, location]], columns=['Name', 'Username', 'Password', 'Role', 'Location'])
    user_data = pd.concat([user_data, new_user], ignore_index=True)
    user_data.to_csv(USER_DATA_FILE, index=False)
    return True