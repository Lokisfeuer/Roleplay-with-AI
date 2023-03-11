# One secret needs to be called "won".
# No new scene is without npcs. (Why? Powerset should also give back an empty list) - test that
# - add class ITEM

import random
import math
import openai
import jsonpickle
import json
# from 'C:\\Users\\thede\\PycharmProjects\\Roleplay-with-AI\\adventure_structure.py' import 'main.py'
from main import GAME


def get_by_name(name, x):
    objs = []
    for i in [x.adventure.major_secrets, x.adventure.major_locations, x.adventure.major_npcs]:
        for j in i:
            if j.name.lower() == name.lower():
                objs.append(j)
    if len(objs) == 1:
        return objs[0]
    else:
        return None


def prolouge(self, x, counter, message=None):
    if self in x.adventure.trigger:
        x.adventure.trigger.remove(self)
    string = \
        f'You, as brave adventurer, have been hired by the very rich Duke of Philsa to find his kidnapped ' \
        f'son.\nSo you set out to find the kidnappers and tracked them to the small port town of Abolia. ' \
        f'You have now\n arrived there in the late evening. It is a dark night and the streets are almost' \
        f' empty. Only one ship\nwith the lettering "Algebra" lies at anchor. You head towards the only ' \
        f'lighted house - an inn called\n"The drowned Aboleth". As you walk towards the inn, a hooded figure ' \
        f'suddenly get in your way. He\npulls out a knife and points it at the leather pouch containing 100' \
        f' gold coins that the Baron gave\n you as a deposit. He says: "Give me the money, if you value your' \
        f'life".'
    if counter == 0:
        return string
    return True


def on_the_algebra(self, x, counter, message=None):
    if counter == 0:
        for i in x.scene.npcs:
            if i.name == 'captain' or i.name == 'matthews':
                pass
            else:
                x.scene.npcs.remove(i)
        if x.scene.location.name == 'Under deck Algebra':
            if get_by_name('Matthews freed', x).found:
                x.conditions = [get_by_name('Top deck Algebra', x), [get_by_name('Captain', x)]]
            else:
                if x.sort is not None:
                    string = 'Matthews Joachim Karl von Philsa is bound and gagged lying in the prison cell.\n' \
                             'Do you want to free Matthews? [Y/n]'
                    return string
    elif x.scene.location.name == 'Under deck Algebra' and counter == 1 and not get_by_name('Matthews freed', x).found:
        answer = x.a.lower()
        if answer[0] == 'y':
            string = 'You free Matthews.'
            get_by_name('Matthews freed', x).found = True
            x.scene.npcs.append(get_by_name('Matthews Joachim Karl von Philsa', x))
            x.conditions = [get_by_name('Top deck Algebra', x), [get_by_name('Captain', x)]]
        else:
            string = 'You do not free Matthews.'
        return string
    return True


def boss_fight(self, x, counter, message=None):
    # just have an awesome boss fight, ending with setting "won" found.
    if counter == 0:
        get_by_name('won', x).found = True
        x.adventure.trigger.remove(self)
        return 'You and the captain are having an awesome boss fight. You win.'
    return False


def at_the_algebra(self, x, counter, message=None):
    if not get_by_name('Guards relieved.', x).found:
        if get_by_name('Steve', x) not in x.scene.npcs:
            x.scene.npcs.append(get_by_name('Steve', x))
        if get_by_name('Tom', x) not in x.scene.npcs:
            x.scene.npcs.append(get_by_name('Tom', x))
        if get_by_name('Any two members of the crew of the Algebra can relieve the guards of the Algebra.', x).found:
            sailors_helping = 0
            names = ''
            sailors_help = {}
            for i in ['Michael', 'John', 'Piet', 'Greg']:
                sailors_help.update(
                    {get_by_name(i, x): get_by_name(f'{get_by_name(i, x).name} is willing to help the player.', x)})
            for i in sailors_help.keys():
                if get_by_name('Michael started on the Algebra.', x).found or i != get_by_name('Michael', x):
                    if sailors_help[i].found:
                        if sailors_helping == 1:
                            names = f'{names} and {i.name}'
                        else:
                            names = f', {i.name}{names}'
                        sailors_helping = sailors_helping + 1
            if sailors_helping > 1:
                if counter == 0:
                    return f'{names[2:]} could relieve the guards and let you on bord of the Algebra.\nShould they do so? [Y/n]'
                elif counter == 1 and x.a.lower().startswith('y'):
                    get_by_name('Guards relieved.', x).found = True
                    return f'You can now proceed to the Algebra.'
    return True


