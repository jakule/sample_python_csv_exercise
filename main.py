from typing import List

# list - []
# dict {}
# tuple ()


def parse_csv(input_data: str) -> List[dict]:
    """
    Process CSV file and return each row as dict...

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


def main():
    with open('sample.csv', 'r') as fp:
        data = fp.read()
    # print(data)
    parsed_csv = parse_csv(data)
    # print(parsed_csv)

if __name__ == '__main__':
    main()
