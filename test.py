import json
import jsonlines
import os


def write_to_json():
    # Does not work!!
    path = 'C:\\Users\\thede\\PycharmProjects\\Roleplay-with-AI\\'
    documents = []
    for i in os.listdir(path):
        if i.endswith('.jsonl'):
            documents.append(i)
    print(documents)
    full_dict = {}
    documents = ['abilities.jsonl', 'adventures.jsonl', 'inputs_correct.jsonl', 'inputs_correct2.jsonl', 'inputs_incorrect.jsonl', 'inputs_unknown.jsonl', 'master_types.jsonl', 'sample.jsonl', 'test.jsonl']
    for i in documents:
        file_dict = {}
        with jsonlines.open(i, 'r') as reader:
            for j in reader:
                if i.startswith('input'):
                    file_dict.update({j['prompt']: j['completion']})
                else:
                    file_dict.update(j)
        full_dict.update({i[:-6]: file_dict})
    with open('data.json', 'w') as out_file:
        json.dump(full_dict, out_file)


def write_as_jsonlines(key):
    pass


write_to_json()
