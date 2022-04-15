import bybit
import sys
from decouple import config

API_KEY = config("API_KEY")
API_SECRET = config("API_SECRET")

try:
    client = bybit.bybit(test=False, api_key=API_KEY, api_secret=API_SECRET)
    print("Logged in successfully!")
except Exception as e:
    print(f'Something went wrong while logging => {e}')
    sys.exit()