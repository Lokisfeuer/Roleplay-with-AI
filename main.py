# Future plans with AI:
# an intelligent adventure writer.
# Every Scene Type intelligent interpreter
# a setting generator

# next steps:
# implement a rulebook -> Characters and Setting
# add fighting
# add multiplayer (Discord server / group chats)
# add the possibility to lose the game.
# all of this comes down to implementing a proper rulebook. D&D seems best for that purpose:
#   D&D all publications: https://the-eye.eu/public/Books/rpg.rem.uz/Dungeons%20%26%20Dragons/
#   Open source d&d character generator: https://www.npcgenerator.com/
#   An equivalent to this for locations. https://www.google.com/search?client=firefox-b-d&q=d%26d+location+generator
#   They need to be intertwined through secrets.
#   Also, they need to kind of react different on different types of characters.

# To do in order:
# 1. look at: the npcgenerator code; the standard rulebook character creation;
# 2. Decide on what is important of the npc generator and which location generator to choose.
# 3. Decide what is important for the player character, which skills should be implemented
# 4. Build the character generator
# 5. If possible, find a way to intertwine npcs and locations with secrets.
# 6. Build the setting generator

# https://github.com/AdrianSI666/DnD_Bestiary-Spellbook-CT
# https://github.com/opendnd/personae Can do relations between characters!
# https://github.com/topics/npc-generator







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
import p_character
import skills
import user_written_adventures.Lokisglut_Test0304 as test0304


TOKEN = os.getenv('DISCORD_TOKEN_ROLEPLAY')
openai.api_key = os.getenv('OPENAI_API_KEY')
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
    test0304.test0304()
    client.run(TOKEN)
    # pull data.json, fine_tuning.json from local server
    # pull folder user_written_adventures from local server
    # every hour push these on the local server


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
            data['players'][username]['running'] = None  # some things like pc generation need to be stopped propperly.
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
    elif running == 'create PC':
        answer = p_character.main_create(username, message.content)
        if isinstance(answer, bool):
            if answer:
                answer = 'PC written successfully.'
            else:
                answer = 'Exited PC creator and deleted PC.'
            with open('data.json', 'r') as f:
                data = json.load(f)
            data['players'][username]['running'] = None
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
    elif running == 'create skill':
        answer = p_character.add_skill(username, message.content)
        if isinstance(answer, bool):
            if answer:
                answer = 'Skill written successfully.'
            else:
                answer = 'Exited skill creator and deleted skill.'
            with open('data.json', 'r') as f:
                data = json.load(f)
            data['players'][username]['running'] = None
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
    elif running == 'level up PC':
        answer = p_character.level_up(username, message.content)
        if isinstance(answer, bool):
            if answer:
                answer = 'Levelled up successfully.'
            else:
                answer = 'Exited but did not level up any character.'
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
    options = ['writing adventure', 'create PC', 'create skill', 'level up PC']  # list of strings of options
    for i in data['adventures'].keys():
        options.append(i)
    # append all npcs or add the menu point "create character"
    if message[0].isdigit():
        if int(message) - 1 < len(options):
            data['players'][username]['running'] = options[int(message) - 1]
            start_texts = {
                'writing adventure': 'Enter "/open name_of_adventure" to create a new adventure or reopen an old one.',
                'create PC': 'Enter the name of the PC you want to create.',
                'create skill': 'Enter the name of the skill you want to create.',
                'level up PC': 'Enter the name of the character you want to level up.'
            }
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
            if options[int(message) - 1] in start_texts.keys():
                return f'You chose "{options[int(message) - 1]}".\n{start_texts[options[int(message) - 1]]}'
            return f'You chose "{options[int(message) - 1]}".\nSend anything to continue.'
        else:
            answer = 'You are in the main menu. You have different options.\n\n'
            for i in options:
                answer = f'{answer}\t({options.index(i)+1})\t{i}\n'
            answer = f'{answer}\nPlease enter the digit of the menu point you want to choose.'
            return answer
    else:
        answer = 'You are in the main menu. You have different options. To return to this menu just type "/exit" (if ' \
                 'this doesn\'t work, try again).\n\n'
        for i in options:
            answer = f'{answer}\t({options.index(i)+1})\t{i}\n'
        answer = f'{answer}\nPlease enter the digit of the menu point you want to choose.'
        return answer


