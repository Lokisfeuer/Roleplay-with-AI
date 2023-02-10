import json
import jsonlines
import os
import random
import textwrap
import main
import adventure_structure
import jsonpickle
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')


def write_trainingsdata_for_secretrecognition():
    secrets = [
        "The key to the hidden chamber lies in the darkest corner of the castle.",
        "A powerful magical artifact lies buried in the catacombs beneath the city.",
        "A mysterious stranger holds the knowledge to unlocking the ancient ruins.",
        "An evil cult has been gathering strength deep in the forest.",
        "The final resting place of a powerful mage is hidden in a mountain cave.",
        "An ancient tome holds the secrets to a powerful spell.",
        "A cursed object is hidden in an old temple.",
        "A secret passage leads to the throne room of a long-lost kingdom.",
        "A powerful artifact is hidden in the depths of an underground maze.",
        "The entrance to a mysterious realm lies in a forgotten corner of the world.",
        "A powerful wizard is planning to unleash a great evil upon the world.",
        "An ancient dragon is asleep in a hidden cave, awaiting the day it will be freed.",
        "A lost continent lies beneath the waves, waiting to be discovered.",
        "A powerful weapon lies hidden in the depths of a mysterious temple.",
        "A powerful magical artifact is locked away in a forgotten vault.",
        "A powerful artifact is hidden in the depths of an enchanted forest.",
        "An evil cult is seeking to unlock the secrets of a powerful magical artifact.",
        "A powerful magical artifact lies in the center of a dark and dangerous dungeon.",
        "A powerful artifact lies in the heart of a forbidden city.",
        "A mysterious cult is seeking to awaken a powerful being from its slumber.",
        "A powerful magical artifact is hidden in the deepest part of a cursed forest.",
        "An ancient ritual is needed to unlock the power of a powerful artifact.",
        "A powerful magical artifact is hidden in the depths of the ocean.",
        "An evil sorcerer is plotting to take control of the kingdom.",
        "A powerful magical artifact is locked away in an ancient temple.",
        "An ancient race of creatures is hidden deep in the forest.",
        "A powerful artifact is hidden in an ancient tomb.",
        "A powerful artifact is locked away in a secret chamber.",
        "An ancient and powerful artifact is hidden in an abandoned castle.",
        "A powerful magical artifact is locked away in a forgotten keep.",
        "An evil necromancer is plotting to raise an army of undead.",
        "An ancient artifact is hidden in a temple of forgotten gods.",
        "A powerful magical artifact is hidden in the depths of a forgotten dungeon.",
        "An evil cult is seeking to gain control of a powerful magical artifact.",
        "A powerful magical artifact is hidden in a hidden cavern.",
        "A powerful magical artifact is locked away in a sacred temple.",
        "An ancient ritual is needed to unlock the power of a powerful magical artifact.",
        "A powerful magical artifact is hidden in a secret laboratory.",
        "A powerful magical artifact is hidden in an ancient ruin.",
        "An evil sorcerer is plotting to use a powerful magical artifact to take control of the kingdom.",
    ]
    prompt = ''
    full_dict = {}
    for i in secrets:
        prompt = f'{i}\n\nWrite a persons direct speech telling someone else about this secret indirectly.\n\n"'
        response = openai.Completion.create(model='text-davinci-003', prompt=prompt, temperature=1, max_tokens=250)
        response = response['choices'][0]['text']
        if response[-1] == '"':
            response = response[:-1]
        else:
            print(response)
        for j in secrets:
            if i != j:
                if random.random() > 0.85:
                    full_dict.update({f'Secret: {j}\nText: {response}\n\nAnswer: \n\n###\n\n': 'N###'})
            else:
                full_dict.update({f'Secret: {j}\nText: {response}\n\nAnswer: \n\n###\n\n': 'Y###'})
    with open('data.json') as f:
        data = json.load(f)
    data.update({'secret sample': full_dict})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(write_as_jsonlines('secret sample'))


def write_to_json():  # from jsonlines
    # Does not work!!
    path = 'PATH' # paste path to files
    documents = []
    for i in os.listdir(path):
        if i.endswith('.jsonl'):
            documents.append(i)
    print(documents)
    full_dict = {}
    # documents = ['abilities.jsonl', 'adventures.jsonl', 'inputs_correct.jsonl', 'inputs_correct2.jsonl', 'inputs_incorrect.jsonl', 'inputs_unknown.jsonl', 'master_types.jsonl', 'sample.jsonl', 'test.jsonl']
    for i in documents:
        file_dict = {}
        with jsonlines.open(i, 'r') as reader:
            for j in reader.iter(type=dict):
                if i.startswith('input') or i == 'sample.jsonl' or i.startswith('wh') or i.startswith('new'):
                    file_dict.update({j['prompt']: j['completion']})
                else:
                    file_dict.update(j)
        full_dict.update({i[:-6]: file_dict})
    with open('data.json', 'w') as out_file:
        json.dump(full_dict, out_file, indent=4)