# replace everything from outer function and set them out of function.
def won(self, x, counter, message=None):
    if counter == 0:
        get_by_name('Won', x).found = True
        return 'This is a great, awesome sounding, really inspiring and epic epilogue. Thanks for playing!'
    elif counter == 1:
        if get_by_name('Won', x).found:
            get_by_name('Won', x).found = False
            return 'You already played through this adventure. Do you want to restart from the beginning? [Y/n]'
    else:
        if x.a.lower().startswith('y'):
            with open('data.json', 'r') as f:
                data = json.load(f)
            conditions = jsonpickle.decode(data['adventures']['the drowned aboleth']['conditions'], keys=True)
            adv = jsonpickle.decode(data['adventures']['the drowned aboleth']['adventure'], keys=True)
            game = GAME(adventure=adv, conditions=conditions)
            return game
        elif x.a.lower().startswith('n'):
            get_by_name('Won', x).found = True
            x.trigger_counter = 0
            return 'Adventure is not being restarted. You will be directed to the main menu.'
        else:
            if get_by_name('Won', x).found:
                get_by_name('Won', x).found = False
            return 'You already played through this adventure. Do you want to restart from the beginning? [Y/n]'


def loveletter(self, x, counter, message=None):
    if get_by_name('John is in love with Isabella and wants the players to bring her a loveletter from him.', x).found:
        if counter == 0:
            return 'You can now deliver Johns loveletter to Isabella.\nDo you want to do so? [Y/n]'
        else:
            if x.a.lower().startswith('y'):
                get_by_name(f'John is willing to help the player.', x).found = True
            x.adventure.trigger.remove(self)
    return True


def money(self, x, counter, message=None):
    if 'Greg' == x.object_of_interest.name:
        if get_by_name('Greg has a gambling problem and desperately needs money.', x).found:
            if counter == 0:
                return 'You can help out Greg with a little bit of your money.\nDo you want to do so? [Y/n]'
            else:
                if x.a.lower().startswith('y'):
                    get_by_name('Greg is willing to help the player.', x).found = True
                    x.adventure.trigger.remove(self)
    return True


def alcohol(self, x, counter, message=None):
    if get_by_name('Piet enjoys alcohol a little to much but he doesn\'t get to have any on the Algebra.', x).found:
        if counter == 0:
            return 'Piet seems pretty broke and asks you for a bottle of liquor. You can get him a bottle.\nDo you ' \
                   'want to do so? [Y/n] '
        else:
            if self in x.adventure.trigger:
                x.adventure.trigger.remove(self)
                if x.a.lower().startswith('y'):
                    get_by_name('Piet is willing to help the player.', x).found = True
                    return 'Piet thanks you very much. If you ever need anything from him, he is happy to help.'
                else:
                    return 'You do not give Piet a bottle.'
    return True


def secret_message(self, x, counter, message=None):
    if get_by_name('There is a message given to the players saying that Matthews is being held on the Algebra.',
                   x).found:
        if counter == 0:
            string = \
                'You find a message in your pocket. Somebody must have smuggled it into there. It says the ' \
                'following:\nI, Matthews Joseph Charles of Philsa, son of the duke of Philsa am being held against ' \
                'my will on the Algebra. My father would be willing to pay great amounts for my rescue. Please help ' \
                'me!!!'
            x.adventure.trigger.remove(self)
            return string
    return True


