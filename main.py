import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

API_KEY = "49FBIC723MR7ZVFI"
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY,
}
URL = "https://www.alphavantage.co/query"
response = requests.get(url=URL, params=parameters)

print(response.json())
data = response.json()["Time Series (Daily)"]
print(data)


data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
dby_data = data_list[1]
dby_closing_price = float(dby_data["4. close"])

# print(yesterday_closing_price)
# print(dby_closing_price)
positive_diff = abs(yesterday_closing_price - dby_closing_price)

sign = None

if yesterday_closing_price > dby_closing_price:
    sign = "🔺"
else:
    sign = "🔻"

print(positive_diff)

perc_difference = positive_diff / yesterday_closing_price * 100

print(perc_difference)

TWILIO_SID = os.getenv("twilio_sid")
TWILIO_AUTH_TOKEN = os.getenv("twilio_auth")

if perc_difference > 2:

    NEWS_API = "253c78b39b3640c6a0485117e21230c0"
    URL = "https://newsapi.org/v2/everything"

    parameters_news = {
        "q": COMPANY_NAME,
        "language": "en",
        "apiKey": NEWS_API,
    }

    news_response = requests.get(url=URL, params=parameters_news)
    articles = news_response.json()["articles"]
    news = articles[:3]

    formatted_list = [f"{STOCK}: {sign}{int(perc_difference)}%. \nHeadline: {article['title']}. \nBrief: {article['description']}." for article in articles]
    print(formatted_list)

    for formatted in formatted_list:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=formatted,
            from_="+16xxxxxxxxx",
            to="+91xxxxxxxxxx"
        )
        print("message sent")


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

