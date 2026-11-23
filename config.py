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