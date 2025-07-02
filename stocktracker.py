import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from google import genai
from google.genai import types

API_KEY = os.environ.get("API_KEY")

GENAI_KEY = "AIzaSyCFqrKH81z6EjJIYpWB3ZFRewYZXf5UTqM"

def stock_data(stock):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json().get("Time Series (Daily)", {})
    df = pd.DataFrame(data)
    return df


def genai_analysis(stock):
    # Create an genAI client using the key from our environment variable
    client = genai.Client(
        api_key=GENAI_KEY,
    )
    # Specify the model to use and the messages to send
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        system_instruction="You are a financial journalist summarizing stock trends for people with little to no background of the topic.",
        ),
        contents=f"Write a brief sentiment analysis for the stock {stock}.",
    )
    return response.text



if __name__== "__main__":
    stock = input("Enter Stock symbol to fetch data : ")
    print(stock_data(stock))
    print(genai_analysis(stock))