def the_drowned_aboleth(prolouge, on_the_algebra, boss_fight, at_the_algebra, won, loveletter, money, alcohol,
                        secret_message):
    # Triggers are checked at the beginning of each scene and after every action.

    sec_false = SECRET(name='false', where_to_find=[])

    john = NPC(name='John', description='John is a sailor on the Algebra.')
    jack = NPC(name='Jack', description='Jack is an elderly fisherman. He is very scared of the sea.')
    isabella = NPC(name='Isabella', description='Isabella is a thief. She lives in the abandoned lighthouse '
                                                'nearby. Usually she just steals food but if she gets the chance she '
                                                'might also take some things of value.')
    michael = NPC(name='Michael', description='He works for his mother in the local tavern "The drowned aboleth" '
                                              'where he is rather unhappy. ')
    andrea = NPC(name='Andrea', description='Andrea is Michael\'s mother. She is the innkeeper and owner of the local '
                                            'tavern "The drowned aboleth".')
    greg = NPC(name='Greg', description='Greg is a sailor on the Algebra.')
    captain = NPC(name='Captain',
                  description='The captain wears a big captain\'s hat. In one hand he holds a saber and '
                              'in the other one he carries a shotgun.',
                  hostile=True, conditions=[{sec_false: True}])  # never active
    piet = NPC(name='Piet', description='Piet is an elderly sailor on the Algebra.')
    timmy = NPC(name='Timmy', description='Timmy is the kitchen boy on the Algebra. He has a friendly character.'
                                          'willing to do anyone a favor. He is a little scared of the captain.')
    matthews = NPC(name='Matthews Joachim Karl von Philsa',
                   description='Matthews Joachim Karl von Philsa is the oldest son of the Duke of Philsa. He is a '
                               'little arrogant and self-pitiful.',
                   conditions=[{sec_false: True}])
    robber = NPC(name='Robber', description='The robber is an intimidating figure with a knife in one hand.',
                 conditions=[{sec_false: True}])
    sec_h = SECRET(name='Guards relieved.', where_to_find=[])
    steve = NPC(name='Steve',
                description='Steve is guarding the Algebra. He takes care and allows nobody to pass through.',
                conditions=[{sec_h: True}])
    tom = NPC(name='Tom',
              description='Tom is protecting the Algebra. He takes care and allows nobody to pass through.',
              conditions=[{sec_h: True}])

    streets = LOCATION(name='streets', description='These are the dark streets of the village. The local tavern "The '
                                                   'drowned aboleth" can be found here.')
    tavern = LOCATION(name='tavern',
                      description='This is the local tavern "The drowned aboleth" which is the social centre of the '
                                  'village. The tavern is well filled, beer and alcoholic beverages flow in streams '
                                  'and there is generally good mood. On one of the walls a map of the local area with '
                                  'a nearby lighthouse can be seen.')
    sec_lighthouse = SECRET(name='There is an abandoned lighthouse nearby.',
                            where_to_find=[tavern, jack, isabella, michael, andrea])
    lighthouse = LOCATION(name='lighthouse',
                          description='The old lighthouse was abandoned years ago. There hasn\'t been a lighthouse'
                                      'keeper for ages.',
                          conditions=[{sec_lighthouse: True}])
    sec_bay = SECRET(name='There is a bay where the crew of the Algebra stores their goods.',
                     where_to_find=[john, jack, isabella, greg, piet, timmy, steve, tom, lighthouse])
    # check sec_bay [lighthouse] during testing.
    bay = LOCATION(name='bay', description='At this bay the crew of the Algebra is storing their smuggled goods. The '
                                           'bay is full with more or less valuable treasury.',
                   conditions=[{sec_bay: True}])
    pier = LOCATION(name='pier', description='There is only a single vessel in the pier. It is the Algebra, '
                                             'a big sailing vessel with three masts. If they are here Tom and Jerry'
                                             'are guarding the Algebra.')
    ship = LOCATION(name='Top deck Algebra',
                    description='The Algebra is a big sailing vessel. It\'s got three masts. On the main deck is a'
                                'huge steering wheel and a hatch to go below deck.',
                    conditions=[{sec_h: True}])
    inside_ship = LOCATION(name='Under deck Algebra', description='Inside the Algebra are multiple smaller '
                                                                  'rooms, including a galley, a mess hall, '
                                                                  'a medical bay, a weapons storage room and '
                                                                  'the crew quarters as well as one cell with '
                                                                  'a prisoner.', conditions=[{sec_h: True}])

    # Story-secrets:
    sec_a = SECRET(name='There is a message given to the players saying that Matthews is being held on the Algebra.',
                   where_to_find=[timmy, tavern])
    sec_b = SECRET(name="John is in love with Isabella and wants the players to bring her a loveletter from him.",
                   where_to_find=[john])
    sec_c = SECRET(name="Jack owns a little boat with which you can approach the Algebra from the unguarded seaside.",
                   where_to_find=[jack, andrea])  # let's ignore this for the first tests.
    sec_d = SECRET(name="Micheal plans to sign on the Algebra.",
                   where_to_find=[michael, michael])
    sec_e = SECRET(name="Isabella lives in the abandoned lighthouse.",
                   where_to_find=[isabella, lighthouse, michael])
    sec_f = SECRET(name="Greg has a gambling problem and desperately needs money.",
                   where_to_find=[greg, andrea])
    sec_g = SECRET(name='Any two members of the crew of the Algebra can relieve the guards of the Algebra.',
                   where_to_find=[john, greg, piet, timmy, steve, tom])
    sec_k = SECRET(name='Piet enjoys alcohol a little to much but he doesn\'t get to have any on the Algebra.',
                   where_to_find=[piet, andrea])
    # Non-story-secrets:
    sailors_help = {}
    sailors_help.update({john: SECRET(name=f'{john.name} is willing to help the player.', where_to_find=[])})
    sailors_help.update({greg: SECRET(name=f'{greg.name} is willing to help the player.', where_to_find=[])})
    sailors_help.update({timmy: SECRET(name=f'{timmy.name} is willing to help the player.', where_to_find=[timmy])})
    sailors_help.update(
        {michael: SECRET(name=f'{michael.name} is willing to help the player.', where_to_find=[michael])})
    sailors_help.update({piet: SECRET(name=f'{piet.name} is willing to help the player.', where_to_find=[])})
    # other_secrets:
    # sec_h = SECRET(name='Guards relieved.', where_to_find=[])
    sec_i = SECRET(name='Matthews freed', where_to_find=[])
    sec_j = SECRET(name='Michael started on the Algebra.', where_to_find=[])
    # sec_false = SECRET(name='false', where_to_find=[])
    sec_won = SECRET(name='Won', where_to_find=[])
    # relevance=1, positive=True, found=False, conditions=None, description={}

    triggerfunctions = [prolouge, on_the_algebra, boss_fight, at_the_algebra, won, loveletter, money, alcohol,
                        secret_message]

    trig_a = TRIGGER(when_triggered=[inside_ship, ship], function=on_the_algebra)
    trig_b = TRIGGER(when_triggered=[captain], function=boss_fight)
    trig_c = TRIGGER(when_triggered=[pier], function=at_the_algebra)
    trig_d = TRIGGER(when_triggered=[sec_won], function=won)

    loveletter = TRIGGER(when_triggered=[isabella], function=loveletter)
    money = TRIGGER(when_triggered=[greg], function=money)
    alcohol = TRIGGER(when_triggered=[piet], function=alcohol)
    secret_message = TRIGGER(when_triggered=[tavern], function=secret_message)
    prolouge = TRIGGER(when_triggered=[streets], function=prolouge)

    npcs = [john, jack, isabella, michael, andrea, greg, captain, piet, timmy, matthews, robber, steve, tom]
    locations = [streets, tavern, lighthouse, bay, ship, inside_ship, pier]
    secrets = [sec_a, sec_b, sec_c, sec_d, sec_e, sec_f, sec_g, sec_h, sec_i, sec_j, sec_k, sec_won, sec_false,
               sec_lighthouse, sec_bay]
    secrets.extend(sailors_help.values())
    trigger = [prolouge, trig_a, trig_b, trig_c, trig_d, loveletter, money, alcohol, secret_message]
    starting_conditions = [streets, [robber]]

    trigger_dict = {}
    for trigger, function in zip(trigger, triggerfunctions):
        trigger_dict.update({trigger: function})

    name = 'the drowned aboleth'
    adventure = ADVENTURE(name=name, major_npcs=npcs, major_locations=locations, major_secrets=secrets,
                          actionrelevance=0, trigger_dict=trigger_dict)
    with open('data.json', 'r') as f:
        data = json.load(f)
    data['adventures'].update({name: {
        'adventure': jsonpickle.encode(adventure, keys=True),
        'conditions': jsonpickle.encode(starting_conditions, keys=True)
    }})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return adventure, starting_conditions


