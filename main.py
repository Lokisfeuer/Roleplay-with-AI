# Future plans with AI:
# A setting generator.
# an intelligent adventure writer.
# Every Scene Type intelligent interpreter
# Something that finds out if secrets have been told.


import openai
import random
import jsonlines
import adventure_structure

# openai.api_key = os.getenv('OPENAI_API_KEY')
# model = 'ada:ft-personal-2022-11-27-20-21-30'
openai.api_key = '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'
analyse = True
type_list = [
    'info question', 'action other', 'action speech', 'action change room', 'action start a fight',
    'action end a fight', 'action conversation', 'action end a conversation', 'action ability acrobatics',
    'action ability appraise', 'action ability bluff', 'action ability climb', 'action ability craft',
    'action ability diplomacy', 'action ability disable device', 'action ability disguise',
    'action ability escape artist', 'action ability fly', 'action ability handle animal',
    'action ability heal', 'action ability intimidate', 'action ability knowledge (arcana)',
    'action ability knowledge (dungeoneering)', 'action ability knowledge (engineering)',
    'action ability knowledge (geography)', 'action ability knowledge (history)',
    'action ability knowledge (local)', 'action ability knowledge (nature)',
    'action ability knowledge (nobility)', 'action ability knowledge (planes)',
    'action ability knowledge (religion)', 'action ability linguistics', 'action ability perception',
    'action ability perform', 'action ability profession', 'action ability ride',
    'action ability sense motive', 'action ability sleight of hand', 'action ability spellcraft',
    'action ability stealth', 'action ability survival', 'action ability swim',
    'action ability use magic device'
]
all_types = {}
for i_type in type_list:
    text = 'a.' + i_type.replace(' ', '_').replace('(', '').replace(')', '')
    all_types.update({i_type: text})


# old fine tuned model = 'ada:ft-personal-2022-11-27-17-16-21'


def main():
    # should get type_list from sample.jsonl

    # print('1st Test: An ever-changing test dialogue:')
    # prompt = 'The following is a dialogue between a pair of star crossed lovers.'
    # response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=1, max_tokens=100)
    # response = response['choices'][0]['text']
    # print(response)
    # print('End of first test.')
    print('Test: classification of input.')
    response = input('')
    response = classify(response)
    print(response)
    print('End of test.')
    play(adventure_structure.play_family_adventure())


def play(adventure, conditions=None):
    if conditions is None:
        conditions = [None, [None]]
    former_scenes = []
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
        former_scenes.append(scene)
        print(scene.location.describe(scene.npcs))
        object_of_interest = scene.location
        running_scene = True
        while running_scene:
            a = input('<please enter:>')
            sort = classify(a)
            a = USERINPUT(a)
            result = all_types[sort](object_of_interest=object_of_interest, scene=scene, adventure=adventure)
            object_of_interest = result['object_of_interest']
            running_scene = result['running_scene']
            conditions = result['conditions']
        for i in scene.secrets:
            if i.name == "won":
                if i.found:
                    running_adventure = False
        input('End of scene. (Press enter to continue)')


