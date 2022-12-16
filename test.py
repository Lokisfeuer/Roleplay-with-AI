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
            for j in reader.iter(type=dict):
                if i.startswith('input') or i == 'sample.jsonl':
                    file_dict.update({j['prompt']: j['completion']})
                else:
                    file_dict.update(j)
        full_dict.update({i[:-6]: file_dict})
    with open('data.json', 'w') as out_file:
        json.dump(full_dict, out_file, indent=2)


def write_as_jsonlines(key):
    path = 'C:\\Users\\thede\\PycharmProjects\\Roleplay-with-AI\\'
    dicts = []
    with open('data.json') as f:
        data = json.load(f)
    if key.startswith('input') or key.startswith('sample'):
        for i in data[key].keys():
            dicts.append({'prompt': i, 'completion': data[key][i]})
    else:
        dicts.append(data[key])
    with jsonlines.open(f'{key}.jsonl', 'r') as reader:
        for line in reader:
            pass
            # dicts.append(line)
    with jsonlines.open(f'{key}.jsonl', 'w') as writer:
        for i in dicts:
            writer.write(i)
    return f'{key}.jsonl'


def create_newsample(*keys):
    x = []
    for i in keys:
        write_as_jsonlines(i)
        with jsonlines.open(f'{i}.jsonl', 'r') as reader:
            for line in reader.iter(type=dict):
                x.append(line)
    change_types = {' info question###': ' info###', ' action other###': ' action###', ' action change room###': ' room change###', ' action start a fight###': ' fight###', ' action end a fight###': ' action###', ' action conversation###': ' talk###', ' action end a conversation###': ' action###', ' action speech###': 'speech', ' action other secrets###': ' action###'}  # etc.
    for i in x:
        if i['completion'] in change_types.keys():
            i['completion'] = change_types[i['completion']]
        elif i['completion'].startswith(' action ability'):
            i['completion'] = ' action###'
        else:
            print(i['completion'])
    with jsonlines.open('newsample.jsonl', 'w') as writer:
        writer.write(None)
        writer.write_all(x)


# write_to_json()
# write_as_jsonlines('sample')
create_newsample('sample', 'inputs_correct', 'inputs_correct2',)