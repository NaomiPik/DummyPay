import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://dummypay.vercel.app/"
USER = os.getenv("BACKEND_EMAIL")
PASSWORD = os.getenv("BACKEND_PASSWORD")