# The following function is awful. Like absolutely terrible, and it doesn't even work properly.
def play2(adventure, conditions=None):
    if conditions is None:
        conditions = [None, [None]]
    former_scenes = []
    running_a = True
    while running_a:
        scene = adventure_structure.get_next_scene(adventure=adventure, all_former_scenes=former_scenes,
                                                   conditions=conditions)
        if analyse:
            print(scene.type)
            print('location: ' + scene.location.name)
            print('amount of npcs: ' + str(len(scene.npcs)))
            for j in scene.npcs:
                print('NPC: ' + j.name)
            print('amount of secrets: ' + str(len(scene.secrets)))
            for j in scene.secrets:
                print('Secret: ' + j.name)
        former_scenes.append(scene)
        print(scene.location.describe(scene.npcs))
        object_of_interest = scene.location
        running_b = True
        while running_b:
            a = input('')  # single sentence input!
            sort = classify(a)
            if sort[0] == ' Question.':
                if isinstance(object_of_interest, adventure_structure.LOCATION):
                    print(object_of_interest.describe(a))
                elif isinstance(object_of_interest, adventure_structure.NPC):
                    print(object_of_interest.talk(a))
            elif sort[0] == ' Speech.':
                if isinstance(object_of_interest, adventure_structure.NPC):
                    print(object_of_interest.talk(a))
                elif len(scene.npcs) > 0:
                    cha = who(a, scene)
                    if isinstance(cha, adventure_structure.NPC):
                        object_of_interest = cha
                    else:
                        object_of_interest = random.choice(scene.npcs)
                    print(object_of_interest.talk(a))
                else:
                    print('You say these words, but there is no one here to hear you.')
            elif sort[1] == ' Change the room':
                loc = where(sort[2], adventure)
                if isinstance(loc, str):
                    conditions = [None, [None]]
                else:
                    conditions = [loc, [None]]
                running_b = False
            elif sort[1] == ' Start a fight':  # with whom?
                cha = who(sort[2], scene)
                if isinstance(cha, adventure_structure.NPC):
                    object_of_interest = cha
                if isinstance(object_of_interest, adventure_structure.NPC):
                    print(object_of_interest.fight(a))
                else:
                    print('Please repeat your sentence but specify who you intend to fight.')
            elif sort[1] == ' Start a conversation':
                cha = who(sort[2], scene)
                if isinstance(cha, adventure_structure.NPC):
                    object_of_interest = cha
                if isinstance(object_of_interest, adventure_structure.NPC):
                    print(object_of_interest.talk(a))
                else:
                    print('Please repeat your sentence but specify who you intend to start a conversation with.')
            elif sort[1] == ' End a conversation':
                object_of_interest = scene.location
            elif sort[1] == ' Something else.':
                object_of_interest = scene.location
                print(object_of_interest.describe(a))
            else:
                print('Sorry, I don\'t know what you mean by that.')
        for i in scene.secrets:
            if i.name == "won":
                if i.found:
                    running_a = False
        input('End of scene. (Press enter to continue)')


