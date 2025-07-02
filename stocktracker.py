import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from google import genai
from google.genai import types

API_KEY = os.environ.get("API_KEY")

GENAI_KEY = os.environ.get("GENAI_KEY")


def mode_selector():
    print("\nSelect a mode:")
    print("1 - View stock information")
    print("2 - Compare two stocks")
    return input("Enter 1 or 2: ")

def mode1 ():
    stock = input("Enter stock symbol: ").upper()
    df = stock_data(stock)
    query(df)
    print(genai_analysis(stock))


def mode2():
    stock1 = input("Enter the first Stock Symbol : ")
    stock2 = input("Enter the first Stock Symbol : ")
    
    df1 = stock_data(stock1)
    df2 = stock_data(stock2)

    avg1 = df1["4. close"].mean()
    avg2 = df2["4. close"].mean()

    high1 =df1["4. close"].max()
    high2 = df2["4. close"].max()

    print("\n AVERAGE")
    print(f"The average of {stock1}: {avg1}")
    print(f"The average of {stock2}: {avg2}")
    print("\n HIGH")
    print(f"The high of {stock1}: {high1}")
    print(f"The high of {stock2}: {high2}")

    print("\n INVESTMENT TIP")
    if avg1 > avg2:
        print(f"{stock1} had a greater average then {stock2}, seems to be more stable")
    else:
        print(f"{stock2} had a greater average then {stock1}, seems to be more stable")



def stock_data(stock):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json().get("Time Series (Daily)", {})
    df = (
        pd.DataFrame.from_dict(data, orient="index")
          .astype(float)
          .rename_axis("date")           
    )
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=False).head(7)

    return df


def genai_analysis(stock):
    # Create an genAI client using the key from our environment variable
    print()
    print(f'Loading Information about {stock} stock ....')
    client = genai.Client(
        api_key=GENAI_KEY,
    )
    # Specify the model to use and the messages to send
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        system_instruction="You are a financial journalist summarizing stock trends for people with little to no background of the topic.",
        ),
        contents=f"Write a brief sentiment analysis on the stock {stock}., clearly state the Pros and Cons, make sure to use words that a beginer would understand, limit the information"
    )
    return response.text

def query(df):
    print("\nWhat would you like to know?")
    print("1. View closing prices")
    print("2. View average closing price")
    print("3. View highest and lowest closing prices")
    print("4. View the past 7 days")
    choice = input("Enter a number (1–4): ")

    if choice == "1":
        print(df["4. close"])

    elif choice == "2":
        avg = df["4. close"].mean()
        print(f"Average closing price: {avg:.2f}")

    elif choice == "3":
        high = df["4. close"].max()
        low = df["4. close"].min()
        print(f"Highest closing price: {high}")
        print(f"Lowest closing price: {low}")
    elif choice == "4":
        print(df)
    else:
        print("Invalid choice.")    

if __name__== "__main__":
    # stock = input("Enter Stock symbol to fetch data : ")
    # df = stock_data(stock)
    # query(df)
    # print(genai_analysis(stock))
    mode = mode_selector()
    if mode == "1":
        mode1()
    elif mode == "2":
        mode2()
    else:
        print("Invalid selection.")