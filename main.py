# Future plans with AI:
# A setting generator.
# an intelligent adventure writer.
# Every Scene Type intelligent interpreter

# next steps:
# clean up code
# write commands (/exit)
# command take back
# A website
# add character skills and classes
# add fighting
# create a proper menu

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


# This is the attempt to set up a discord bot via which one can play adventures. (It does not work (yet).)
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        if not isinstance(message.channel, discord.channel.DMChannel):
            if not message.content.lower().startswith('/dm'):
                return
            else:
                pass
        username = message.author.name
        with open('data.json', 'r') as f:
            data = json.load(f)
        async for i in message.channel.history(limit=1):
            sec = (datetime.datetime.now(datetime.timezone.utc) - i.created_at).total_seconds()
        if username in data['players'].keys() and sec < 1800:
            if not data['players'][username]['fetching game'] and data['players'][username]['recent adventure'] is not None:
                adventure = data['players'][message.author.name]['recent adventure']
                if adventure == 'writing adventure':
                    answer = adventure_writer.main(username, message.content)
                    await message.channel.send(answer)
                    if isinstance(answer, bool):
                        data['players'][username]['fetching game'] = True
                        await message.channel.send('Which adventure do you want to play?')
                    return
                pickled_object = data['players'][message.author.name][adventure][-1]
                game = jsonpickle.decode(pickled_object, keys=True)
                if game.triggering is None:
                    answer = game.dc_play(message.content, username=username)
                else:
                    game.a = message.content
                    # There are likely other game.variables that need to be updated here as well
                    answer = game.triggering.call(game.adventure, game.triggering, game, game.trigger_counter, message=message)
                    if isinstance(answer, bool):
                        game.triggering = None
                        game.trigger_counter = 0
                        if answer:
                            answer = game.dc_play(message.content, username=username)
                        else:
                            answer = 'please enter'
                    else:
                        game.trigger_counter = game.trigger_counter + 1
                with open('data.json', 'r') as f:
                    data = json.load(f)
                data['players'][message.author.name][adventure].append(jsonpickle.encode(game, keys=True))
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
                if not answer.startswith('\n\n'):
                    answer = '\n\n' + answer
                answer = f'Devtool: {adventure}/{game.scene.location.name}/{game.object_of_interest.name}{answer}'
            else:
                answer = await dc_login(message)
        else:
            answer = await dc_login(message)
        print('on_message is through')
        if answer == '' or answer is None:
            answer = '<game saved>\nAsk, what you see.'
        await message.channel.send(answer)


