import json

def write_json_list_start(file):
    file.write('[\n')

def write_json_list_end(file):
    file.write('\n]')

def write_json_entry(file, data, is_first_entry):
    if not is_first_entry:
        file.write(',\n')
    json.dump(data, file, indent=4, ensure_ascii=False)
