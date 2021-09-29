import requests


def get_rates(current, desired):
    global cache
    request = requests.get("https://www.floatrates.com/daily/" + current + ".json")
    currency_rates = request.json()
    cache[desired] = currency_rates[desired]["rate"]


cache = {}
current_cur = input().lower()
if current_cur != "usd":
    get_rates(current_cur, "usd")
if current_cur != "eur":
    get_rates(current_cur, "eur")

while 1:
    desired_cur = input().lower()
    if not desired_cur:
        break
    amount = float(input())

    print("Checking the cache...")
    if desired_cur in cache:
        print("Oh! It is in the cache!")
    else:
        print("Sorry, but it is not in the cache!")
        get_rates(current_cur, desired_cur)
    amount *= cache[desired_cur]
    print("You received", round(amount, 2), desired_cur.upper() + ".")
