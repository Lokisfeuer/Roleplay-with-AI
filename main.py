# Future plans with AI:
# A setting generator.
# an intelligent adventure writer.
# Every Scene Type intelligent interpreter
# Something that finds out if secrets have been told.

# next steps:
# commands: take back, inventory and secrets, hint, help, /mastertype a, describe scene (analyse)
# 1 and only 1 input spot.
# implement the new models

import openai
import random
import adventure_structure
import os
import json
import jsonlines

# openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = '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'
# model = 'ada:ft-personal-2022-11-27-20-21-30'
# old fine tuned model = 'ada:ft-personal-2022-11-27-17-16-21'
# model = ada:ft-personal:input-classifier-2022-12-17-07-32-32
# wheremodel = curie:ft-personal:where-2022-12-17-23-05-15
# whomodel = curie:ft-personal:who-2022-12-17-23-11-02


def main():
    # write_to_json()  # Error!
    # test()
    adventure, conditions = adventure_structure.the_drowned_aboleth()
    GAME(adventure=adventure, conditions=conditions).play()
    pass


class GAME:
    def __init__(self, object_of_interest=None, scene=None, adventure=None, a=None, running_scene=None, conditions=None, running_adventure=True, former_scenes=None, sort=None):
        if conditions is None:
            self.conditions = [None, [None]]
        else:
            self.conditions = conditions
        if former_scenes is None:
            self.former_scenes = []
        else:
            self.former_scenes = former_scenes
        self.object_of_interest = object_of_interest
        self.scene = scene
        self.adventure = adventure
        self.a = a
        self.running_scene = running_scene
        self.running_adventure = running_adventure
        self.former_scenes = former_scenes
        self.sort = sort

    def check_for_trigger(self):
        if self.a.startswith('/') or self.a.startswith('\\'):
            pass
        for i in self.adventure.trigger:
            triggered = False
            for j in i.when_triggered:
                if isinstance(j, adventure_structure.SECRET):
                    if j.found:
                        triggered = True
                if isinstance(j, adventure_structure.NPC):
                    if j in self.scene.npcs:
                        triggered = True
                if isinstance(j, adventure_structure.LOCATION):
                    if self.scene.location == j:
                        triggered = True
            if triggered:
                return i.function(self)  # if an error is triggered add a try except.

    def play(self, analyse=True):
        while self.running_adventure:
            self.scene = adventure_structure.get_next_scene(
                adventure=self.adventure, all_former_scenes=self.former_scenes, conditions=self.conditions
            )
            if analyse:
                print(self.scene.type)
                print('location: ' + self.scene.location.name)
                print('amount of npcs: ' + str(len(self.scene.npcs)))
                for j in self.scene.npcs:
                    print('NPC: ' + j.name)
                print('amount of secrets: ' + str(len(self.scene.secrets)))
                for j in self.scene.secrets:
                    print('Secret: ' + j.name)
            self.object_of_interest = self.scene.location
            self.running_scene = True
            self.sort = None
            self.check_for_trigger()  # Is this really needed?
            print(self.scene.location.describe(npcs=self.scene.npcs))
            while self.running_scene:
                self.a = input('<please enter:>')
                self.sort = classify(self.a, analyse)
                master_types = {'info': self.info, 'talk': self.talk, 'speech': self.speech, 'fight': self.fight,
                                'room change': self.room_change, 'action': self.action}
                if self.sort not in master_types.keys():
                    print('classification error line 143ish')
                if self.check_for_trigger():
                    master_types[self.sort]()
            for i in self.scene.secrets:
                if i.name == "won":
                    if i.found:
                        self.running_adventure = False
                        return None
            self.a = input('End of scene. (Press enter to continue)')

    def info(self):
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            print(self.object_of_interest.talk(self.a))  # or fight?
        elif isinstance(self.object_of_interest, adventure_structure.LOCATION):
            print(self.object_of_interest.describe(self.a))
        else:
            print('Error <info>')

    def action(self):
        secrets = []
        for i in self.scene.secrets:
            if self.object_of_interest in i.where_to_find:
                if random.random() > 0:
                    secrets.append(i)
                    i.found = True
                    print(f'(Devtool) secret: {i.name}')
        if len(secrets) == 0:
            secrets = None
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            print(self.object_of_interest.talk(self.a, secrets=secrets))  # or fight?
        elif isinstance(self.object_of_interest, adventure_structure.LOCATION):
            print(self.object_of_interest.describe(self.a, secrets=secrets))
        else:
            print('Error action')

    def speech(self):
        if not isinstance(self.object_of_interest, adventure_structure.NPC):
            person = who(self.a, self.scene)
            self.object_of_interest = person
        secrets = []
        for i in self.scene.secrets:
            if self.object_of_interest in i.where_to_find:
                if random.random() > 0:
                    secrets.append(i)
                    i.found = True  # always immediately True?
                    print(f'(Devtool) secret: {i.name}')
        if len(secrets) == 0:
            secrets = None
        print(self.object_of_interest.talk(self.a, secrets=secrets))

    def room_change(self):
        self.conditions = [where(self.a, self.adventure), [None]]
        # NPC conditions should explicitly exclude the ones from the last scene.
        self.running_scene = False

    def fight(self):
        print('Fighting does not yet work.')

    def talk(self):
        person = who(self.a, self.scene)
        if not isinstance(person, adventure_structure.NPC):
            person = random.choice(self.scene.npcs)
        print(f'You are talking to {person.name}.')
        self.object_of_interest = person
        secrets = []
        for i in self.scene.secrets:
            if self.object_of_interest in i.where_to_find:
                if random.random() > 0:
                    secrets.append(i)
                    i.found = True
                    print(f'(Devtool) You find out the following secret: {i.name}')
        if len(secrets) == 0:
            secrets = None
        print(self.object_of_interest.talk(self.a, secrets=secrets))