def classify(a):
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
        elif yn[0] == 'n':
            for i in range(5):
                print(all_types.keys())
                response = input(f'Please copy paste the correct type.')
                if response in all_types.keys():
                    document = 'inputs_correct2.jsonl'
                    response = ' ' + response
                    break
            if document == '':
                document = 'inputs_incorrect.json'
        else:
            document = 'inputs_unknown.jsonl'
    else:
        document = 'inputs_unknown'
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
class USERINPUT:
    def __init__(self, a):
        self.a = a

    def write(self):
        global all_types
        for i in all_types.keys():
            print(f'def {all_types[i][2:]}(self, **kwargs):\n\tprint(\'The ability <{i}> is not implemented '
                  f'yet.\')\n\treturn kwargs\n\n')

    def info_question(self, **kwargs):
        print('The ability <info question> is not implemented yet.')
        return kwargs

    def action_other(self, **kwargs):
        print('The ability <action other> is not implemented yet.')
        return kwargs

    def action_speech(self, **kwargs):
        print('The ability <action speech> is not implemented yet.')
        return kwargs

    def action_change_room(self, **kwargs):
        print('The ability <action change room> is not implemented yet.')
        return kwargs

    def action_start_a_fight(self, **kwargs):
        print('The ability <action start a fight> is not implemented yet.')
        return kwargs

    def action_end_a_fight(self, **kwargs):
        print('The ability <action end a fight> is not implemented yet.')
        return kwargs

    def action_conversation(self, **kwargs):
        print('The ability <action conversation> is not implemented yet.')
        return kwargs

    def action_end_a_conversation(self, **kwargs):
        print('The ability <action end a conversation> is not implemented yet.')
        return kwargs

    def action_ability_acrobatics(self, **kwargs):
        print('The ability <action ability acrobatics> is not implemented yet.')
        return kwargs

    def action_ability_appraise(self, **kwargs):
        print('The ability <action ability appraise> is not implemented yet.')
        return kwargs

    def action_ability_bluff(self, **kwargs):
        print('The ability <action ability bluff> is not implemented yet.')
        return kwargs

    def action_ability_climb(self, **kwargs):
        print('The ability <action ability climb> is not implemented yet.')
        return kwargs

    def action_ability_craft(self, **kwargs):
        print('The ability <action ability craft> is not implemented yet.')
        return kwargs

    def action_ability_diplomacy(self, **kwargs):
        print('The ability <action ability diplomacy> is not implemented yet.')
        return kwargs

    def action_ability_disable_device(self, **kwargs):
        print('The ability <action ability disable device> is not implemented yet.')
        return kwargs

    def action_ability_disguise(self, **kwargs):
        print('The ability <action ability disguise> is not implemented yet.')
        return kwargs

    def action_ability_escape_artist(self, **kwargs):
        print('The ability <action ability escape artist> is not implemented yet.')
        return kwargs

    def action_ability_fly(self, **kwargs):
        print('The ability <action ability fly> is not implemented yet.')
        return kwargs

    def action_ability_handle_animal(self, **kwargs):
        print('The ability <action ability handle animal> is not implemented yet.')
        return kwargs

    def action_ability_heal(self, **kwargs):
        print('The ability <action ability heal> is not implemented yet.')
        return kwargs

    def action_ability_intimidate(self, **kwargs):
        print('The ability <action ability intimidate> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_arcana(self, **kwargs):
        print('The ability <action ability knowledge (arcana)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_dungeoneering(self, **kwargs):
        print('The ability <action ability knowledge (dungeoneering)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_engineering(self, **kwargs):
        print('The ability <action ability knowledge (engineering)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_geography(self, **kwargs):
        print('The ability <action ability knowledge (geography)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_history(self, **kwargs):
        print('The ability <action ability knowledge (history)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_local(self, **kwargs):
        print('The ability <action ability knowledge (local)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_nature(self, **kwargs):
        print('The ability <action ability knowledge (nature)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_nobility(self, **kwargs):
        print('The ability <action ability knowledge (nobility)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_planes(self, **kwargs):
        print('The ability <action ability knowledge (planes)> is not implemented yet.')
        return kwargs

    def action_ability_knowledge_religion(self, **kwargs):
        print('The ability <action ability knowledge (religion)> is not implemented yet.')
        return kwargs

    def action_ability_linguistics(self, **kwargs):
        print('The ability <action ability linguistics> is not implemented yet.')
        return kwargs

    def action_ability_perception(self, **kwargs):
        print('The ability <action ability perception> is not implemented yet.')
        return kwargs

    def action_ability_perform(self, **kwargs):
        print('The ability <action ability perform> is not implemented yet.')
        return kwargs

    def action_ability_profession(self, **kwargs):
        print('The ability <action ability profession> is not implemented yet.')
        return kwargs

    def action_ability_ride(self, **kwargs):
        print('The ability <action ability ride> is not implemented yet.')
        return kwargs

    def action_ability_sense_motive(self, **kwargs):
        print('The ability <action ability sense motive> is not implemented yet.')
        return kwargs

    def action_ability_sleight_of_hand(self, **kwargs):
        print('The ability <action ability sleight of hand> is not implemented yet.')
        return kwargs

    def action_ability_spellcraft(self, **kwargs):
        print('The ability <action ability spellcraft> is not implemented yet.')
        return kwargs

    def action_ability_stealth(self, **kwargs):
        print('The ability <action ability stealth> is not implemented yet.')
        return kwargs

    def action_ability_survival(self, **kwargs):
        print('The ability <action ability survival> is not implemented yet.')
        return kwargs

    def action_ability_swim(self, **kwargs):
        print('The ability <action ability swim> is not implemented yet.')
        return kwargs

    def action_ability_use_magic_device(self, **kwargs):
        print('The ability <action ability use magic device> is not implemented yet.')
        return kwargs


if __name__ == '__main__':
    main()