def get_next_scene(adventure, all_former_scenes=None, conditions=None):
    if all_former_scenes is None:
        all_former_scenes = []
    if conditions is None:
        conditions = [None, [None]]
    scenes = adventure.create_scenes(conditions)
    values = []
    total = 0
    for i in scenes:
        inputs = evaluate_getinputs(all_former_scenes, adventure)
        value = i.evaluate(inputs[0], inputs[1], inputs[2], inputs[3])
        values.append(value)
        total = total + value
    p = []
    for i in values:
        p.append(i / total)
    scene = random.choices(population=scenes, weights=p, k=1)[0]
    return scene


class NPC:
    def __init__(self, name, hostile=False, conditions=None, description=None):
        self.name = name
        self.hostile = hostile
        self.conditions = conditions
        self.active = None
        if description is None:
            self.description = ''
        else:
            self.description = description
        self.prompt = f'The following is a conversation between {self.name} and a person. {self.description} '
        # Proper grammar and Spelling! Ends with "."; Includes the secrets and how he talks about them.
        self.former_inputs = []
        self.former_answers = []
        check_active(self)

    def talk(self, a, secrets=None):
        # check prompt propperly
        if secrets is None:
            prompt = self.prompt + '\n\nPerson: '
        else:
            secret_text = ''
            for i in secrets:
                secret_text = f'{secret_text}Secret: {i.description[self]}\n'
            prompt = f'{self.prompt}{self.name} knows some secrets and loves to talk about them.' \
                     f'\n{secret_text}\nPerson: '
            # The single \n before person is correct.
        for i in range(min(len(self.former_inputs), 3)):
            prompt = f'{prompt}{self.former_inputs[i]}\n{self.name}: {self.former_answers[i]}\n\nPerson: '
        prompt = f'{prompt}{a}\n{self.name}: '  # logical error, Person: I talk to the bartender.
        response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0.4,
                                            max_tokens=100, stop='Person:')
        response = response['choices'][0]['text']
        self.former_inputs.append(a)
        self.former_answers.append(response)
        return response

    def fight(self, a=None):
        return f'{self.name} does not want to fight you.'


