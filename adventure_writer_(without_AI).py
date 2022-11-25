

# Major Secrets werden immer bei erster Gelegenheit gefunden. (Gut so!)
# One secret needs to be called "won".
# No new scene is without npcs.

import random
import math

settings = []


def main():
    global settings
    settings = {
        'test': SETTING('test', npcs=[NPC('Una'), NPC('Jerry')], locations=[LOCATION('School'), LOCATION('house')])}
    play_mumsadventure()


def play_irishadventure():
    valentin = NPC('Valentin')
    brendon = NPC('Brendon')
    npcs = [valentin, brendon]
    ireland = LOCATION('Ireland')
    locations = [ireland, LOCATION('Germany')]
    secret = SECRET('chocolatebarsinvalentinsdesk', where_to_find=[ireland, valentin])
    irishadventure = ADVENTURE(major_npcs=npcs, major_locations=locations, major_secrets=[secret])
    play(irishadventure)


def play_mumsadventure():
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

    mumsadventure = ADVENTURE(major_npcs=npcs, major_locations=locations, major_secrets=secrets)

    play(mumsadventure, analyse=False)


def play(adventure, conditions=None, analyse=True):
    if conditions is None:
        conditions = [None, [None]]
    former_scenes = []
    if analyse:
        for i in range(10):
            scene = get_next_scene(adventure=adventure, all_former_scenes=former_scenes, conditions=conditions)
            print(type(scene))
            print('location: ' + scene.location.name)
            print('amount of npcs: ' + str(len(scene.npcs)))
            for j in scene.npcs:
                print('NPC: ' + j.name)
            print('amount of secrets: ' + str(len(scene.secrets)))
            for j in scene.secrets:
                print('Secret: ' + j.name)
            former_scenes.append(scene)
            conditions = [None, [None]]  # should depend on last scene.
    else:  # a mini engine.
        end = False
        while not end:
            scene = get_next_scene(adventure=adventure, all_former_scenes=former_scenes, conditions=conditions)
            answers = []
            print(f"You are in {scene.location.name}.")
            if scene.npcs == 0:
                print("There is no one else here.")
            elif scene.npcs == 1:
                print("There is one other person here.")
            else:
                print(f'There are {len(scene.npcs)} other persons here.')
            for i in scene.npcs:
                print(f'{i.name} is here.')
                answers.append(i.name)
            if scene.type == 'fight':
                for i in scene.npcs:
                    if i.hostile:
                        print(f'{i.name} attacks you.')
                print('If you want to fight back, type the name of the person you want to attack.')
            elif scene.type == 'social interaction':
                print('If you want to talk to someone, type their name.')
            else:
                print(f'You can search the {scene.location.name}. To do so type "{scene.location.name}".')
                answers.append(scene.location.name)
            print('If you want to go somewhere else type "go to <name of location>".')
            print('To just go somewhere type "go to somewhere".')
            print('. To see all locations you could go to type "go to where?".')
            answers.append('go to where?')
            answers.append('go to somewhere')
            for i in adventure.major_locations:
                if i.active and i.name != scene.location.name:
                    answers.append(f'go to {i.name}')
            answered = False
            while not answered:
                answer = check_answers(answers)
                if answer == "go to where?":
                    print('These are all places you could go to:')
                    for i in adventure.major_locations:
                        if scene.name != i.name:
                            print(i.name)
                    for i in adventure.setting.locations:
                        if scene.name != i.name:
                            print(i.name)
                else:
                    answered = True
            if scene.type == 'fight':
                for i in scene.npcs:
                    if answer == i.name:
                        if random.random() > 0.5:
                            print(f'you fight and lose. {i.name} totally beats you up.')
                        else:
                            secretstoget = []
                            for j in scene.secrets:
                                if j.where_to_find == i:
                                    secretstoget.append(j)
                            if len(secretstoget) > 1:
                                print(f'you fight and win. You totally beat up {i.name}. You get the following pieces '
                                      f'of information.')
                            elif len(secretstoget) == 1:
                                print(f'you fight and win. You totally beat up {i.name}. You get the following piece '
                                      f'of information.')
                            for j in secretstoget:
                                print(j.name)
                                j.found = True
                            if len(secretstoget) == 0:
                                print(f'you fight and win. You totally beat up {i.name}.')
                            scene.npcs.remove(i)
                        conditions = [scene.location, scene.npcs]
            elif scene.type == 'social interaction':
                for i in scene.npcs:
                    if answer == i.name:
                        for j in scene.secrets:
                            if j.where_to_find == i:
                                print(f'From your conversation with {i.name} you get the following piece of '
                                      f'information:')
                                print(j.name)
                                j.found = True
                        print(f'After a little bit of talking your conversation with {i.name} ends. {i.name} leaves.')
                        scene.npcs.remove(i)
                        conditions = [scene.location, scene.npcs]
            elif answer == scene.location.name:
                secretstoget = []
                for i in scene.secrets:
                    get = False
                    for j in i.where_to_find:
                        if j.name == answer:
                            get = True
                    if get:
                        secretstoget.append(i)
                if len(secretstoget) == 0:
                    print('You search for a while but you find nothing of interest.')
                elif len(secretstoget) == 1:
                    print('After searching for a while you find the following piece of information:')
                else:
                    print('After searching for a while you find the following pieces of information:')
                for i in secretstoget:
                    print(i.name)
                    i.found = True
                conditions = [scene.location, scene.npcs]
            else:
                if answer == "go to somewhere":
                    print(f'You leave {scene.location.name} and go somewhere else.')
                    conditions = [None, [None]]
                elif answer.startswith("go to"):
                    answer = answer[6:]
                    for i in adventure.major_locations:
                        if answer == i.name:
                            conditions = [i, [None]]
                            break
                    for i in adventure.setting.locations:
                        if answer == i.name:
                            conditions = [i, [None]]
                            break
            for i in scene.secrets:
                if i.name == "won":
                    if i.found:
                        end = True
            input('End of scene. (press enter to continue)')


