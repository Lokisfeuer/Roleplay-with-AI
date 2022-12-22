# Future plans with AI:
# A setting generator.
# an intelligent adventure writer.
# Every Scene Type intelligent interpreter
# Something that finds out if secrets have been told.
import jsonpickle
# next steps:
# test commands
# command take back
# A website
# easier and with AI written adventures. (Text to code?)


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


def write_adventure():
    object_dict = {'npcs': [], 'locations': [], 'secrets': []}
    print(f'Please enter all ')
    for i in range(3):
        a = input('<please enter:> ')
        while not a.startswith('/'):
            object_dict[i].append(a)
            a = input('<please enter:> ')

def main():
    # write_to_json()  # Error!
    # test()
    trigger = [adventure_structure.prolouge, adventure_structure.on_the_algebra, adventure_structure.boss_fight, adventure_structure.at_the_algebra, adventure_structure.won, adventure_structure.loveletter, adventure_structure.money, adventure_structure.alcohol, adventure_structure.secret_message]
    adventure_structure.the_drowned_aboleth(*trigger)
    game, username = login()
    game.play(username=username)
    # adventure, conditions = adventure_structure.the_drowned_aboleth()
    # GAME(adventure=adventure, conditions=conditions).play()
    pass


def login():
    username = input('Please enter your username: ')
    with open('data.json', 'r') as f:
        data = json.load(f)
    accounts = list(data['players'].keys())
    while username not in accounts:
        for i in range(len(username)):
            for j in data['players'].keys():
                if len(accounts) == 1:
                    break
                if not j[i] == username[i] and j in accounts:
                    accounts.remove(j)
        print(f'This username is not registered. Do you want to\n    (1) register it or\n    (2) use the existing '
              f'username {accounts[0]} or\n    (3) reenter your username?')
        num = input('Please enter [1/2/3]: ')
        if num == '1':
            data['players'].update({username: {}})
        elif num == '2':
            username = accounts[0]
        else:
            username = input('Please enter your username: ')
        accounts = list(data['players'].keys())
    print(f'You are logged in as {username}.')
    print(f'Which adventure do you want to play?')
    adventures = list(data['adventures'].keys())
    for i in range(len(adventures)):
        print(f'    {adventures[i]} ({i+1})')
    adventure = input('Please enter the name or number of the adventure you want to play: ')
    while adventure not in adventures:
        if adventure[0].isdigit():
            adventure = adventures[int(adventure[0])-1]
        else:
            adventures = data['adventures'].keys()
            for i in range(len(adventure)):
                for j in data['adventures'].keys():
                    if not j[i] == adventure[i]:
                        adventures.remove(j)
                    if len(adventures) == 1:
                        break
                if len(adventures) == 1:
                    break
            if input(f'Did you mean {adventures[0]}? [Y/n] ').lower().startswith('y'):
                adventure = adventures[0]
            else:
                adventure = input('Please enter the name or number of the adventure you want to play: ')
    print(f'You chose {adventure}')
    if adventure not in data['players'][username].keys():
        data['players'][username].update({adventure: []})
    if len(data['players'][username][adventure]) > 0:
        game = jsonpickle.decode(data['players'][username][adventure][-1], keys=True)
    else:
        conditions = jsonpickle.decode(data['adventures'][adventure]['conditions'], keys=True)
        adventure = jsonpickle.decode(data['adventures'][adventure]['adventure'], keys=True)
        game = GAME(adventure=adventure, conditions=conditions)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return game, username


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
        if a is None:
            self.a = ''
        else:
            self.a = a
        self.object_of_interest = object_of_interest
        self.scene = scene
        self.adventure = adventure
        self.running_scene = running_scene
        self.running_adventure = running_adventure
        self.sort = sort

    def check_for_trigger(self):
        back = []
        a = self.a.replace('\\', '/')
        if '/' in a[:3]:
            a = '/'+''.join(self.a.split('/')[1:])
            while a.startswith('/ '):
                a = '/'+a[2:]
            # commands: back, log (inventory and secrets), clue, help, /mastertype a, describe scene (analyse)
            b = False
            if a.startswith('/b'):
                print('Taking back your action does not work yet.')
                pass
            elif a.startswith('/l'):
                for i in self.adventure.major_secrets:
                    if i.found and i.active:
                        print(i.name)
            elif a.startswith('/c'):
                for i in self.adventure.major_secrets:
                    l = []
                    if i.active and i.clue and not i.found:
                        l.append(i)
                    clue = random.choice(l)
                    clue.found = True
                    print(f'Here is your clue: {clue.name}.{clue.description}')
            elif a.startswith('/h'):
                print('Here are all commands and what they do. Just enter them after the <please enter:> instead of your normal statement.')
                print(f'"/b" or "/back"         This command takes back your last input.')
                print(f'"/h" or "/help"         This command lists and explains all commands.')
                print(f'"/l" or "/log"          This command lists everything you have already found and collected.')
                print(f'"/c" or "/clue"         This command gives you a clue on how to proceed.')
                print(f'"/d" or "/describe"     This command lists all the data of the current scene.')

                print(f'The following commands need a normal statement after the command.')
                print(f'E. g. "/info What do I see?"')
                print(f'"/i" or "/info"         This command classifies the following statement as an info question.')
                print(f'"/a" or "/action"       This command classifies the following statement as an action.')
                print(f'"/v" or "/verbatim"     This command classifies the following statement as verbatim (speech).')
                print(f'"/t" or "/talk"         This command classifies the following statement as an attempt to')
                print(f'                        start a conversation.')
                print(f'"/f" or "/fight"        This command classifies the following statement as an aggressive action.')
                print(f'"/r" or "/room change"  This command classifies the following statement as a room change.')
                print('These 6 commands are not necessary, usually inputs are automatically classified correctly.')
            elif a.startswith('/d'):
                print(f'Scene type: {self.scene.type}')
                print('location: ' + self.scene.location.name)
                print('amount of npcs: ' + str(len(self.scene.npcs)))
                for j in self.scene.npcs:
                    print('NPC: ' + j.name)
                print('amount of secrets: ' + str(len(self.scene.secrets)))
                for j in self.scene.secrets:
                    print('Secret: ' + j.name)
            elif a.startswith('/i'):
                b = True
                self.a = ''.join(a.split()[1:])
                self.sort = 'info'
            elif a.startswith('/a'):
                b = True
                self.a = ''.join(a.split()[1:])
                self.sort = 'action'
            elif a.startswith('/v'):
                b = True
                self.a = ''.join(a.split()[1:])
                self.sort = 'speech'
            elif a.startswith('/t'):
                b = True
                self.a = ''.join(a.split()[1:])
                self.sort = 'talk'
            elif a.startswith('/f'):
                b = True
                self.a = ''.join(a.split()[1:])
                self.sort = 'fight'
            elif a.startswith('/r'):
                b = True
                if a.split()[1].startswith('ch'):
                    self.a = ''.join(a.split()[2:])
                else:
                    self.a = ''.join(a.split()[1:])
                self.sort = 'room change'
            else:
                print('Command not understood, see \'/help\' for help on commands.')
            # commands: back, log (inventory and secrets), clue, help, /mastertype a, describe scene (analyse)
            # '/b, /i, /c, /h, /d, /l, /a, /s, /t, /f, /r'
            back.append(b)
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
                    if self.scene.location.name == j.name:
                        triggered = True
            if triggered:
                back.append(i.function(i, self))
        if False in back:
            return False
        return True

    def play(self, username='username', analyse=True):
        while self.running_adventure:
            self.scene = adventure_structure.get_next_scene(
                adventure=self.adventure, all_former_scenes=self.former_scenes, conditions=self.conditions
            )
            con = self.conditions
            self.conditions = [self.scene.location, [self.scene.npcs]]
            with open('data.json', 'r') as f:
                data = json.load(f)
            data['players'][username][self.adventure.name].append(jsonpickle.encode(self, keys=True))
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
            self.conditions = con
            self.object_of_interest = self.scene.location
            self.running_scene = True
            self.sort = None
            # commands: take back, inventory and secrets, hint, help, describe scene (analyse), /mastertype a
            self.check_for_trigger()  # Is this really needed?
            print(self.scene.location.describe(npcs=self.scene.npcs))
            while self.running_scene:
                self.a = input('<please enter:> ')
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
            self.former_scenes.append(self.scene)


    def info(self):
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            print(self.object_of_interest.talk(self.a))  # or fight?
        elif isinstance(self.object_of_interest, adventure_structure.LOCATION):
            print(self.object_of_interest.describe(self.a))
        else:
            print('Error <info>')

    def action(self):
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            # all social skills need to be implemented in speech. And all tiny social actions as well.
            s = input(f'Do you intend to leave your conversation with {self.object_of_interest.name}? [Y/n]')
            if s.lower().startswith('y'):
                self.object_of_interest = self.scene.location
        secrets = []
        for i in self.scene.secrets:
            if self.object_of_interest in i.where_to_find:
                if random.random() > 0:
                    secrets.append(i)
                    print(f'(Devtool) secret: {i.name}')
        if len(secrets) == 0:
            secrets = None
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            response = self.object_of_interest.talk(self.a, secrets=secrets)  # or fight?
        elif isinstance(self.object_of_interest, adventure_structure.LOCATION):
            response = self.object_of_interest.describe(self.a, secrets=secrets)
        else:
            print('(Devtool) Error action line 195ish')
        if secrets is not None:
            for i in secrets:
                prompt = f'{response}\n\nWas the following secret told in the text above?\nSecret: {i.description}\n\nYes or no?\n'
                mentioned = openai.Completion.create(model='text-davinci-003',
                                                    prompt=prompt, temperature=0, max_tokens=1, )
                mentioned = mentioned['choices'][0]['text']
                if mentioned.lower().startswith('y'):
                    print(f'(Devtool) Secret {i.name} was found.')
                    i.found = True
                elif mentioned.lower().startswith('n'):
                    i.found = False
                else:
                    print('(Devtool) Error secret mentioned? Line 222ish.')
                    i.found = False
        print(response)

    def speech(self):
        if not isinstance(self.object_of_interest, adventure_structure.NPC):
            person = who(self.a, self.scene)
            self.object_of_interest = person
        secrets = []
        for i in self.scene.secrets:
            if self.object_of_interest in i.where_to_find:
                if random.random() > 0:
                    secrets.append(i)
                    print(f'(Devtool) secret: {i.name}')
        if len(secrets) == 0:
            secrets = None
        response = self.object_of_interest.talk(self.a, secrets=secrets)
        if secrets is not None:
            for i in secrets:
                prompt = f'{response}\n\nWas the following secret told in the text above?\nSecret: {i.description}\n\nYes or no?\n'
                mentioned = openai.Completion.create(model='text-davinci-003',
                                                    prompt=prompt, temperature=0, max_tokens=1, )
                mentioned = mentioned['choices'][0]['text']
                if mentioned.lower().startswith('y'):
                    print(f'(Devtool) Secretm {i.name} was found.')
                    i.found = True
                elif mentioned.lower().startswith('n'):
                    i.found = False
                else:
                    print('(Devtool) Error secret mentioned? Line 222ish.')
                    i.found = False
        print(response)

    def room_change(self):
        loc = where(self.a, self.adventure)
        # NPC conditions should explicitly exclude the ones from the last scene.
        if input(f'Do you want to leave {self.scene.location.name} and go to {loc.name}? [Y/n] ').lower().startswith('y'):
            self.conditions = [loc, [None]]
            self.running_scene = False


    def fight(self):
        print('Fighting does not yet work.')

    def talk(self):
        person = who(self.a, self.scene)
        if not isinstance(person, adventure_structure.NPC):
            person = random.choice(self.scene.npcs)
        print(f'You are talking to {person.name}.')
        self.object_of_interest = person
        print(self.object_of_interest.talk(self.a, secrets=None))


