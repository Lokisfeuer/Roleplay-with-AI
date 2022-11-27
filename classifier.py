# classes in classifier
#   question
#       knowledge
#   action
#       speech
#       change room
#           in big scale
#       start a fight
#       end a fight
#       conversation
#       end a conversation
#       all D&D abilities
#       rest
#       take / leave / use ITEM

import openai
import jsonlines


# openai.api_key = os.getenv('OPENAI_API_KEY')
# openai.api_key = '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'

def write_file():
    abilities_pathfinder = [
        'Acrobatics',
        'Appraise',
        'Bluff',
        'Climb',
        'Craft',
        'Diplomacy',
        'Disable Device',
        'Disguise',
        'Escape Artist',
        'Fly',
        'Handle Animal',
        'Heal',
        'Intimidate',
        'Knowledge (arcana)',
        'Knowledge (dungeoneering)',
        'Knowledge (engineering)',
        'Knowledge (geography)',
        'Knowledge (history)',
        'Knowledge (local)',
        'Knowledge (nature)',
        'Knowledge (nobility)',
        'Knowledge (planes)',
        'Knowledge (religion)',
        'Linguistics',
        'Perception',
        'Perform',
        'Profession',
        'Ride',
        'Sense Motive',
        'Sleight of Hand',
        'Spellcraft',
        'Stealth',
        'Survival',
        'Swim',
        'Use Magic Device']
    train = []
    data = {
        'Info question': ['What do I see?', 'What do I hear?', 'How does it look?', 'Do I feel anything?'],
        'action speech': ['How are you?', 'I think so too.', 'I think so.', 'What have you been doing?', 'I like John.'],
        'action change room': ['I leave the room.', 'I\'m going to the store.', 'I go to the kitchen.', 'I go to the tower'],
        'action start a fight': ['I start a fight.', 'I attack him.', 'I hit Bettina.', 'I slap Albert in the face.'],
        'action end a fight': ['I end a fight.', 'I stop fighting.', 'I give up.', 'I do not attack him.', 'I do not attack her.'],
        'action conversation': ['I have a conversation with someone.', 'I talk to Christopher.', 'I greet Daniela warmly.'],
        'action end a conversation': ['I end a conversation.', 'I stop talking.', 'I don\'t answer.'],
    }
    for i in abilities_pathfinder:
        data[f'action ability {i.lower()}'] = [f'I use {i.lower()}.', f'I try using my ability {i.lower()}.', f'I {i.lower()}.']
    for i in data.keys():
        for j in data[i]:
            dict = {'prompt': j+'\n\n###\n\n', 'completion': ' '+i+'###'}
            train.append(dict)
    with jsonlines.open("sample.jsonl", "w") as outfile:
        outfile.write_all(train)

# ada:ft-personal-2022-11-27-17-16-21
#write_file()

def classify(a):
    prompt = f'{a}\n\n###\n\n'
    response = openai.Completion.create(model="ada:ft-personal-2022-11-27-17-16-21", prompt=prompt, temperature=0, max_tokens=12, stop="###")
    return response


def old_classify(a):
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

Sentence: {a}
Type:'''
    response = openai.Completion.create(model="ada:ft-personal-2022-11-27-17-16-21", prompt=prompt, temperature=0, max_tokens=12)
    response = response['choices'][0]['text']
    if response == ' Action.':
        # Here could abilities get added.
        prompt = f'''The following classifies what an action does. Actions either start a conversation, end a
conversation, change the room, start a fight or do something else.


Action: {a}
Result:'''
        action_type = openai.Completion.create(model="ada:ft-personal-2022-11-27-17-16-21", prompt=prompt, temperature=0, max_tokens=12)
        action_type = action_type['choices'][0]['text']
        return [response, action_type, a]
    else:
        return [response]