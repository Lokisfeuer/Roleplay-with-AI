# One secret needs to be called "won".
# No new scene is without npcs. (Why? Powerset should also give back an empty list) - test that
# - add class ITEM

import random
import math
import openai


def the_drowned_aboleth():
    # Triggers are checked at the beginning of each scene and after every action.
    def on_the_algebra(x):
        scene = x['scene']
        for i in scene.npcs:
            if i == captain or i == matthews:
                pass
            else:
                scene.npcs.remove(i)
        if scene.location == inside_ship:
            if sec_i.found:
                x['conditions'] = [ship, [captain]]
            else:
                if 'sort' in x.keys():
                    print('Matthews Joachim Karl von Phisa is bound and gagged lying in the prison cell.')
                    answer = input('Do you want to free Matthews? [Y/n]').lower()
                    if answer[0] == 'y':
                        print('You free Matthews.')
                        sec_i.found = True
                        scene.npcs.append(matthews)
                        x['conditions'] = [ship, [captain]]
                    else:
                        print('You do not free Matthews.')
        x['scene'] = scene
        return x

    def boss_fight(x):
        # just have an awesome boss fight, ending with setting "won" found.
        print('You and the captain are having an awesome boss fight. You win.')
        won.found = True
        return x

    def at_the_algebra(x):
        scene = x['scene']
        if not sec_h.found:
            if steve not in scene.npcs:
                scene.npcs.append(steve)
            if tom not in scene.npcs:
                scene.npcs.append(tom)
            if sec_g.found:
                sailors_helping = 0
                names = ''
                for i in sailors_help.keys():
                    if sec_j.found or not i == michael:
                        if sailors_help[i].found:
                            if sailors_helping == 0:
                                names = f' and {i.name}'
                            else:
                                names = f', {i.name}{names}'
                            sailors_helping = sailors_helping+1
                if sailors_helping > 1:
                    print(f'{names[1:]} could relieve the guards and let you on bord of the Algebra.')
                    if input('Should they do so? [Y/n]').lower()[0] == 'y':
                        sec_h.found = True
                        print(f'You can now proceed to the Algebra.')
        x['scene'] = scene
        return x

    def won(x):
        print('This is a great awesome sounding epilogue.')
        print('Thanks for playing!')
        x['running_adventure'] = False
        pass

    def loveletter(x):
        if sec_b.found:
            print('You can now deliver Johns loveletter to Isabella.')
            if input('Do you want to do so? [Y/n]').lower()[0] == 'y':
                sailors_help[piet].found = True
        return x

    def money(x):
        if sec_f.found:
            print('You can help out Greg with a little bit of your money.')
            if input('Do you want to do so? [Y/n]').lower()[0] == 'y':
                sailors_help[greg].found = True
        return x

    def alcohol(x):
        if sec_k.found:
            print('You can get Piet a bottle of liquor.')
            if input('Do you want to do so? [Y/n]').lower()[0] == 'y':
                sailors_help[piet].found = True
        return x

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
                  hostile=True, conditions=[sec_false])  # never active
    piet = NPC(name='Piet', description='Piet is an elderly sailor on the Algebra.')
    timmy = NPC(name='Timmy', description='Timmy is the kitchen boy on the Algebra. He has a friendly character.'
                                          'willing to do anyone a favor. He is a little scared of the captain.')
    matthews = NPC(name='Matthews Joachim Karl von Phisa',
                   description='Matthews Joachim Karl von Phisa is the oldest son of the Duke of Phisa. He is a '
                               'little arrogant and self-pitiful.',
                   conditions=[sec_false])
    robber = NPC(name='Robber', description='The robber is an intimidating figure with a knife in one hand.',
                 conditions=[sec_false])
    sec_h = SECRET(name='Guards relieved.', where_to_find=[])
    steve = NPC(name='Steve',
                description='Steve is guarding the Algebra. He takes care and allows nobody to pass through.',
                conditions=[sec_h])
    tom = NPC(name='Tom',
              description='Tom is protecting the Algebra. He takes care and allows nobody to pass through.',
              conditions=[sec_h])

    streets = LOCATION(name='streets', description='These are the dark streets of the village. The local tavern "The '
                                                   'drowned aboleth" can be found here.')
    tavern = LOCATION(name='tavern "The drowned aboleth"',
                      description='This is the local tavern "The drowned aboleth" which is the social centre of the '
                                  'village. The tavern is well filled, beer and alcoholic beverages flow in streams '
                                  'and there is generally good mood. On one of the walls a map of the local area with '
                                  'a nearby lighthouse can be seen.')
    sec_lighthouse = SECRET(name='There is an abandoned lighthouse nearby.',
                            where_to_find=[tavern, jack, isabella, michael, andrea])
    lighthouse = LOCATION(name='lighthouse',
                          description='The old lighthouse was abandoned years ago. There hasn\'t been a lighthouse'
                                      'keeper for ages.',
                          conditions=[sec_lighthouse])
    sec_bay = SECRET(name='There is a bay where the crew of the Algebra stores their goods.',
                     where_to_find=[john, jack, isabella, greg, piet, timmy, steve, tom, lighthouse])
    # check sec_bay [lighthouse] during testing.
    bay = LOCATION(name='bay', description='At this bay the crew of the Algebra is storing their smuggled goods. The '
                                           'bay is full with more or less valuable treasury.', conditions=[sec_bay])
    pier = LOCATION(name='pier', description='There is only a single vessel in the pier. It is the Algebra, '
                                             'a big sailing vessel with three masts. Two guards are standing in front '
                                             'of it, allowing nobody to enter who is not part of the crew.')
    ship = LOCATION(name='Algebra',
                    description='The Algebra is a big sailing vessel. It\'s got three masts. On the main deck is a'
                                'huge steering wheel and a hatch to go below deck.',
                    conditions=[sec_h])
    inside_ship = LOCATION(name='inner deck of the Algebra', description='Inside the Algebra are multiple smaller '
                                                                         'rooms, including a galley, a mess hall, '
                                                                         'a medical bay, a weapons storage room and '
                                                                         'the crew quarters as well as one cell with '
                                                                         'a prisoner.', conditions=[sec_h])

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
    sec_k = SECRET(name='Piet enjoys alcohol a little to much but he doesn\t get to have any on the Algebra.',
                   where_to_find=[piet, andrea])
    # Non-story-secrets:
    sailors_help = {}
    sailors_help.update({john: SECRET(name=f'{john.name} is willing to help the player.', where_to_find=[])})
    sailors_help.update({greg: SECRET(name=f'{greg.name} is willing to help the player.', where_to_find=[])})
    sailors_help.update({timmy: SECRET(name=f'{timmy.name} is willing to help the player.', where_to_find=[timmy])})
    sailors_help.update({michael: SECRET(name=f'{michael.name} is willing to help the player.', where_to_find=[michael])})
    sailors_help.update({piet: SECRET(name=f'{piet.name} is willing to help the player.', where_to_find=[])})
    # other_secrets:
    # sec_h = SECRET(name='Guards relieved.', where_to_find=[])
    sec_i = SECRET(name='Matthews freed.', where_to_find=[])
    sec_j = SECRET(name='Michael started on the Algebra.', where_to_find=[])
    # sec_false = SECRET(name='false', where_to_find=[])
    sec_won = SECRET(name='Won', where_to_find=[])
    # relevance=1, positive=True, found=False, conditions=None, description={}

    trig_a = TRIGGER(when_triggered=[inside_ship, ship], function=on_the_algebra)
    trig_b = TRIGGER(when_triggered=[captain], function=boss_fight)
    trig_c = TRIGGER(when_triggered=[pier], function=at_the_algebra)
    trig_d = TRIGGER(when_triggered=[sec_won], function=won)

    loveletter = TRIGGER(when_triggered=[isabella], function=loveletter)
    money = TRIGGER(when_triggered=[greg], function=money)
    alcohol = TRIGGER(when_triggered=[piet], function=alcohol)

    npcs = [john, jack, isabella, michael, andrea, greg, captain, piet, timmy, matthews, robber, steve, tom]
    locations = [streets, tavern, lighthouse, bay, ship, inside_ship]
    secrets = [sec_a, sec_b, sec_c, sec_d, sec_e, sec_f, sec_g, sec_h, sec_i, sec_j, sec_k, sec_won, sec_false,
               sec_lighthouse, sec_bay].extend(sailors_help.values())
    trigger = [trig_a, trig_b, trig_c, trig_d, loveletter, money, alcohol]
    starting_conditions = [streets, [robber]]

    the_drowned_aboleth = ADVENTURE(major_npcs=npcs, major_locations=locations, major_secrets=secrets, trigger=trigger,
                                    actionrelevance=0)
    return the_drowned_aboleth, starting_conditions

