# Future plans with AI:
# A setting generator.
# an intelligent adventure writer.
# Every Scene Type intelligent interpreter
# Something that finds out if secrets have been told.


import openai
import random
import jsonlines
import adventure_structure
import os
import json

# openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = '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'
# model = 'ada:ft-personal-2022-11-27-20-21-30'
# old fine tuned model = 'ada:ft-personal-2022-11-27-17-16-21'


def main():
    # write_to_json()
    # test()
    adventure, conditions = adventure_structure.the_drowned_aboleth()
    play(adventure, conditions=conditions)
    pass


def write_to_json():
    path = 'C:\\Users\\thede\\PycharmProjects\\Roleplay-with-AI\\'
    documents = []
    for i in os.listdir(path):
        if i.endswith('.jsonl'):
            documents.append(i)
    full_dict = {}
    for i in documents:
        file_dict = {}
        with jsonlines.open(i, 'r') as reader:
            for j in reader:
                file_dict.update(j)
        full_dict.update({i[:-6]: file_dict})
    with open('out.json', 'w') as out_file:
        json.dump(full_dict, out_file)


def get_type_list():
    type_list = []
    lines = {}
    with jsonlines.open('master_types.jsonl', 'r') as master_types:
        for line in master_types.iter(type=dict):
            lines.update(line)
    for i in lines.keys():
        type_list.append(i.lower())
    lines = {}
    with jsonlines.open('abilities.jsonl', 'r') as abilities:
        for line in abilities.iter(type=dict):
            lines.update(line)
    for i in lines.keys():
        type_list.append('action ability '+i.lower())
    return type_list


def write_master_types():
    master_types = {
        'info question': info_question, 'action other': action_other, 'action speech': action_speech,
        'action change room': action_change_room, 'action start a fight': action_start_a_fight,
        'action end a fight': action_end_a_fight, 'action conversation': action_conversation,
        'action end a conversation': action_end_a_conversation
    }
    x = []
    for i in master_types.keys():
        x.append({i: i.replace(' ', '_')})
    with jsonlines.open('master_types.jsonl', 'w') as writer:
        writer.write_all(x)


def test():
    print('1st Test: An ever-changing test dialogue:')
    prompt = 'The following is a dialogue between a pair of star crossed lovers.'
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=1, max_tokens=100)
    response = response['choices'][0]['text']
    print(response)
    print('End of first test.')
    print('Test: classification of input.')
    response = input('')
    response = classify(response, analyse=True)
    print(response)
    print('End of test.')


def play(adventure, conditions=None, analyse=True):
    if conditions is None:
        conditions = [None, [None]]
    former_scenes = []
    a = None
    running_adventure = True
    while running_adventure:
        scene = adventure_structure.get_next_scene(
            adventure=adventure, all_former_scenes=former_scenes, conditions=conditions
        )
        if analyse:
            print(scene.type)
            print('location: ' + scene.location.name)
            print('amount of npcs: ' + str(len(scene.npcs)))
            for j in scene.npcs:
                print('NPC: ' + j.name)
            print('amount of secrets: ' + str(len(scene.secrets)))
            for j in scene.secrets:
                print('Secret: ' + j.name)
        object_of_interest = scene.location
        running_scene = True
        params = {'object_of_interest': object_of_interest, 'scene': scene, 'adventure': adventure, 'a': a,
                  'running_scene': running_scene, 'conditions': conditions, 'running_adventure': running_adventure}
        params = check_for_trigger(params)
        object_of_interest = params["object_of_interest"]
        scene = params["scene"]
        adventure = params["adventure"]
        a = params["a"]
        running_scene = params["running_scene"]
        conditions = params["conditions"]
        running_adventure = params["running_adventure"]
        description = scene.location.describe(npcs=scene.npcs)
        print(description)
        while running_scene:
            a = input('<please enter:>')
            sort = classify(a, analyse)
            master_types = {}
            with jsonlines.open('master_types.jsonl', 'r') as reader:
                for line in reader.iter(type=dict):
                    master_types.update(line)
            if sort in master_types.keys():
                params = {'object_of_interest': object_of_interest, 'scene': scene, 'adventure': adventure, 'a': a,
                          'running_scene': running_scene, 'conditions': conditions, 'sort': sort,
                          'running_adventure': running_adventure}
                result = eval(master_types[sort]+'(**params)')  # Kwargs!!
                result = check_for_trigger(result)
                object_of_interest = result['object_of_interest']
                running_scene = result['running_scene']
                conditions = result['conditions']
            else:
                print('Abilities are not implemented yet.')
                # with open('out.json', 'r') as f:
                #    att = f['abilities'][sort]
                # chance_of_success = 0.5  # chance of success should be dependent on att and player.
        for i in scene.secrets:
            if i.name == "won":
                if i.found:
                    running_adventure = False
        input('End of scene. (Press enter to continue)')


def classify(a, analyse):
    prompt = f'{a}\n\n###\n\n'
    response = openai.Completion.create(model='ada:ft-personal-2022-11-27-20-21-30', prompt=prompt, temperature=0,
                                        max_tokens=12, stop="###")
    response = response['choices'][0]['text']
    if analyse:
        print(f'Classification:{response}')
        yn = input(f'Is this correct? [Y/n]').lower()
        document = ''
        if yn == '':
            document = 'inputs_unknown.jsonl'
        elif yn[0] == 'y':
            document = 'inputs_correct.jsonl'
            # If not an ability yet, create a new one. !
        elif yn[0] == 'n':
            for i in range(5):
                print(get_type_list())
                response = input(f'Please copy paste the correct type.')
                if response in get_type_list():
                    document = 'inputs_correct2.jsonl'
                    response = ' ' + response
                    break
            if document == '':
                document = 'inputs_incorrect.json'
        else:
            document = 'inputs_unknown.jsonl'
    else:
        document = 'inputs_unknown.jsonl'
    lines = []
    with jsonlines.open(document, 'r') as reader:
        for line in reader:
            lines.append(line)
    prompt_dict = {'prompt': prompt, 'completion': response + '###'}
    lines.append(prompt_dict)
    with jsonlines.open(document, 'w') as writer:
        writer.write_all(lines)
    if response[0] == ' ':
        response = response[1:]
    return response


