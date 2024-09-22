import csv
import re

from logic.geocodes import Geocodes
from removes import remove_words_dotted_dict, remove_words_not_dotted_dict


def add_to_dict(d, key):
    if key in d.keys():
        d[key] += 1
    else:
        d[key] = 1


def write_to_file(a):
    with open('result_file.txt', 'a+', encoding='utf-8') as file:
        file.write(a)


def transform_address(address):
    # Regex pattern to capture 'д.' (house), 'к.' (building), and 'стр.' (structure) parts.
    pattern = r'д\.(\d+)(?:,?\s*к\.(\d+))?(?:,?\s*стр\.(\d+))?'

    # Find matches using regex
    match = re.search(pattern, address)

    if match:
        # Extract the captured groups, with defaults for non-existent groups
        house = match.group(1)  # Always exists (house number)
        building = match.group(2) or ''  # May not exist (building number)
        structure = match.group(3) or ''  # May not exist (structure number)

        # Format result: "house" + "k" + "building" + "s" + "structure"
        result = f"{house}{'к' + building if building else ''}{'с' + structure if structure else ''}"
        return result

    # If no match, return original address (or handle differently)
    return address


result_dict = dict()
addresses = []


with open('ТЕСТ_ПОЕЗДОК.csv', newline='', encoding='utf-8') as csvfile:
    # TODO: Поменять название
    reader = csv.DictReader(csvfile, restval=None, restkey=None, delimiter=';')
    for i, row in enumerate(reader):
        cur = row['Адрес проживания']
        cur = cur.replace(',.', '.,')
        old_address = cur
        cur = cur.split(', ')
        cur_parts = []
        if len(cur) > 0 and 'кв' in cur[-1]:
            cur = cur[:-1]

        new_cur = ', '.join(cur)
        if 'д.' in ', '.join(cur):
            house_num = transform_address(new_cur)
            new_cur = re.split(' д.', new_cur)[0]
            new_cur = new_cur + ' ' + house_num
            cur = new_cur.split(', ')

        if not cur[0]:
            continue

        for part in cur:
            words = part.split()
            res_words = []
            for word in words:
                if word[0] == '(' or word[-1] == ')':
                    continue

                for error in remove_words_dotted_dict:
                    if 'проезд' in word:
                        pass
                    ban = re.search(f"^{re.escape(error)}", word)
                    if ban:
                        word = re.sub(f"^{error}", remove_words_dotted_dict[error], word)

                for error in remove_words_not_dotted_dict:
                    ban = re.search(f"^{re.escape(error)}$", word)
                    if ban:
                        word = re.sub(f"^{error}$", remove_words_not_dotted_dict[error], word)

                res_words.append(word)

            cur_parts.append(' '.join(res_words))

        if not cur_parts or len(cur_parts) < 2:
            continue

        if not 'Москва' in cur_parts[1] and not 'Санкт' in cur_parts[1]:
            cur_parts = cur_parts[2:]
        result_address = ', '.join(cur_parts[-2:])
        result_address = result_address.replace('.', '')
        result_address = result_address.replace('  ', ' ')

        # print(f'before - {old_address}; === after - {result_address}')
        addresses.append((old_address, result_address))

idx = 0
for address in addresses:
    idx += 1
    coords = Geocodes().get_coords_from_address(address[1])
    if coords == (None, None):
        error_string = f'ERROR: {address[0]} ================ {address[1]}\n'
        print(error_string)
        write_to_file(error_string)

    if idx % 100 == 0:
        print(f'=================== {idx} ====================')
