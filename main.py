# Future plans with AI:
# A setting generator.
# an intelligent adventure writer.
# Every Scene Type intelligent interpreter

# next steps:
# write commands (/exit) (take back)
# secrets need proper names and descriptions (for the adventure writer)
# add character skills and classes
# add fighting
# A website


import jsonpickle
import openai
import random
import adventure_structure
import os
import json
import jsonlines
import discord
import datetime
import adventure_writer

openai.api_key = os.getenv('OPENAI_API_KEY')
TOKEN = os.getenv('DISCORD_TOKEN_ROLEPLAY')
client = discord.Client(intents=discord.Intents.default())


# model = 'ada:ft-personal-2022-11-27-20-21-30'
# very old model = 'ada:ft-personal-2022-11-27-17-16-21'
# old model = ada:ft-personal:input-classifier-2022-12-17-07-32-32
# ada:ft-personal:input-classifier-2023-02-10-10-14-50
# wheremodel = curie:ft-personal:where-2022-12-17-23-05-15
# whomodel = curie:ft-personal:who-2022-12-17-23-11-02


def main():
    trigger = [adventure_structure.prolouge, adventure_structure.on_the_algebra, adventure_structure.boss_fight,
               adventure_structure.at_the_algebra, adventure_structure.won, adventure_structure.loveletter,
               adventure_structure.money, adventure_structure.alcohol, adventure_structure.secret_message]
    adventure, conditions = adventure_structure.the_drowned_aboleth(*trigger)
    # check the triggers for their functions.
    # adventure.trigger[0].call(adventure, adventure.trigger[0], 'game_object', 0)
    client.run(TOKEN)
    # write_to_json()  # Error!
    # test()
    # game, username = login()
    # game.play(username=username)
    # adventure, conditions = adventure_structure.the_drowned_aboleth()
    # GAME(adventure=adventure, conditions=conditions).play()
    pass


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord.')


@client.event
async def on_message(message):
    if message.author == client.user or not isinstance(message.channel, discord.channel.DMChannel):
        return
    username = message.author.name
    with open('data.json', 'r') as f:
        data = json.load(f)
    if username not in data['players'].keys():
        data['players'].update({username: {'running': None}})
    async for i in message.channel.history(limit=1):
        sec = (datetime.datetime.now(datetime.timezone.utc) - i.created_at).total_seconds()
        if sec > 1800:
            data['players'][username]['running'] = None
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    running = data['players'][username]['running']
    if running is None:
        answer = menu(message.content, username)
    elif running in data['adventures'].keys():
        if running in data['players'][username].keys():
            game = jsonpickle.decode(data['players'][username][running][-1], keys=True)
        else:
            conditions = jsonpickle.decode(data['adventures'][running]['conditions'], keys=True)
            adv = jsonpickle.decode(data['adventures'][running]['adventure'], keys=True)
            game = GAME(adventure=adv, conditions=conditions)
            if running not in data['players'][username].keys():
                with open('data.json', 'r') as f:
                    data = json.load(f)
                data['players'][username].update({running: [jsonpickle.encode(game, keys=True)]})
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
        answer = game.play(message.content, username)
    elif running == 'writing adventure':
        answer = adventure_writer.main(username, message.content)
        if isinstance(answer, bool):
            if answer:
                answer = 'Adventure written successfully.'
            else:
                answer = 'Exited adventure writer'
            with open('data.json', 'r') as f:
                data = json.load(f)
            data['players'][username]['running'] = None
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
    # elif running in data['players'][username][characters].keys():
    else:
        answer = 'Error no running'
    await message.channel.send(answer)


def menu(message, username):
    with open('data.json', 'r') as f:
        data = json.load(f)
    options = ['writing adventure']  # list of strings of options
    for i in data['adventures'].keys():
        options.append(i)
    # append all npcs or add the menu point "create character"
    if message[0].isdigit():
        if int(message) - 1 < len(options):
            data['players'][username]['running'] = options[int(message) - 1]
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
            return f'You chose "{options[int(message) - 1]}"\nSend anything to continue.'
        else:
            answer = 'You are in the main menu. You have different options.\n\n'
            for i in options:
                answer = f'{answer}\t({options.index(i)+1})\t{i}\n'
            answer = f'{answer}\nPlease enter the digit of the menu point you want to choose.'
            return answer
    else:
        answer = 'You are in the main menu. You have different options. To return to this menu just type "/exit".\n\n'
        for i in options:
            answer = f'{answer}\t({options.index(i)+1})\t{i}\n'
        answer = f'{answer}\nPlease enter the digit of the menu point you want to choose.'
        return answer