async def dc_login(message):
    with open('data.json', 'r') as f:
        data = json.load(f)
    username = message.author.name
    answer = ''
    async for i in message.channel.history(limit=1):
        sec = (datetime.datetime.now(datetime.timezone.utc) - i.created_at).total_seconds()
    if username not in data['players'].keys() or sec > 1800:
        if username not in data['players'].keys():
            answer = answer + 'You are not registered yet. An account with your username is being created.'
            data['players'].update({username: {}})
        else:
            answer = answer + 'Resetting...'
        data['players'][username].update({'fetching game': True})
        data['players'][username].update({'recent adventure': None})
        answer = answer + '\nWhich adventure do you want to play?'
        adventures = list(data['adventures'].keys())
        for i in range(len(adventures)):
            answer = answer + f'\n    {adventures[i]} ({i + 1})'
        answer = answer + '\nPlease enter the name or number of the adventure you want to play.'
    else:
        if data['players'][username]['fetching game']:
            data['players'][username].update({'fetching game': False})
            print('fetching game is turned off now.')
            adventure = message.content
            adventures = list(data['adventures'].keys())
            if adventure in adventures or adventure[0].isdigit():
                if adventure[0].isdigit():
                    adventure = adventures[int(adventure[0]) - 1]
                if not adventure == 'writing adventure':
                    conditions = jsonpickle.decode(data['adventures'][adventure]['conditions'], keys=True)
                    adv = jsonpickle.decode(data['adventures'][adventure]['adventure'], keys=True)
                    game = GAME(adventure=adv, conditions=conditions)
                    if adventure not in data['players'][username].keys():
                        data['players'][username].update({adventure: [jsonpickle.encode(game, keys=True)]})
                data['players'][username].update({'recent adventure': adventure})
                answer = f'You are logged in as {username} and are playing the adventure {adventure}.\n' \
                         f'Send anything to continue.'
                print(answer)
                # answer = answer + game.dc_play('Please describe the Situation.', username=username)
            else:
                data['players'][username].update({'fetching game': True})
                answer = 'That did not work. Please (re-)enter the name or number of the adventure you want to ' \
                         'play. '
        else:
            # This is the case after a full adventure has been completed.
            if message.content.startswith('new'):
                data['players'][username]['fetching game'] = True
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
                return 'Please enter the name or number of the adventure you want to play.'
            else:
                return 'You finished your adventure. If you want to play another one, enter "new adventure"'
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return answer


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
        print(f'    {adventures[i]} ({i + 1})')
    adventure = input('Please enter the name or number of the adventure you want to play: ')
    while adventure not in adventures:
        if adventure[0].isdigit():
            adventure = adventures[int(adventure[0]) - 1]
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
    def __init__(self, object_of_interest=None, scene=None, adventure=None, a=None, running_scene=None, conditions=None,
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
        self.object_of_interest = object_of_interest
        self.scene = scene
        self.adventure = adventure
        self.running_scene = running_scene
        self.running_adventure = running_adventure
        self.sort = sort
        self.triggering = triggering
        self.trigger_counter = trigger_counter

    def check_for_trigger(self):
        back = []
        a = self.a.replace('\\', '/')
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
                while self.triggering == i and not isinstance(answer, bool):
                    self.trigger_counter = self.trigger_counter + 1
                    self.a = input(answer)
                    answer = i.call(self.adventure, i, self, self.trigger_counter)
                self.triggering = None
                self.trigger_counter = 0
                back.append(answer)
        if False in back:
            return False
        elif True in back:
            return True
        else:
            pass
            # One trigger at a time!

    def dc_check_for_trigger(self):
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
                        return answer
        return True

    def dc_play(self, input, username='username', analyse=True):
        # return 'Playing via discord does not work (yet).'
        # Trigger still don't work.
        if not self.running_scene:
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
            answer = self.dc_check_for_trigger()
            if not isinstance(answer, bool):
                self.scene.location.describe(npcs=self.scene.npcs)
                return answer
            else:
                return self.secret_finder(self.scene.location.describe(npcs=self.scene.npcs))
                # This line leads to ignoring user input when it shouldn't be ignored.
        # This is running scene:
        self.a = input
        self.sort = classify(self.a, self.adventure, analyse)
        master_types = {'info': self.info, 'talk': self.talk, 'speech': self.speech, 'fight': self.fight,
                        'room change': self.room_change, 'action': self.action}
        if self.sort not in master_types.keys():
            print('classification error line 143ish')
        answer = self.dc_check_for_trigger()
        if isinstance(answer, bool):
            if answer:
                answer = master_types[self.sort]()
                answer = self.secret_finder(answer)
        if not self.running_scene:
            for i in self.scene.secrets:
                if i.name == "won":
                    if i.found:
                        with open('data.json', 'r') as f:
                            data = json.load(f)
                        data['players'][username]['recent adventure'] = None
                        with open('data.json', 'w') as f:
                            json.dump(data, f, indent=4)
            self.former_scenes.append(self.scene)
        return answer

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
            print(self.secret_finder(self.scene.location.describe(npcs=self.scene.npcs)))
            while self.running_scene:
                self.a = input('<please enter:> ')
                self.sort = classify(self.a, self.adventure, analyse)
                master_types = {'info': self.info, 'talk': self.talk, 'speech': self.speech, 'fight': self.fight,
                                'room change': self.room_change, 'action': self.action}
                if self.sort not in master_types.keys():
                    print('classification error line 143ish')
                if self.check_for_trigger():  # trigger are (too?) Tricky to convert for dc_play()
                    # Maybe right now running trigger could be checked with another clause.
                    answer = master_types[self.sort]()
                    answer = self.secret_finder(answer)
                    print(answer)
            for i in self.scene.secrets:
                if i.name == "won":
                    if i.found:
                        self.running_adventure = False
                        return None
            self.a = input('End of scene. (Press enter to continue)')
            self.former_scenes.append(self.scene)

    def info(self):
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            return self.object_of_interest.talk(self.a)  # or fight?
        elif isinstance(self.object_of_interest, adventure_structure.LOCATION):
            return self.object_of_interest.describe(self.a)
        else:
            return 'Error <info>'

    def action(self):
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

    def secret_finder(self, response):
        # save for future trainingsdata !!
        secrets = []
        for i in self.scene.secrets:
            if self.object_of_interest in i.where_to_find:
                if not i.found:
                    secrets.append(i)
                    print(f'(Devtool) secret: {i.name}')
        for i in secrets:
            prompt = f'Secret: {i.name}\nText: {response}\n\nAnswer:'
            mentioned = openai.Completion.create(model='davinci:ft-personal:secret-finder-2023-02-02-05-34-08',
                                                 prompt=prompt, temperature=0, max_tokens=5, stop='###')
            mentioned = mentioned['choices'][0]['text']
            if mentioned == '':
                print('Secret finder gave no output.')
            if mentioned[0] == ' ':
                mentioned = mentioned[1:]
            if mentioned.lower().startswith('y'):
                print(f'(Devtool) Secret {i.name} was found.')
                response = f'{response}\n\n<You found an important piece of information: {i.name}>'
                i.found = True
            with open('data.json', 'r') as f:
                data = json.load(f)
            data['newsecret_sample'].update({prompt: ' ' + response + '###'})
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
        return response

    def speech(self):
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

    def room_change(self):
        loc = where(self.a, self.adventure)
        if self.a.startswith('Okay,'):
            npcs = []
            for i in self.adventure.major_npcs:
                if i.active:
                    npcs.append(i)
            self.conditions = [loc, npcs]
        else:
            # NPC conditions should explicitly exclude the ones from the last scene.
            self.conditions = [loc, [None]]
        self.running_scene = False
        return f'You are going to the {loc.name}.'

    def fight(self):
        return 'Fighting does not yet work.'

    def talk(self):
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


def classify(a, adventure, analyse):
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
