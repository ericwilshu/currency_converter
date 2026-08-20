#!/usr/bin/env python3

# Currency Converter
# by Eric Shumaker
# A program that makes a simple API call to get exchange rates and converts an amount from one currency to another.
# Exchange rates come from https://www.exchangerate-api.com/docs/free

import sys
import requests
import json
import time
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--amount", type=float, help="Amount to convert")
parser.add_argument("-i", "--input_curr", help="Currency to convert from")
parser.add_argument("-o", "--output_curr", help="Currency to convert to")
parser.add_argument("-v", "--verbosity", type=int, default=0, help="Control amount of output. Values can be 0 or more")
args = parser.parse_args()

# Where USD is the base currency you want to use
url = "https://open.er-api.com/v6/latest/USD"
filename = "rates.json"

if args.amount == None:
    curr_amnt = 0.0
else:
    curr_amnt = args.amount

country1 = args.input_curr.upper()
country2 = args.output_curr.upper()


def get_rates(url, filename):
    """
    Makes request to url, writes returned JSON to filename
    url: the url of the api
    filename: the name of the file to cache the data in
    """
    response = requests.get(url)
    fout = open(filename, "w")
    fout.write(response.text)
    fout.close()


def get_rates_dict(filename):
    """
    Reads the cache file if it exists and returns the JSON as a dictionary
    filename: the name of the file the currency data is cached in
    Returns: a dict with currency conversion data
    """
    fin = open(filename, "r")
    rates_str = fin.read()
    fin.close()
    rates_dict = json.loads(rates_str)
    return rates_dict


# check if rates.json already exists. If not, get it.
if not Path(filename).exists():
    if args.verbosity >= 2:
        print("rates.json not found...")
        print("retrieving data...")
    get_rates(url, filename)

# get the JSON data as a dictionary
rates_dict = get_rates_dict(filename)

# check if time to next update has passed. If so, get new data.
if rates_dict["time_next_update_unix"] < time.time():
    if args.verbosity >= 2:
        print("rates.json out of date...")
        print("retrieving data...")
    get_rates(url, filename)

# get the JSON data as a dictionary, again...
rates_dict = get_rates_dict(filename)

# get the conversion rate out of the dictionary
# if either currency code is not in the dictionary, exit.
try:
    country1_rate = rates_dict["rates"][country1]
except KeyError:
    if args.verbosity >= 1:
        print(f"{country1} is not a valid currency code.")
    sys.exit()
try:
    country2_rate = rates_dict["rates"][country2]
except KeyError:
    if args.verbosity >= 1:
        print(f"{country2} is not a valid currency code.")
    sys.exit()

# do the calculation...
conv_amnt = (country2_rate / country1_rate) * curr_amnt

# print the results
if args.verbosity >= 1:
    print(f"{curr_amnt:.2f} {country1} = {conv_amnt:.2f} {country2}")
else:
    print(f"{conv_amnt:.2f}")
