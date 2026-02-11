import pandas as pd
from pathlib import Path

USERS = Path("users.csv")

def signup(username, password, persona):
    username = username.strip()
    password = password.strip()

    if USERS.exists():
        df = pd.read_csv(USERS, dtype=str)
    else:
        df = pd.DataFrame(columns=["username", "password", "persona"])

    # remove whitespace
    df["username"] = df["username"].str.strip()

    # check duplicate username
    if username in df["username"].values:
        return False

    # add new user
    new_user = pd.DataFrame([{
        "username": username,
        "password": password,
        "persona": persona
    }])

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS, index=False)

    return True


def login(username, password):
    if not USERS.exists():
        return None

    df = pd.read_csv(USERS, dtype=str)

    df["username"] = df["username"].str.strip()
    df["password"] = df["password"].str.strip()

    username = username.strip()
    password = password.strip()

    match = df[
        (df["username"] == username) &
        (df["password"] == password)
    ]

    if match.empty:
        return None

    return match.iloc[0]["persona"]