def classify(a, analyse):
    prompt = f'{a}\n\n###\n\n'
    response = openai.Completion.create(model='ada:ft-personal:input-classifier-2022-12-17-07-32-32',
                                        prompt=prompt, temperature=0, max_tokens=12, stop="###")
    response = response['choices'][0]['text']
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['sample'].append({'prompt': prompt, 'completion': response + '###'})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    if response[0] == ' ':
        response = response[1:]
    return response


def who(a, scene):
    names = []
    name_dict = {}
    for i in scene.npcs:
        names.append(i.name)
        name_dict.update({i.name.lower(): i})
    prompt = f'{names.keys()}\n{a}\n\n###\n\n'
    response = openai.Completion.create(model='curie:ft-personal:who-2022-12-17-23-11-02',
                                        prompt=prompt, temperature=0, max_tokens=12, stop="###")
    response = response['choices'][0]['text']
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['who'].append({'prompt': prompt, 'completion': response + '###'})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    if response.startswith(' '):
        response = response[1:]
    if response.lower() in name_dict.keys():
        return name_dict[response]
    else:
        print('Who are you talking to?')
        print(names.keys())
        response = input('Please copypaste who you  are talking to or leave empty to just talk to someone.')
        if response in names.keys():
            return names[response]
        else:
            print('I did not understand that.')
            return 'could not find'


def where(a, adventure):
    names = []
    name_dict = {}
    for i in adventure.major_locations:
        if i.active:
            names.append(i.name)
            name_dict.update({i.name.lower(): i})
    prompt = f'{names.keys()}\n{a}\n\n###\n\n'
    response = openai.Completion.create(model='curie:ft-personal:where-2022-12-17-23-05-15',
                                        prompt=prompt, temperature=0, max_tokens=18)
    response = response['choices'][0]['text']
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['where'].append({'prompt': prompt, 'completion': response + '###'})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    if response.startswith(' '):
        response = response[1:]
    if response.lower() in name_dict.keys():
        return name_dict[response]
    else:
        print('Where are you going?')
        print(names.keys())
        response = input('(!) Please copypaste where you are going or leave empty to just go somewhere.')
        if response in names.keys():
            return names[response]
        else:
            print('I did not understand that.')
            return 'could not find'


def write_as_jsonlines(key):
    path = 'C:\\Users\\thede\\PycharmProjects\\Roleplay-with-AI\\'
    x = []
    with open('data.json') as f:
        data = json.load(f)[key]
    if isinstance(data, dict):
        for i in data[key].keys():
            x.append({'prompt': i, 'completion': data[key][i]})
    else:
        x = data
    with jsonlines.open(f'{key}.jsonl', 'w') as writer:
        writer.write_all(x)
    return f'{key}.jsonl'


if __name__ == '__main__':
    main()
