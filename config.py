import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://dummypay.vercel.app"
VALID_EMAIL   = os.getenv("DUMMYPAY_USER")
VALID_PASSWORD = os.getenv("DUMMYPAY_PASS")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
RESET_USER = os.getenv("RESET_USER")
RESET_PASS = os.getenv("RESET_PASS")
USER = os.getenv("BACKEND_EMAIL")
PASSWORD = os.getenv("BACKEND_PASSWORD")

WALLET_NAMES = {
    "ILS": "Israeli Shekel",
    "EUR": "Euro",
    "USD": "US Dollar",
    "GBP": "British Pound"
}