class GAME:
    def __init__(self, object_of_interest=None, scene=None, adventure=None, a=None, conditions=None,
                 running_adventure=True, former_scenes=None, sort=None, triggering=None, trigger_counter=0):
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
        self.adventure = adventure
        self.scene = self.scene = adventure_structure.get_next_scene(
            adventure=self.adventure, all_former_scenes=self.former_scenes, conditions=self.conditions
        )
        self.object_of_interest = self.scene.location
        self.running_adventure = running_adventure
        self.sort = sort
        self.triggering = triggering
        self.trigger_counter = trigger_counter

    def play(self, message, username):
        answer = None
        if self.triggering is not None:
            self.a = message
            answer = self.triggering.call(self.adventure, self.triggering, self, self.trigger_counter, message=message)
            if isinstance(answer, str):
                self.trigger_counter = self.trigger_counter + 1
            else:
                self.triggering = None
                self.trigger_counter = 0
                if answer:
                    answer = None
                else:
                    answer = 'please enter'
        if answer is None:
            self.a = message
            self.sort = classify(self.a, self.adventure)
            master_types = {'info': self.info, 'talk': self.talk, 'speech': self.speech, 'fight': self.fight,
                            'room change': self.room_change, 'action': self.action}
            if self.sort not in master_types.keys():
                raise Exception('A classification error occurred.')
            answer = self.check_for_trigger(username)
            if isinstance(answer, bool):
                if answer:
                    answer = master_types[self.sort](username)
                    answer = secret_finder(self.scene.secrets, self.object_of_interest, answer)
        with open('data.json', 'r') as f:
            data = json.load(f)
        for i in self.scene.secrets:
            if i.name == "won" and i.found or self.a == '/exit':  # the /exit case should be in check_for_trigger()
                data['players'][username]['running'] = None
        while len(data['players'][username][self.adventure.name]) > 3:
            del data['players'][username][self.adventure.name][0]
        data['players'][username][self.adventure.name].append(jsonpickle.encode(self, keys=True))
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        pos = f'You are here: playing/{self.adventure.name}/{self.scene.location.name}/{self.object_of_interest.name}\n\n'
        return pos + answer

    def check_for_trigger(self, username):
        back = []
        a = self.a.replace('\\', '/')
        # The / commands are not discorded yet.
        if '/' in a[:3]:
            a = '/' + ''.join(self.a.split('/')[1:])
            while a.startswith('/ '):
                a = '/' + a[2:]
            # commands: back, log (inventory and secrets), clue, help, /mastertype a, describe scene (analyse)
            b = False
            if a.startswith('/b'):
                print('Taking back your last input does not work yet. Sorry.')
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
                print(
                    'Here are all commands and what they do. Just enter them after the <please enter:> instead of '
                    'your normal statement.')
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
                print(
                    f'"/f" or "/fight"        This command classifies the following statement as an aggressive action.')
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
                self.triggering = i
                answer = i.call(self.adventure, i, self, self.trigger_counter)
                if not isinstance(answer, bool):
                    self.trigger_counter = self.trigger_counter + 1
                    return answer
                else:
                    self.trigger_counter = 0
                    self.triggering = None
                    if not answer:
                        return 'please enter'
        return True

    def info(self, username=None):
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            return self.object_of_interest.talk(self.a)  # or fight?
        elif isinstance(self.object_of_interest, adventure_structure.LOCATION):
            return self.object_of_interest.describe(self.a)
        else:
            return 'Error <info>'

    def action(self, username=None):
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            # all social skills need to be implemented in speech. And all tiny social actions as well.
            self.object_of_interest = self.scene.location
        secrets = []
        for i in self.scene.secrets:
            if self.object_of_interest in i.where_to_find:
                if random.random() > 0:
                    secrets.append(i)
                    print(f'(Devtool) secret: {i.name}')
        if len(secrets) == 0:
            secrets = None
        return self.object_of_interest.describe(self.a, secrets=secrets)

    def speech(self, username=None):
        if not isinstance(self.object_of_interest, adventure_structure.NPC):
            if len(self.scene.npcs) == 0:
                return 'There is no interesting character to talk to.'
            person = who(self.a, self.scene)
            if person == 'could not find':
                names = self.scene.npcs[0].name
                if not len(self.scene.npcs) == 1:
                    names = names + ' and '
                    for i in self.scene.npcs[1:]:
                        names = f'{names}{i.name}, '
                return f'Who do you intent to talk to? The following characters are in the room: {names[:-2]}'
            self.object_of_interest = person
        secrets = []
        for i in self.scene.secrets:
            if self.object_of_interest in i.where_to_find:
                if random.random() > 0:
                    secrets.append(i)
                    print(f'(Devtool) chance for secret: {i.name}')
        if len(secrets) == 0:
            secrets = None
        response = self.object_of_interest.talk(self.a, secrets=secrets)
        return response

    def room_change(self, username, con=None):
        if con is None:
            loc = where(self.a, self.adventure)
        else:
            loc = con
        if self.a.startswith('Okay,'):
            npcs = []
            for i in self.adventure.major_npcs:
                if i.active:
                    npcs.append(i)
            self.conditions = [loc, npcs]
        else:
            # NPC conditions should explicitly exclude the ones from the last scene.
            self.conditions = [loc, [None]]
        if con is not None:
            self.conditions = con
        self.former_scenes.append(self.scene)
        self.scene = adventure_structure.get_next_scene(
            adventure=self.adventure, all_former_scenes=self.former_scenes, conditions=self.conditions
        )
        self.conditions = [self.scene.location, [self.scene.npcs]]
        self.object_of_interest = self.scene.location
        self.sort = None
        # commands: take back, inventory and secrets, hint, help, describe scene (analyse), /mastertype a
        answer = self.check_for_trigger(username)
        if not isinstance(answer, bool):
            self.scene.location.describe(npcs=self.scene.npcs)
        else:
            if answer:
                answer = self.scene.location.describe(npcs=self.scene.npcs)
                answer = secret_finder(self.scene.secrets, self.object_of_interest, answer)
        return f'You are going to the {loc.name}.{answer}'

    def fight(self, username=None):
        return 'Fighting does not yet work.'

    def talk(self, username=None):
        if len(self.scene.npcs) == 0:
            return 'There is no interesting character to talk to.'
        person = who(self.a, self.scene)
        if person == 'could not find':
            names = self.scene.npcs[0].name
            if not len(self.scene.npcs) == 1:
                names = names + ' and '
                for i in self.scene.npcs[1:]:
                    names = f'{names}{i.name}, '
            return f'Who do you intent to talk to? The following characters are in the room: {names[:-2]}'
        self.object_of_interest = person
        return f'You are talking to {person.name}. {self.object_of_interest.talk(self.a, secrets=None)}'