class LOCATION:
    def __init__(self, name, conditions=None, description=None):
        self.name = name
        self.active = None
        self.conditions = conditions
        if description is None:
            self.description = ''
        else:
            if description[0] == '\n':
                self.description = description
            else:
                self.description = '\n' + description
        self.prompt = ''
        check_active(self)

    def describe(self, a=None, npcs=None, secrets=None):
        secret_text = '\nIf someone looks around closely they might find the following secrets:\n'
        if secrets is not None:
            for i in secrets:
                secret_text = f'{secret_text}{i.description[self]}.'
        else:
            secret_text = ''
        if npcs is None or npcs == []:
            npcs = []
            names = ''
            per_text = ''
        else:
            names = npcs[0].name
            for i in npcs[1:]:
                names = f'{names}, {i.name}'
            per_text = f'\nThe following people are at the location: {names}.'
        if a is None:
            self.prompt = f'The locationAI describes a location and answers questions about it. The location is a ' \
                          f'{self.name}.{self.description}{per_text}' \
                          f'{secret_text}\n\nPerson: What do I see at the location?\nLocationAI: '  # trailing space )-:
        else:
            self.prompt = f'{self.prompt}{a}\nLocationAI: '
        # This prompt sometimes leads to no answer based on prior not answering.
        response = openai.Completion.create(model="text-davinci-002", prompt=self.prompt, temperature=0.8,
                                            max_tokens=256, stop='Person')
        response = response['choices'][0]['text']
        self.prompt = f'{self.prompt}{response}\n\nPerson: '
        return response


class SECRET:
    def __init__(self, name, where_to_find, relevance=1, positive=True,
                 found=False, conditions=None, description=None, clue=True):  # relevance is small for minor secrets.
        self.name = name
        self.where_to_find = where_to_find  # list of NPCs and or locations.
        self.relevance = relevance
        self.positive = positive
        if self.positive:
            self.effect = relevance
        else:
            self.effect = -1 * relevance
        self.found = found
        self.conditions = conditions
        self.description = description
        self.prompt = ''
        if isinstance(description, str):
            self.description = {}
            for i in where_to_find:
                self.description.update({i: description})
        elif description is None:
            self.description = {}
            for i in where_to_find:
                self.description.update({i: self.name})
        else:
            for i in where_to_find:
                if i not in description.keys():
                    self.description.update({i: self.name})
        self.clue = clue
        check_active(self)