def write_single_file_to_json(file):
    file_dict = {}
    with jsonlines.open(file, 'r') as reader:
        for j in reader.iter(type=dict):
            if file.startswith('input') or file == 'sample.jsonl' or file.startswith('wh') or file.startswith('new') or file.startswith('secret_sample'):
                file_dict.update({j['prompt']: j['completion']})
            else:
                file_dict.update(j)
    with open('data.json', 'r') as f:
        data = json.load(f)
    data.update({file[:-6]: file_dict})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def write_as_jsonlines(key):
    path = 'C:\\Users\\thede\\PycharmProjects\\Roleplay-with-AI\\'
    x = []
    with open('data.json') as f:
        data = json.load(f)[key]
    if isinstance(data, dict):
        for i in data.keys():
            x.append({'prompt': i, 'completion': data[i]})
    else:
        x = data
    with jsonlines.open(f'{key}.jsonl', 'w') as writer:
        for i in x:
            writer.write(i)
    return f'{key}.jsonl'


def rewrite_sec_sample():
    x = []
    with jsonlines.open('secret_sample_prepared.jsonl', 'r') as reader:
        for line in reader:
            new_line = {'prompt': line['prompt'][:-8], 'completion': line['completion']}
            x.append(new_line)
    with jsonlines.open('secret_sample.jsonl', 'w') as writer:
        for i in x:
            writer.write(i)


def create_newsample(*keys):
    x = []
    for i in keys:
        write_as_jsonlines(i)
        with jsonlines.open(f'{i}.jsonl', 'r') as reader:
            for line in reader.iter(type=dict):
                x.append(line)
    change_types = {
        ' info question###': ' info###', ' action other###': ' action###', ' action change room###': ' room change###',
        'action start a fight###': ' fight###', ' action end a fight###': ' action###',
        ' action conversation###': ' talk###', ' action end a conversation###': ' action###',
        ' action speech###': 'speech', ' action other secrets###': ' action###'}
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


