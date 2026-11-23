import requests
from config import SUPABASE_URL, SUPABASE_ANON_KEY

HEADERS = {"apikey": SUPABASE_ANON_KEY, "Content-Type": "application/json"}


def get_session(email, password):
    r = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers=HEADERS, json={"email": email, "password": password})
    r.raise_for_status()
    return r.json()


def set_password(access_token, new_password):
    r = requests.put(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={**HEADERS, "Authorization": f"Bearer {access_token}"},
        json={"password": new_password})
    r.raise_for_status()