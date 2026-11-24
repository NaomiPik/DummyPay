import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://dummypay.vercel.app/"
USER = os.getenv("BACKEND_EMAIL")
PASSWORD = os.getenv("BACKEND_PASSWORD")

WALLET_NAMES = {
    "ILS": "Israeli Shekel",
    "EUR": "Euro",
    "USD": "US Dollar",
    "GBP": "British Pound"
}