def classify(a, adventure):
    prompt = f'{a}\n\n###\n\n'
    response = openai.Completion.create(model='ada:ft-personal:input-classifier-2023-02-10-10-14-50',
                                        prompt=prompt, temperature=0, max_tokens=12, stop="###")
    response = response['choices'][0]['text']
    if response[0] == ' ':
        response = response[1:]
    if response == 'room change':
        if where(a, adventure) == 'could not find':
            response = 'action'
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['newsample'].update({prompt: ' ' + response + '###'})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return response


def secret_finder(scene_secrets, object_of_interest, text):
    # save for future trainingsdata !!
    secrets = []
    for i in scene_secrets:
        if object_of_interest in i.where_to_find:
            if not i.found:
                secrets.append(i)
    for i in secrets:
        prompt = f'Secret: {i.name}\nText: {text}\n\nAnswer:'
        mentioned = openai.Completion.create(model='davinci:ft-personal:secret-finder-2023-02-02-05-34-08',
                                             prompt=prompt, temperature=0, max_tokens=5, stop='###')
        mentioned = mentioned['choices'][0]['text']
        if mentioned == '':
            print('Secret finder gave no output.')
        if mentioned[0] == ' ':
            mentioned = mentioned[1:]
        if mentioned.lower().startswith('y'):
            text = f'{text}\n\n<You found an important piece of information: {i.name}>'
            i.found = True
        with open('data.json', 'r') as f:
            data = json.load(f)
        data['newsecret_sample'].update({prompt: ' ' + text + '###'})
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
    return text


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
    data['newwho'].update({prompt: response + '###'})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    if response.startswith(' '):
        response = response[1:]
    if response.lower() in name_dict.keys():
        return name_dict[response.lower()]
    else:
        print('With whom are you interacting?')
        str = ''
        n = 0
        for i in names[:-1]:
            str = f'{str}, {i}'
            n = 2
        str = str[n:] + ' or ' + names[-1]
        # response = input(f'{str}\nPlease enter who you are talking to or leave empty to just talk to someone. ')
        response = ''
        prompt = f'{names}\nI interact with {response} the following way: {a}\n\n###\n\n'
        response = openai.Completion.create(model='curie:ft-personal:who-2022-12-17-23-11-02',
                                            prompt=prompt, temperature=0, max_tokens=12, stop="###")
        if response in names:
            return name_dict[response.lower()]
        else:
            return 'could not find'


def where(a, adventure):
    names = []
    name_dict = {}
    for i in adventure.major_locations:
        adventure_structure.check_active(i)
        if i.active:
            names.append(i.name)
            name_dict.update({i.name.lower(): i})
    prompt = f'{names}\n{a}\n\n###\n\n'
    response = openai.Completion.create(model='curie:ft-personal:where-2022-12-17-23-05-15',
                                        prompt=prompt, temperature=0, max_tokens=18, stop='###')
    response = response['choices'][0]['text']
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['newwhere'].update({prompt: response + '###'})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    if response.startswith(' '):
        response = response[1:]
    if response.lower() in name_dict.keys():
        return name_dict[response.lower()]
    else:
        print('Where are you going?')
        print(names)
        # response = input('(!) Please copypaste where you are going or leave empty to just go somewhere. ')
        response = ''
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
        for i in data.keys():
            x.append({'prompt': i, 'completion': data[i]})
    else:
        x = data
    with jsonlines.open(f'{key}.jsonl', 'w') as writer:
        writer.write_all(x)
    return f'{key}.jsonl'


if __name__ == '__main__':
    main()