'''
class ITEM:
    def __init__(self, name, where_to_find, change_of_abilities=None, secret=None):
        self.name = name
        self.where_to_find = where_to_find
        self.change_of_abilities = change_of_abilities
        if secret is None:
            self.secret = SECRET(name=f'item {name} found')
        else:
            self.secret = secret
        check_active(self)
'''


class SETTING:
    def __init__(self, name, npcs=None, locations=None, secrets=None):
        self.name = name
        if npcs is None:
            self.npcs = []
        else:
            self.npcs = npcs
        if locations is None:
            self.locations = []
        else:
            self.locations = locations
        if secrets is None:
            self.secrets = []
        else:
            self.secrets = secrets


class SCENE:
    def __init__(self, location, npcs, secrets):
        self.location = location
        self.npcs = npcs
        self.secrets = secrets
        self.type = 'exploration'
        if len(npcs) != 0:
            self.type = 'social interaction'
        for i in self.npcs:
            if i.hostile:
                self.type = 'fight'
        self.difficulty = 0.5  # a percentage chance of failure.
        self.hope = 0
        for i in self.secrets:
            if i.positive:
                self.hope = self.hope + i.relevance
            else:
                self.hope = self.hope + i.relevance * (-1)
        type_to_number = {'fight': 1, 'social interaction': 0, 'exploration': -1}
        self.action = type_to_number[self.type]

    def evaluate(self, idealaction, idealdifficulty, idealhope, adventure):
        relevance_sum = adventure.actionrelevance + adventure.difficultyrelevance + adventure.hoperelevance
        relevance_sum = relevance_sum / 3
        action_relevance = adventure.actionrelevance / relevance_sum
        difficulty_relevance = adventure.difficultyrelevance / relevance_sum
        hope_relevance = adventure.hoperelevance / relevance_sum
        x = abs(self.action - idealaction) * action_relevance
        y = abs(self.difficulty - idealdifficulty) * difficulty_relevance
        z = pow(abs(self.hope - idealhope), 0.5) * pow(0.5, 0.5) * hope_relevance  # sqrt to get proper dimensions
        return pow(math.exp((-1) * (x + y + z)), 2)

    def __eq__(self, other):
        if not isinstance(other, SCENE):
            return NotImplemented
        return self.location == other.location and self.npcs == other.npcs and self.secrets == other.secrets

    def __hash__(self):
        return hash((self.location, self.npcs, self.secrets))
        # makes scenes hashable (they work in dicts and sets)


class TRIGGER:
    def __init__(self, when_triggered, function):
        # 4 Things can trigger: 1. Talking to a NPC, 2. Fighting a NPC, 3. Searching a location and 4. finding a secret
        self.when_triggered = when_triggered
        self.function = function
        pass

    def call(self, adventure, *args, **kwargs):
        function = adventure.trigger_dict[self]
        return function(*args, **kwargs)