def check_for_trigger(x):
    for i in x['adventure'].trigger:
        triggered = False
        for j in i.when_triggered:
            if isinstance(j, adventure_structure.SECRET):
                if j.found:
                    triggered = True
            if isinstance(j, adventure_structure.NPC):
                if j in x['scene'].npcs:
                    triggered = True
            if isinstance(j, adventure_structure.LOCATION):
                if x['scene'].location == j:
                    triggered = True
        if triggered:
            x = i.function(x)
    return x


def who(a, scene):
    names = {scene.npcs[0].name: scene.npcs[0]}
    names_str = scene.npcs[0].name
    for i in scene.npcs[1:]:
        names.update({i.name: i})
        names_str = f'{names_str}, {i.name}'
    prompt = f'Who of the following people is meant by the statement? It could be {names}\n\nStatement: {a}\nPerson: '
    response = openai.Completion.create(model='text-davinci-002', prompt=prompt, temperature=0, max_tokens=12,
                                        stop="###")
    response = response['choices'][0]['text']
    if response in names.keys():
        return names[response]
    else:
        return 'could not find'


def where(a, adventure):
    names = {}
    names_str = ''
    for i in adventure.major_locations:  # Why only the major_locations?
        if i.active:
            names.update({i.name: i})
            names_str = f'{names_str}, {i.name}'
    names_str = names_str[2:]
    prompt = f'Where does the person go to? It could be each of the following: {names_str}\n\nPerson: {a}\nLocation: '
    response = openai.Completion.create(model='text-davinci-002', prompt=prompt, temperature=0, max_tokens=18)
    response = response['choices'][0]['text']
    if response in names.keys():
        return names[response]
    else:
        return 'could not find'


# Now come all the type functions:

def info_question(**kwargs):
    if isinstance(kwargs['object_of_interest'], adventure_structure.NPC):
        print(kwargs['object_of_interest'].talk(kwargs['a']))  # or fight?
    elif isinstance(kwargs['object_of_interest'], adventure_structure.LOCATION):
        print(kwargs['object_of_interest'].describe(kwargs['a']))
    else:
        print('Error action_other')
    return kwargs


def action_other(**kwargs):
    if isinstance(kwargs['object_of_interest'], adventure_structure.NPC):
        secrets = []
        for i in kwargs['scene'].secrets:
            if kwargs['object_of_interest'] in i.where_to_find:
                if random.random() > 0.3:
                    secrets.append(i)
                    i.found = True
                    print(f'(Devtool) You find out the following secret: {i.name}')
        print(kwargs['object_of_interest'].talk(kwargs['a'], secrets=secrets))  # or fight?
    elif isinstance(kwargs['object_of_interest'], adventure_structure.LOCATION):
        secrets = []
        for i in kwargs['scene'].secrets:
            if kwargs['object_of_interest'] in i.where_to_find:
                if random.random() > 0.3:
                    secrets.append(i)
                    i.found = True
                    print(f'(Devtool) You find out the following secret: {i.name}')
        print(kwargs['object_of_interest'].describe(kwargs['a'], secrets=secrets))
    else:
        print('Error action_other')
    return kwargs


def action_speech(**kwargs):
    if not isinstance(kwargs['object_of_interest'], adventure_structure.NPC):
        person = who(kwargs['a'], kwargs['scene'])
        if not isinstance(person, adventure_structure.NPC):
            person = random.choice(kwargs['scene'].npcs)
        print(f'You are talking to {person}.')
        kwargs['object_of_interest'] = person
    secrets = []
    for i in kwargs['scene'].secrets:
        if kwargs['object_of_interest'] in i.where_to_find:
            if random.random() > 0.3:
                secrets.append(i)
                i.found = True
                print(f'(Devtool) You find out the following secret: {i.name}')
    print(kwargs['object_of_interest'].talk(kwargs['a'], secrets=secrets))
    return kwargs


def action_change_room(**kwargs):  # proper kwargs implementation is needed!
    kwargs['conditions'] = [where(kwargs['a'], kwargs['adventure']), [None]]
    kwargs['running_scene'] = False
    return kwargs


def action_start_a_fight(**kwargs):
    print('The ability <action start a fight> is not implemented yet.')
    return kwargs


def action_end_a_fight(**kwargs):
    print('The ability <action end a fight> is not implemented yet.')
    return kwargs


def action_conversation(**kwargs):
    person = who(kwargs['a'], kwargs['scene'])
    if not isinstance(person, adventure_structure.NPC):
        person = random.choice(kwargs['scene'].npcs)
    print(f'You are talking to {person.name}.')
    kwargs['object_of_interest'] = person
    secrets = []
    for i in kwargs['scene'].secrets:
        if kwargs['object_of_interest'] in i.where_to_find:
            if random.random() > 0.3:
                secrets.append(i)
                i.found = True
                print(f'(Devtool) You find out the following secret: {i.name}')
    print(kwargs['object_of_interest'].talk(kwargs['a'], secrets=secrets))
    return kwargs


def action_end_a_conversation(**kwargs):
    print('The ability <action end a conversation> is not implemented yet.')
    return kwargs


if __name__ == '__main__':
    main()