class GAME:
    def __init__(self, adventure=None, a=None, conditions=None,
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
        to_be_saved = self
        if self.triggering is not None:
            self.a = message
            answer = self.triggering.call(self.adventure, self.triggering, self, self.trigger_counter, message=message)
            if isinstance(answer, str):
                self.trigger_counter = self.trigger_counter + 1
            elif hasattr(answer, 'adventure'):  # isinstance(answer, GAME)
                self.triggering = None
                self.trigger_counter = 0
                to_be_saved = answer
                answer = 'please enter'
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
                    to_be_saved = self
            elif hasattr(answer, 'adventure'):
                to_be_saved = answer
                answer = 'Took back your last input.'
            else:
                to_be_saved = self
        with open('data.json', 'r') as f:
            data = json.load(f)
        for i in self.adventure.major_secrets:
            if i.name.lower() == "won" and i.found:
                data['players'][username]['running'] = None
        while len(data['players'][username][self.adventure.name]) > 3:
            del data['players'][username][self.adventure.name][0]
        data['players'][username][self.adventure.name].append(jsonpickle.encode(to_be_saved, keys=True))
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        pos = f'You are here: playing/{self.adventure.name}/{self.scene.location.name}/{self.object_of_interest.name}\n\n'
        if not isinstance(answer, str):
            answer = 'please enter'
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
                with open('data.json', 'r') as f:
                    data = json.load(f)
                saves = data['players'][username][self.adventure.name]
                if len(saves) > 1:
                    b = jsonpickle.decode(saves[-2], keys=True)  # test this
                    saves.pop()
                    saves.pop()
                    data['players'][username][self.adventure.name] = saves
                    with open('data.json', 'w') as f:
                        json.dump(data, f, indent=4)
                else:
                    b = 'Can\'t take back'
                print('Taking back your last input does not work yet. Sorry.')
                pass
            elif a.startswith('/e'):
                with open('data.json', 'r') as f:
                    data = json.load(f)
                data['players'][username]['running'] = None
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
            elif a.startswith('/l'):
                b = 'Here is everything you know:\n'
                j = 0
                for i in self.adventure.major_secrets:
                    if i.found and i.active:
                        j = j+1
                        b = f'{b}{j}.\t{i.name}\n'
            elif a.startswith('/c'):
                l = []
                for i in self.adventure.major_secrets:
                    if i.active and i.clue and not i.found:
                        l.append(i)
                clue = random.choice(l)
                clue.found = True
                b = f'Here is your clue: {clue.name}.{clue.description}'
            elif a.startswith('/h'):
                b = (
                    f'Here are all commands and what they do:\n'
                    f'\t"/b" or "/back"\t\t\tThis command takes back your last input.\n'
                    f'\t"/h" or "/help"\t\t\t This command lists and explains all commands.\n'
                    f'\t"/l" or "/log"\t\t\t\t This command lists everything you have already found and collected.\n'
                    f'\t"/c" or "/clue"\t\t\t This command gives you a clue on how to proceed.\n'
                    f'\t"/d" or "/describe"\t This command lists all the data of the current scene.\n'
                    f'\nThe following commands need a normal statement after the command:\n'
                    f'\t\t\tE. g. "/info What do I see?"\n'
                    f'\t"/i" or "/info"\t\t\t\t  This command classifies the following statement as an info question.\n'
                    f'\t"/a" or "/action"\t\t\t This command classifies the following statement as an action.\n'
                    f'\t"/v" or "/verbatim"\t\tThis command classifies the following statement as verbatim (speech).\n'
                    f'\t"/t" or "/talk"\t\t\t\t This command classifies the following statement as an attempt to\n'
                    f'\t\t\t\t\tstart a conversation.\n'
                    f'\t"/f" or "/fight"\t\t\t\tThis command classifies the following statement as an aggressive action.\n'
                    f'\t"/r" or "/room change"\t\tThis command classifies the following statement as a room change.\n'
                )
            elif a.startswith('/d'):
                b = f'Scene type: {self.scene.type}\nLocation: {self.scene.location.name}\nAmount of npcs: {str(len(self.scene.npcs))}'
                for j in self.scene.npcs:
                    b = b + '\nNPC: ' + j.name
                b = b + '\nAmount of secrets: ' + str(len(self.scene.secrets))
                for j in self.scene.secrets:
                    b = b + '\nSecret: ' + j.name
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
                return 'Command not understood, see \'/help\' for help on commands.'
            # commands: back, log (inventory and secrets), clue, help, /mastertype a, describe scene (analyse)
            # '/b, /i, /c, /h, /d, /l, /a, /v, /t, /f, /r'
            return b
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

    def check_for_skill(self, username, type):
        with open('data.json', 'r') as f:
            data = json.load(f)
        pc = data['players'][username]['characters'][data['players'][username]['current_PC']]
        if 'skills' in pc:
            for i in pc['skills'].keys():
                if i in self.a and type == data['skills'][i]['type']:
                    answer = skills.main(username, self.a, i, self)
                    if answer is not None:
                        return answer
                    break
        return None

    def info(self, username=None):
        answer = self.check_for_skill(username, 'knowledge')
        if answer is not None:
            return answer
        if isinstance(self.object_of_interest, adventure_structure.NPC):
            return self.object_of_interest.talk(self.a)  # Why are here no secrets???
        elif isinstance(self.object_of_interest, adventure_structure.LOCATION):
            return self.object_of_interest.describe(self.a) # Why are here no secrets???
        else:
            return 'Error <info>'

    def action(self, username=None):
        answer = self.check_for_skill(username, 'action')
        if answer is not None:
            return answer
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
        answer = self.check_for_skill(username, 'social')
        if answer is not None:
            return answer
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
            loc = con[0]
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
        if isinstance(answer, bool):
            answer = self.scene.location.describe(npcs=self.scene.npcs)
            answer = secret_finder(self.scene.secrets, self.object_of_interest, answer)

        return f'You are going to the {loc.name}.\n{answer}'

    def fight(self, username=None):
        answer = self.check_for_skill(username, 'fight')
        if answer is not None:
            return answer
        # Three options on where to attack (random but for one fight constant sequence of 0;1;2 where to hit.).
        # length of sequence varies randomly between 3 and 5. (also constant for one fight.)
        return 'You are fighting. Which fighting skills do you want to use?'

    def talk(self, username=None):
        answer = self.check_for_skill(username, 'social')
        if answer is not None:
            return answer
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
    with open('fine_tuning.json', 'r') as f:
        data = json.load(f)
    data['newsample'].update({prompt: ' ' + response + '###'})
    with open('fine_tuning.json', 'w') as f:
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
        prompt = f'Secret: {i.description[object_of_interest]}\nText: {text}\n\nAnswer:'
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
        with open('fine_tuning.json', 'r') as f:
            data = json.load(f)
        data['newsecret_sample'].update({prompt: ' ' + mentioned.lower()[0] + '###'})
        with open('fine_tuning.json', 'w') as f:
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
    with open('fine_tuning.json', 'r') as f:
        data = json.load(f)
    data['newwho'].update({prompt: response + '###'})
    with open('fine_tuning.json', 'w') as f:
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
    with open('fine_tuning.json', 'r') as f:
        data = json.load(f)
    data['newwhere'].update({prompt: response + '###'})
    with open('fine_tuning.json', 'w') as f:
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
    with open('fine_tuning.json') as f:
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