class ADVENTURE:  # To do: differ between active and inactive locations, npcs and secrets
    def __init__(self, name, setting=None, major_npcs=None, major_locations=None, major_secrets=None, actions=None,
                 trigger_dict=None, actionrelevance=1, difficultyrelevance=1, hoperelevance=1):
        self.name = name
        self.seed = None
        if isinstance(setting, SETTING):
            self.setting = setting
        else:
            self.setting = SETTING('empty')
        if major_npcs is None:
            self.major_npcs = []
        else:
            self.major_npcs = major_npcs
        if major_locations is None:
            self.major_locations = []
        else:
            self.major_locations = major_locations
        if major_secrets is None:
            self.major_secrets = []
        else:
            self.major_secrets = major_secrets
        if actions is None:
            self.actions = []
        else:
            self.actions = actions
        if trigger_dict is None:
            self.trigger = []
            self.trigger_dict = {}
        else:
            self.trigger_dict = trigger_dict
            self.trigger = list(self.trigger_dict.keys())
        self.actionrelevance = actionrelevance
        self.difficultyrelevance = difficultyrelevance
        self.hoperelevance = hoperelevance

    def create_scene(self):
        location = self.seed[0]
        npcs = self.seed[1]
        secrets = []
        for i in (self.major_secrets + self.seed[2]):
            if i.active:
                add = False
                for j in i.where_to_find:
                    if j == location:
                        add = True
                    if j in npcs:
                        add = True
                if add:
                    secrets.append(i)
        scene = SCENE(location, npcs, secrets)
        return scene

    def create_scenes(self, conditions):
        tocheck = [self.major_secrets, self.setting.secrets, self.major_npcs, self.setting.npcs, self.major_locations,
                   self.setting.locations]
        for i in tocheck:
            for j in i:
                check_active(j)
        #  check whether to add stuff to the active lists from the inactive.
        self.seed = [0, 0, 0]  # [location, npcs, secrets]
        scenes = []
        if isinstance(conditions[0], LOCATION):
            total_loc = [conditions[0]]
        else:
            t = self.major_locations + self.setting.locations
            total_loc = []
            for i in t:
                if i.active:
                    total_loc.append(i)
        if not isinstance(conditions[1], list):
            print('Conditions are wrongly listed! (To prevent an error conditions[1] = [conditions[1]]')
            conditions[1] = [conditions[1]]
        if len(conditions[1]) == 0:
            total_npc = [[]]
        elif isinstance(conditions[1][0], NPC):
            total_npc = [conditions[1]]
        else:
            t = self.major_npcs + self.setting.npcs
            total_npc = []
            for i in t:
                if i.active:
                    total_npc.append(i)
            total_npc = list(powerset(total_npc))
        t = self.setting.secrets
        total_sec = []
        for i in t:
            if i.active:
                total_sec.append(i)
        total_sec = list(powerset(total_sec))  # also needs to be somehow related to their where_to_find
        for i in total_loc:
            for j in total_npc:
                for k in total_sec:
                    self.seed = [i, j, k]
                    scenes.append(self.create_scene())
        return scenes


def check_active(object_to_check):
    if object_to_check.conditions is None:
        object_to_check.active = True
        return True
    else:
        if isinstance(object_to_check.conditions, list):
            for i in object_to_check.conditions:
                object_to_check.active = True
                for j in i.keys():
                    # The error caused here is due to the fact, that the captain's conditions haven't fully been decoded
                    if not j.found == i[j]:
                        object_to_check.active = False
                        break
                if object_to_check.active:
                    return True
        else:
            object_to_check.active = True
            for i in object_to_check.conditions.keys():
                if not i.found == object_to_check.conditions[i]:
                    object_to_check.active = False
                    return False
            return True


def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


def evaluate_getinputs(former_scenes, adventure):  # former_scenes[0] is the oldest scene. new ones are being appended.
    # hope & fear
    # difficulty
    # action (Inertia?)
    type_to_number = {'fight': 1, 'social interaction': 0, 'exploration': -1}
    try:
        x = len(former_scenes)
        all_weights = 0
        idealaction = 0
        idealdifficulty = 0
        idealhope = 0
        for i in range(x):
            weight = (1 / math.exp((x - i - 1) / math.e))
            all_weights = all_weights + weight
            idealaction = idealaction + (weight * type_to_number[former_scenes[i].type] * (-1))
            idealdifficulty = idealdifficulty + (weight * (1 - former_scenes[i].difficulty))
            idealhope = idealhope + (weight * former_scenes[i].hope * (-1))
        idealaction = pow(abs(idealaction / all_weights), 1 / 4) * (
                idealaction / abs(idealaction))  # square root to prevent stagnation on 0
        idealdifficulty = idealdifficulty / all_weights
        idealhope = idealhope / all_weights
        idealhope = (idealhope / abs(idealhope)) * (
                pow(abs(idealhope), 0.5) * pow(2, 0.5)) + 1  # square root * sqrt(2) to let it approach 2
        return [idealaction, idealdifficulty, idealhope, adventure]
    except ZeroDivisionError:
        # print('A zero division error occurred and I am to lazy to fix it so I just gave you standard ideal values.')
        return [1, 0.1, 1, adventure]
    except TypeError:
        print('wrong format of list of former scenes was given.')
        return [1, 0.1, 1, adventure]

    # except:
    # print("Something went wrong (evaluate_getinputs) <!><!><!><!><!><!><!><!><!><!><!><!><!><!><!><!><!><!><!>")
    # return


trigger = [prolouge, on_the_algebra, boss_fight, at_the_algebra, won, loveletter, money, alcohol, secret_message]
# adventure, conditions = the_drowned_aboleth(*trigger)
