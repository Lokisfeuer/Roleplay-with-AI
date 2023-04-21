# Character structure:
import json
import openai
import jsonpickle
import os

openai.api_key = os.getenv('OPENAI_API_KEY')


# A character has 8 Attributes (DSA) and unlimited amounts of skills.

# 8 Attributes with percentages adding to a fix sum of about 500 with no skill over 80 and no skill under 20
# bravery
# intuition
# etc.

# Every Skill depends on two attributes, one major and one minor. To successfully use a skill the probability is the
# percentage of the major attribute squared times the percentage of the minor attribute + the amount of skill points
# in this skill.

# Skills fall in one of three categories: social (talk & speech), physical (action (& fight?)), knowledge (info)

# Every skill can have up to 40ish skill points. (Maybe in levels like: beginner = 10 SP; intermediate = 20 SP;
# expert = 30 SP; Master = 40 and maybe grand master = 45) (You can only level one skill to grand master level per
# character))

# If anyone wants to add skills, feel free just assign them their major and minor attribute as well as category.

# there should be just a handful different skills to not weaken the effect of improving in one.


# MESSAGES NEEDS TO BE DELETED WHEN A PC IS DONE!!!

def main_create(author, input):
    with open('data.json', 'r') as f:
        data = json.load(f)
    if input.startswith('/exit'):
        # set running None
        data['players'][author]['current_PC'] = None
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return False
    if 'current_PC' in data['players'][author].keys():
        if data['players'][author]['current_PC'] is not None:
            answer = create_pc(author, input)
            if isinstance(answer, bool):
                with open('data.json', 'r') as f:
                    data = json.load(f)
                data['players'][author]['current_PC'] = None
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
            return answer
    messages = [
        {"role": "system",
         "content": "You are helping to create a character for tabletop rpg. To create a character the user needs to "
                    "give every attribute points between minimal 20 and maximal 80 points. The user cannot have less "
                    "than 20 or more than 80 points on any attribute. The user can overall distribute 500 points over "
                    "the attributes.\nThe attributes are courage, cleverness, intuition, charisma, dexterity, agility, "
                    "constitution and strength."},
        {"role": "user", "content": "Hello, I would like to create a character."}]
    data['players'][author].update({'current_PC': input})
    data['players'][author].update({'messages_PC': messages})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return f'Setup PC {input}. You are being directed to the PC generator assistant. When you are done, enter ' \
           f'"/done" to continue'


def create_pc(author, input):
    with open('data.json', 'r') as f:
        data = json.load(f)
    name = data['players'][author]['current_PC']
    messages = data['players'][author]['messages_PC']
    if input != '/done':
        messages.append({'role': 'user', 'content': input})
        answer = openai.ChatCompletion.create(model='gpt-3.5-turbo', temperature=0.7, max_tokens=256, messages=messages)
        messages.append(answer['choices'][0]['message'])
        with open('data.json', 'r') as f:
            data = json.load(f)
        data['players'][author]['messages_PC'] = messages
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        answer = answer['choices'][0]['message']['content']
    else:
        prompt = ''
        for i in messages:
            prompt = prompt + f'{i["role"]}: {i["content"]}\n\n'
        prompt = prompt + 'courage: $$\ncleverness: $$\nintuition: $$\ncharisma: $$\ndexterity: $$\nagility: ' \
                          '$$\nconstitution: $$\nstrength: $$'
        instruction = 'replace the "$$" of the attributes with the correct number based on the chat history above.'
        answer = openai.Edit.create(
            model='text-davinci-edit-001', input=prompt, instruction=instruction, temperature=0)
        answer = answer['choices'][0]['text']
        attributes = {}
        for i in answer.split('\n')[::-1]:
            if not i == '':
                if i[-1].isdigit():
                    try:
                        attribute = i[0: i.find(':')]
                        attributes.update({attribute: int(i[-2:])})
                    except ValueError:
                        raise 'ReplacementError'
            if len(list(attributes.keys())) == 8:
                break
        if len(list(attributes.keys())) == 8:
            range_error = False
            for i in attributes.values():
                if not 19 < i < 81:
                    range_error = True
                    break
            if range_error:
                answer = 'Every attribute needs to have between 20 and 80 points.'
            elif sum(list(attributes.values())) == 500:
                with open('data.json', 'r') as f:
                    data = json.load(f)
                attributes.update({'skills': {}})
                if 'characters' not in data['players'][author]:
                    data['players'][author].update({'characters': {}})
                data['players'][author]['characters'].update({name: attributes})
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
                answer = True
            else:
                answer = f'The attributes don\'t add up to 500 points.'  # add to messages.
            if isinstance(answer, str):
                with open('data.json', 'r') as f:
                    data = json.load(f)
                messages.append({"role": "assistant", "content": answer})
                data['players'][author]['messages_PC'] = messages
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
        else:
            answer = f'Error creating PC {name}. Try again "/done" or leave with "/exit" or summarize your ' \
                     f'character again.'
    return answer


