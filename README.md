# currency_converter
A program that makes a simple API call to get exchange rates and converts an amount from one currency to another.

Exchange rates come from https://www.exchangerate-api.com/docs/free

usage: currency_converter.py [-h] [-a AMOUNT] [-i INPUT_CURR] [-o OUTPUT_CURR] [-v VERBOSITY]

options:
  -h, --help            show this help message and exit
  -a, --amount AMOUNT   Amount to convert
  -i, --input_curr INPUT_CURR
                        Currency to convert from
  -o, --output_curr OUTPUT_CURR
                        Currency to convert to
  -v, --verbosity VERBOSITY
                        Control amount of output. Values can be 0 or more
