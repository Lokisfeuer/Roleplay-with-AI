import openai
import math
import random

openai.api_key = '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'


def main():
    global settings
    settings = {
        'test': SETTING('test', npcs=[NPC('Una'), NPC('Jerry')], locations=[LOCATION('School'), LOCATION('house')])
    }
    prompt = '''The following classifies for each sentence whether it is an action, a question or speech.

    Sentence: Hi, how are you?.
    Type: Speech.

    Sentence: I go into the room.
    Type: Action.

    Sentence: What do I see?
    Type: Question.

    Sentence: I sit down at the table.
    Type: Action.

    Sentence: I think so too.
    Type: Speech.

    Sentence: Probably.
    Type: Speech.

    Sentence: How does the room look?
    Type: Question.'''
    print(prompt)

    pass


def useai():
    # A setting generator.
    # an intelligent adventure writer.
    # Every Scene Type intelligent interpreter
    # a classifier that will differ between in-scene texts and out-of-scene commands.
    # Something that finds out if secret have been told.
    response = openai.Completion.create(model="text-davinci-002",
                                        prompt="Say this is a test",
                                        temperature=0,
                                        max_tokens=6)
    response = response['choices'][0]['text']
    print(response)


# The following function is awful.
def play(adventure, conditions=None, analyse=True):
    if conditions is None:
        conditions = [None, [None]]
    former_scenes = []
    end = False
    while not end:
        scene = get_next_scene(adventure=adventure, all_former_scenes=former_scenes, conditions=conditions)
        if analyse:
            print(type(scene))
            print('location: ' + scene.location.name)
            print('amount of npcs: ' + str(len(scene.npcs)))
            for j in scene.npcs:
                print('NPC: ' + j.name)
            print('amount of secrets: ' + str(len(scene.secrets)))
            for j in scene.secrets:
                print('Secret: ' + j.name)
        former_scenes.append(scene)
        # describe room
        # repeat:
            # input
            # classify input
            # 1. (Question and Speech) Answer and go
            # 2. (Action) in-scene-command
            # execute directly (or even keep in talk)
            # 3. change-scene-commands
            # execute and break loop
        conditions = [None, [None]]  # should depend on last scene.
        for i in scene.secrets:
            if i.name == "won":
                if i.found:
                    end = True
        input('End of scene. (press enter to continue)')


def classify(input):
    # Should this differ between in-scene actions and out-of-scene actions?
    prompt = f'''The following classifies for each sentence whether it is an action, a question or speech. 
        
Sentence: Hi, how are you?.
Type: Speech.

Sentence: I go into the room.
Type: Action.

Sentence: What do I see?
Type: Question.

Sentence: I sit down at the table.
Type: Action.

Sentence: I think so too.
Type: Speech.

Sentence: Probably.
Type: Speech.

Sentence: How does the room look?
Type: Question.

Sentence: {input}
Type:'''
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=12)
    response = response['choices'][0]['text']
    print(f'Type of {input} is {response}')
    if response == 'action':
        # Here could abilities get added.
        prompt = f'''The following classifies what an action does. Actions either start a conversation, change the 
room, start a fight or do something else.

Action: I sit down at the table.
Result: Something else.

Action: I leave the room.
Result: Change the room.

Action: I hit him.
Result: Start a fight.

Action: I attack John.
Result: Start a fight.

Action: I talk to John.
Result: Start a conversation.

Action: I go there.
Result: Change the room.

Action: I go to the table.
Result: Something else.

Action: {input}
Result:'''
        action_type = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=12)
        action_type = action_type['choices'][0]['text']
        return [response, action_type]
    else:
        return [response]

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
            print('ERROR: Conditions are wrongly listed! (To prevent an error conditions[1] = [conditions[1]]')
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


if __name__ == '__main__':
    main()