def classify(a, analyse):
    prompt = f'{a}\n\n###\n\n'
    response = openai.Completion.create(model='ada:ft-personal:input-classifier-2022-12-17-07-32-32',
                                        prompt=prompt, temperature=0, max_tokens=12, stop="###")
    response = response['choices'][0]['text']
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['sample'].update({prompt: response + '###'})
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
    prompt = f'{names}\n{a}\n\n###\n\n'
    response = openai.Completion.create(model='curie:ft-personal:who-2022-12-17-23-11-02',
                                        prompt=prompt, temperature=0, max_tokens=12, stop="###")
    response = response['choices'][0]['text']
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['who'].update({prompt: response + '###'})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    if response.startswith(' '):
        response = response[1:]
    if response.lower() in name_dict.keys():
        return name_dict[response.lower()]
    else:
        print('Who are you talking to?')
        print(names)
        response = input('Please copypaste who you  are talking to or leave empty to just talk to someone.')
        if response in names:
            return name_dict[response.lower()]
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
    prompt = f'{names}\n{a}\n\n###\n\n'
    response = openai.Completion.create(model='curie:ft-personal:where-2022-12-17-23-05-15',
                                        prompt=prompt, temperature=0, max_tokens=18, stop='###')
    response = response['choices'][0]['text']
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['where'].update({prompt: response + '###'})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    if response.startswith(' '):
        response = response[1:]
    if response.lower() in name_dict.keys():
        return name_dict[response.lower()]
    else:
        print('Where are you going?')
        print(names)
        response = input('(!) Please copypaste where you are going or leave empty to just go somewhere.')
        if response in names:
            return name_dict[response]
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
