from typing import List

import requests


def parse_csv(input_data: str) -> List[dict]:
    """
    Process CSV file and return each row as dict...

    Note:
        This function assumes header as a first line

    :param input_data:
    :return:
    """
    lines = input_data.splitlines()
    if len(lines) < 1:
        raise ValueError("CSV is empty")

    headers = lines[0].split(',')

    out = []
    for line in lines[1:]:
        elements = line.split(',')
        out.append(dict(zip(headers, elements)))

    return out


def split_price_literal(price):
    if price[-3:] == "PLN":
        value, currency = price[:-3], price[-3:]
        return int(value), currency
    raise Exception(f"Unknown currency {price}")


def calculate_total_sum(parsed_csv):
    accumulated_sum = 0
    for row in parsed_csv:
        price = row['price']
        price = split_price_literal(price)
        accumulated_sum += price[0]
    return accumulated_sum


def convert_currency(value: int, source_currency: str, output_currency: str):
    server_response = requests.get(
        "http://www.floatrates.com/daily/{}.json".format(source_currency))
    if server_response.status_code != 200:
        raise Exception(f"Server communication error: {server_response.status_code}")
    currency_json = server_response.json()
    return value * float(currency_json[output_currency.lower()]['rate'])


def main():
    with open('sample.csv', 'r') as fp:
        data = fp.read()

    parsed_csv = parse_csv(data)
    accumulated_sum = calculate_total_sum(parsed_csv)

    print(f"Accumulated price {accumulated_sum} PLN")
    price_in_usd = convert_currency(accumulated_sum,
                                    source_currency="PLN",
                                    output_currency="USD")
    print("Price in USD: {0:.2f}".format(price_in_usd))


if __name__ == '__main__':
    main()