def level_up(author, input):
    with open('data.json', 'r') as f:
        data = json.load(f)
    if input.startswith('/exit'):
        data['players'][author]['current_PC'] = None  # if new skill in there.
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return False
    if 'current_PC' in data['players'][author].keys():
        if data['players'][author]['current_PC'] is not None:
            pc = data['players'][author]['current_PC']
            if input in data['skills'].keys():
                if input in data['players'][author]['characters'][pc]['skills'].keys():
                    new_value = data['players'][author]['characters'][pc]['skills'][input] + 1
                    if new_value > 6:
                        return 'You cannot skill this ability any higher.'
                    with open('data.json', 'r') as f:
                        data = json.load(f)
                    data['players'][author]['characters'][pc]['skills'][input] = new_value
                    with open('data.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    return True
                else:
                    with open('data.json', 'r') as f:
                        data = json.load(f)
                    data['players'][author]['characters'][pc]['skills'].update({input: 1})
                    with open('data.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    return True
            else:
                skills = ''
                for i in data['skills'].keys():
                    skills += f'\t{i}\n'
                return f'Please enter the skill you want to improve or learn. Here a list of all skills:\n{skills}' \
                       f'If you want to improve a different skill, you can create skills yourself in the main menu.'
        else:
            if input in data['players'][author]['characters'].keys():
                with open('data.json', 'r') as f:
                    data = json.load(f)
                data['players'][author]['current_PC'] = input
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
                return f'You are levelling up your character "{input}".'
            else:
                return 'Which of your characters would you like to level up?'
    else:
        return 'Please create a character before levelling it up.'


def add_skill(author, input):
    with open('data.json', 'r') as f:
        data = json.load(f)
    if input.startswith('/exit'):
        # set running None
        data['players'][author]['new_skill'] = None  # if new skill in there.
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        # delete unfinished skills.
        return False
    attributes = ["strength", "constitution", "agility", "dexterity", "charisma", "intuition", "cleverness", "courage"]
    if not 'new_skill' in data['players'][author].keys():
        data['players'][author].update({'new_skill': None})
    if data['players'][author]['new_skill'] is None:
        data['skills'].update({input: {'attributes': []}})
        data['players'][author].update({'new_skill': input})
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        answer = f'Setup skill "{input}".\n'
        answer = answer + f'If the name is correct, please enter the digit of the attribute your skill is most ' \
                          f'dependent on.\n'
        for i in attributes:
            answer = answer + f'\t({attributes.index(i)+1}) {i[0].upper()}{i[1:]}\n'
        return answer + 'After that enter the digit of the attribute your skill is second most dependent on.'
    elif input[0].isdigit():
        if len(input) == 1:
            if not len(data['skills'][data['players'][author]['new_skill']]['attributes']) == 2:
                input = attributes[int(input)-1]
                data['skills'][data['players'][author]['new_skill']]['attributes'].append(input)
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
                answer = f'Added attribute "{input}" as main attribute to skill "{data["players"][author]["new_skill"]}".'
                if len(data['skills'][data['players'][author]['new_skill']]['attributes']) == 2:
                    data['players'][author]['new_skill'] = None
                    with open('data.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    return f'Added attribute "{input}" as secondary attribute to skill "{data["players"][author]["new_skill"]}".\nNow please enter the number of the type of skill this is.\n\t(1) fight\n\t(2) knowledge\n\t(3) social\n\t(4) action'
                return answer
            else:
                l = ['fight', 'knowledge', 'social', 'action']
                data['skills'][data['players'][author]['new_skill']].update({'type': l[int(input)-1]})
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
        else:
            return 'Answer to long.'