# The following function needs to be deleted ASAP
def check_answers(answerchoices):
    running = True
    while running:
        answer = input('What do you want to do?').lower()
        possibilities = []
        for i in answerchoices:
            possibilities.append(i.lower())
        for i in range(len(answer)):
            delete = []
            for j in possibilities:
                if j[i] != answer[i]:
                    delete.append(j)
            for j in delete:
                possibilities.remove(j)
            if len(possibilities) == 1:
                print(f'Your answer: {possibilities[0]}')
                return possibilities[0]
            elif len(possibilities) == 0:
                print('Input not understood.')
                break
            elif len(possibilities) == 2:
                if possibilities[0] == possibilities[1]:
                    print(f'Systematical error: Two identically called choices. {possibilities[0]} und '
                          f'{possibilities[1]}')
                    return possibilities[0]

# These two functions need to be deleted ASAP.


def check_active(object_tocheck):
    if object_tocheck.conditions is None:
        object_tocheck.active = True
    else:
        if isinstance(object_tocheck.conditions[0], list):
            for i in object_tocheck.conditions[0]:
                if not i.found:
                    object_tocheck.active = False
            if isinstance(object_tocheck.conditions[1], list):
                for i in object_tocheck.conditions[1]:
                    if i.found:
                        object_tocheck.active = False
        else:
            for i in object_tocheck.conditions:
                if not i.found:
                    object_tocheck.active = False

        return object_tocheck.active


class NPC:
    def __init__(self, name, hostile=False, conditions=None):
        self.name = name
        self.hostile = hostile
        self.conditions = conditions
        self.active = None
        check_active(self)


class LOCATION:
    def __init__(self, name, conditions=None):
        self.name = name
        self.active = None
        self.conditions = conditions
        check_active(self)


class SECRET:
    def __init__(self, name, where_to_find, relevance=1, positiv=True,
                 found=False, conditions=None):  # relevance is small for minor secrets.
        self.name = name
        self.where_to_find = where_to_find  # list of NPCs and or locations.
        self.relevance = relevance
        self.positiv = positiv
        if self.positiv:
            self.effect = relevance
        else:
            self.effect = -1 * relevance
        self.found = found
        self.conditions = conditions
        check_active(self)


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
            if i.positiv:
                self.hope = self.hope + i.relevance
            else:
                self.hope = self.hope + i.relevance * (-1)
        type_to_number = {'fight': 1, 'social interaction': 0, 'exploration': -1}
        self.action = type_to_number[self.type]

    def evaluate(self, idealaction, idealdifficulty, idealhope, adventure):
        relevance_sum = adventure.actionrelevance + adventure.difficultyrelevance + adventure.hoperelevance
        relevance_sum = relevance_sum / 3
        actionrelevance = adventure.actionrelevance / relevance_sum
        difficultyrelevance = adventure.difficultyrelevance / relevance_sum
        hoperelevance = adventure.hoperelevance / relevance_sum
        x = abs(self.action - idealaction) * actionrelevance
        y = abs(self.difficulty - idealdifficulty) * difficultyrelevance
        z = pow(abs(self.hope - idealhope), 0.5) * pow(0.5, 0.5) * hoperelevance  # sqrt to get propper dimensions
        return pow(math.exp((-1) * (x + y + z)), 2)

    def __eq__(self, other):
        if not isinstance(other, SCENE):
            return NotImplemented
        return self.location == other.location and self.npcs == other.npcs and self.secrets == other.secrets

    def __hash__(self):
        return hash((self.location, self.npcs, self.secrets))
        # makes scenes hashable (they work in dicts and sets)


class TRIGGER:
    def __init__(self):
        pass


class ACTION:
    def __init__(self):
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


def get_next_scene(adventure, all_former_scenes, conditions):
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


# Hier folgen kleinere, unwichtige Funktionen:


def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


# from https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
# This is not optimized but it works.

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


def get_setting_by_name(name):
    global settings
    if name == 'classic':
        setting = SETTING('classic')
    else:
        setting = settings[name]
    return setting


main()