def play_family_adventure():
    thede = NPC(name='thede')
    sophie = NPC(name='sophie')
    mama = NPC(name='mama', hostile=True)
    papa = NPC(name='papa', hostile=True)
    npcs = [thede, sophie, mama, papa]

    wohnzimmer = LOCATION(name='wohnzimmer')
    kueche = LOCATION(name='kueche')
    locations = [wohnzimmer, kueche]

    abendessen = SECRET(name="Heute gibt es Tomatenrisotto", where_to_find=[kueche, papa])
    bettzeit = SECRET(name="Sophie muss um 20:00 ins Bett.", where_to_find=[mama, papa])
    beruhigen = SECRET(name="Thede kann Sophie beruhigen", where_to_find=[thede, mama])
    sieg = SECRET(name="won", where_to_find=[sophie])
    secrets = [sieg, abendessen, bettzeit, beruhigen]

    family_adventure = ADVENTURE(major_npcs=npcs, major_locations=locations, major_secrets=secrets)
    return family_adventure


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
        if secrets is None:
            prompt = self.prompt + '\n\nPerson: '
        else:
            secret_text = ''
            for i in secrets:
                secret_text = f'{secret_text}Secret: {i.description[self]}\n'
            prompt = f'{self.prompt}{self.name} knows some secrets.\n{secret_text}\nPerson: '
            # The single \n before person is correct.
        for i in range(min(len(self.former_inputs), 3)):
            prompt = f'{prompt}{self.former_inputs[i]}\n{self.name}: {self.former_answers[i]}\n\nPerson: '
        prompt = f'{prompt}{a}\n{self.name}: '
        response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0.8,
                                            max_tokens=150)
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
            self.description = description
        self.prompt = ''
        check_active(self)

    def describe(self, a=None, npcs=None, secrets=None):
        secret_text = ''
        if secrets is not None:
            for i in secrets:
                secret_text = f'{secret_text}{i.description[self]}.'
        if npcs is None:
            npcs = []
            names = ''
        else:
            names = npcs[0].name
        for i in npcs[1:]:
            names = f'{names}, {i.name}'
        if a is None:
            self.prompt = f'The locationAI describes a location and answers questions about it. The location is a ' \
                          f'{self.name}.{self.description} The following people are at the location: {names}.' \
                          f'\n\nPerson: What do I see at the location?\nLocationAI: '
        else:
            self.prompt = f'{self.prompt}{a}\nLocationAI: '
        response = openai.Completion.create(model="text-davinci-002", prompt=self.prompt, temperature=0.6,
                                            max_tokens=256)
        response = response['choices'][0]['text']
        self.prompt = f'{self.prompt}{response}\n\nPerson: '
        return response


class SECRET:
    def __init__(self, name, where_to_find, relevance=1, positive=True,
                 found=False, conditions=None, description=None):  # relevance is small for minor secrets.
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
        if description is None:
            self.description = {}
            for i in where_to_find:
                self.description.update({i: ''})
        else:
            for i in where_to_find:
                if i not in description.keys():
                    self.description.update({i: ''})
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


class ADVENTURE:  # To do: differ between active and inactive locations, npcs and secrets
    def __init__(self, setting=None, major_npcs=None, major_locations=None, major_secrets=None, actions=None,
                 trigger=None, actionrelevance=1, difficultyrelevance=1, hoperelevance=1):
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
        if trigger is None:
            self.trigger = []
        else:
            self.trigger = trigger
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
    # action (Trägheit?)
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
    # return [1, 0.1, 1, adventure]