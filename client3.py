################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import json
import random
import urllib.request

# Server API URL
QUERY = "http://localhost:8080/query?id={}"

# Number of server requests
N = 500

def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    # Corrected price calculation
    price = (bid_price + ask_price) / 2
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None  # Return None if price_b is zero
    return price_a / price_b

# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    for _ in range(N):
        try:
            quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())
        except Exception as e:
            print(f"Error fetching data: {e}")
            continue

        prices = {}
        for quote in quotes:
            try:
                stock, bid_price, ask_price, price = getDataPoint(quote)
                prices[stock] = price
                print(f"Quoted {stock} at (bid: {bid_price}, ask: {ask_price}, price: {price})")
            except KeyError as e:
                print(f"Key error in data: {e}")
            except ValueError as e:
                print(f"Value error in data: {e}")

        if "ABC" in prices and "DEF" in prices:
            ratio = getRatio(prices["ABC"], prices["DEF"])
            print(f"Ratio ABC/DEF: {ratio}")
        else:
            print("Missing data for ABC or DEF.")