def create_who_and_where_dataset():
    '''
I talk to John.


I start a conversation with Daniela.


I go over to Micheal and talk to him.


I greet Albert warmly.


I ask Mary how she's doing.


I chat with Sarah about the latest news.


I inquire of Jeffrey what he's been up to.


I ask Olivia what her plans are for the weekend.


I enquire of Robert what his opinion is on the matter.


I check in with David to see how things are going.


I start a conversation with Karen about the weather.


I talk to Paul about the current situation.


I ask Matthew what his thoughts are on the subject.


I converse with Angela about her day.


I engage in a dialogue with George about the news.


I start up a conversation with Lucas about his hobbies.


I speak to Jack about his plans for the future.


I ask Jenny what she thinks about the issue.


I have a chat with Emma about her favorite books.


I engage in a discussion with Tyler about his experiences.


I have a conversation with Samuel about his favorite movies.
    '''
    pass
    '''
I attack John.


I start a fight with Daniela.


I go over to Micheal and beat him.


I slap Albert.


I throw a punch at Robert.


I kick Tom in the stomach.


I take a swing at Sarah.


I shove Maria.


I punch Paul in the face.


I give Lucas a black eye.


I hit Jordan in the chest.


I elbow Kyle in the ribs.


I pummel Nathan.


I knock out Oliver.


I strike Steve in the jaw.


I elbow Ashley in the face.


I smash William's nose.


I grapple with Victoria.


I tackle Samuel.


I start a fight with Eric.


I throw a punch at Johnathon.
    '''
    data = {'I talk to John.': 'John', 'I start a conversation with Daniela.': 'Daniela',
            'I go over to Micheal and talk to him.': 'Micheal', 'I greet Albert warmly.': 'Albert',
            'I ask Mary how she\'s doing.': 'Mary', 'I chat with Sarah about the latest news.': 'Sarah',
            'I inquire of Jeffrey what he\'s been up to.': 'Jeffrey',
            'I ask Olivia what her plans are for the weekend.': 'Olivia',
            'I enquire of Robert what his opinion is on the matter.': 'Robert',
            'I check in with David to see how things are going.': 'David',
            'I start a conversation with Karen about the weather.': 'Karen',
            'I talk to Paul about the current situation.': 'Paul',
            'I ask Matthew what his thoughts are on the subject.': 'Matthew',
            'I converse with Angela about her day.': 'Angela',
            'I engage in a dialogue with George about the news.': 'George',
            'I start up a conversation with Lucas about his hobbies.': 'Lucas',
            'I speak to Jack about his plans for the future.': 'Jack',
            'I ask Jenny what she thinks about the issue.': 'Jenny',
            'I have a chat with Emma about her favorite books.': 'Emma',
            'I engage in a discussion with Tyler about his experiences.': 'Tyler',
            'I have a conversation with Samuel about his favorite movies.': 'Samuel', 'I attack John.': 'John',
            'I start a fight with Daniela.': 'Daniela', 'I go over to Micheal and beat him.': 'Micheal',
            'I slap Albert.': 'Albert', 'I throw a punch at Robert.': 'Robert', 'I kick Tom in the stomach.': 'Tom',
            'I take a swing at Sarah.': 'Sarah', 'I shove Maria.': 'Maria', 'I punch Paul in the face.': 'Paul',
            'I give Lucas a black eye.': 'Lucas', 'I hit Jordan in the chest.': 'Jordan',
            'I elbow Kyle in the ribs.': 'Kyle', 'I pummel Nathan.': 'Nathan', 'I knock out Oliver.': 'Oliver',
            'I strike Steve in the jaw.': 'Steve', 'I elbow Ashley in the face.': 'Ashley',
            'I smash William\'s nose.': 'William', 'I grapple with Victoria.': 'Victoria', 'I tackle Samuel.': 'Samuel',
            'I start a fight with Eric.': 'Eric', 'I throw a punch at Johnathon.': 'Johnathon'}
    x = []
    for i in data.keys():
        names = random.choices(list(data.values()), k=random.randint(0, 7))
        while data[i] in names:
            names = random.choices(list(data.values()), k=random.randint(0, 7))
        names.append(data[i])
        random.shuffle(names)
        x.append({'prompt': f'{names}\n{i}\n\n###\n\n', 'completion': f' {data[i]}###'})
    data = {
        'I take a trip to the tavern.': 'tavern', 'I set off for the market.': 'market', 'I embark on a journey to '
                                                                                         'the port.': 'port',
        'I head off to the shop.': 'shop', 'I am on my way to the city.': 'city', 'I make my way to the castle.':
            'castle', 'I set out for the dungeon.': 'dungeon', 'I travel to the forest.': 'forest', 'I trek to the '
                                                                                                    'mountains.':
            'mountains', 'I am off to the swamp.': 'swamp', 'I voyage to the desert.': 'desert', 'I make a trip to '
                                                                                                 'the beach.':
            'beach', 'I go to a place in the jungle.': 'jungle', 'I go to a destination in the ocean.': 'ocean',
        'I journey to the river.': 'river', 'I make my way to a place in the sky.': 'sky', 'I take a voyage to the '
                                                                                           'moon.': 'moon',
        'I take a journey to the sun.': 'sun', 'I take off to the stars.': 'stars', 'I am travelling to the galaxy.':
            'galaxy', 'I am journeying to the universe.': 'universe', 'I am headed to the cosmos.': 'cosmos '
    }
    x = []
    for i in data.keys():
        places = random.choices(list(data.values()), k=random.randint(0, 7))
        while data[i] in places:
            places = random.choices(list(data.values()), k=random.randint(0, 7))
        places.append(data[i])
        random.shuffle(places)
        x.append({'prompt': f'{places}\n{i}\n\n###\n\n', 'completion': f' {data[i]}###'})
    with jsonlines.open('wheresample.jsonl', 'w') as writer:
        writer.write_all(x)


def save_game_to_json():
    adventure, conditions = adventure_structure.the_drowned_aboleth()
    game = main.GAME(adventure=adventure, conditions=conditions)
    string = jsonpickle.encode(game)
    print(string)
    g = jsonpickle.decode(string)
    print(g.adventure.major_secrets[0].name)


def rewrite_classifier_sample():
    x = []
    with jsonlines.open('sample.jsonl', 'r') as reader:
        for line in reader:
            x.append(line)
    for line in x:
        if not line['completion'].endswith('###'):
            line['completion'] = f'{line["completion"]}###'
    newlist = sorted(x, key=lambda d: d['completion'])
    with jsonlines.open('sample.jsonl', 'w') as writer:
        writer.write_all(newlist)


# write_to_json()
# write_as_jsonlines('secret sample')
# create_newsample('sample', 'inputs_correct', 'inputs_correct2',)
# write_to_json()
# write_trainingsdata_for_secretrecognition()
# rewrite_sec_sample()
write_single_file_to_json('sample.jsonl')
# rewrite_classifier_sample()