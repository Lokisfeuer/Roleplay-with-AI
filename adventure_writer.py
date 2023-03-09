import json

# check names
# Description (and names) should be multiple words long.
# command to show all objects
# if Error not in keywords, check whether its an object to navigate


def talk_and_write(message, author):
    with open('user_written_adventures/adventures.json', 'r') as f:
        data = json.load(f)
    if author not in data.keys():
        return 'To setup a new adventure, enter "/new name_of_adventure".'
    object_of_interest = data[author]['background']['object_of_interest']
    name_of_adventure = data[author]['background']['name_of_adventure']
    adventure = data[author][name_of_adventure]
    object_type = data[author]['background']['object_type']
    keyword_dict = {'npcs': {'name': '', 'hostile': 'False', 'conditions': [], 'description': ''},
                    'locations': {'name': '', 'conditions': [], 'description': ''},
                    'secrets': {'name': '', 'where_to_find': [], 'relevance': '1', 'positive': 'True',
                                'found': 'False', 'conditions': [], 'description': '', 'clue': 'True'}}
    if object_of_interest in keyword_dict.keys():
        if message == '/done':
            index = list(keyword_dict.keys()).index(object_of_interest)
            if index == 2:
                object_of_interest = 'starting_conditions'
                answer = f'Please enter now the starting conditions.'
            else:
                object_of_interest = list(keyword_dict.keys())[index + 1]
                answer = f'Please enter now all your {object_of_interest}.'
            data[author]['background']['object_of_interest'] = object_of_interest
            with open('user_written_adventures/adventures.json', 'w') as f:
                json.dump(data, f, indent=4)
            return answer
        if message not in data[author][name_of_adventure][object_of_interest].keys():
            data[author][name_of_adventure][object_of_interest].update({message.lower(): keyword_dict[object_of_interest]})
            with open('user_written_adventures/adventures.json', 'w') as f:
                json.dump(data, f, indent=4)
            return f'Received {object_of_interest[:-1]} "{message}"'
        else:
            return f'This {object_of_interest[:-1]} already exists.'
    else:
        if object_of_interest == 'starting_conditions':
            if message in list(adventure['npcs'].keys()) + list(adventure['locations'].keys()):
                if message in adventure['locations'].keys():
                    data[author][name_of_adventure]['starting_conditions'][0] = message
                    answer = f'Set location "{message}" to starting conditions.'
                else:
                    data[author][name_of_adventure]['starting_conditions'][1].append(message)
                    answer = f'Added npc "{message}" to starting conditions.'
            elif message == '/done':
                if data[author][name_of_adventure]['starting_conditions'][1] == []:
                    data[author][name_of_adventure]['starting_conditions'][1].append(None)
                object_of_interest = list(data[author][name_of_adventure]['npcs'].keys())[0]
                data[author]['background']['object_of_interest'] = object_of_interest
                data[author]['background']['object_type'] = 'npcs'
                answer = f'Starting conditions set as location: ' \
                         f'"{adventure["starting_conditions"][0]}" and npcs: "{adventure["starting_conditions"][1]}"'
                answer = f'{answer}\nYou are now at npc "{object_of_interest}". You can set attributes with keywords.'
            else:
                answer = 'This is not a valid condition. Type /done to end.'
            with open('user_written_adventures/adventures.json', 'w') as f:
                json.dump(data, f, indent=4)
            return answer
        if message.split()[0][1:] in keyword_dict[object_type].keys() or not message.startswith('/'):
            full_object = data[author][name_of_adventure][object_type][object_of_interest]
            keyword = message.split()[0]
            if keyword.startswith('/'):
                keyword = keyword[1:]
            elif keyword.endswith(':'):
                keyword = keyword[:-1]
            if keyword not in full_object.keys():
                return 'Error keyword not in keywords.'
            value = message.split()[-1]
            if keyword == 'conditions' or keyword == 'where_to_find':
                data[author][name_of_adventure][object_type][object_of_interest][keyword].append(value)
            else:
                data[author][name_of_adventure][object_type][object_of_interest][keyword] = value
            with open('user_written_adventures/adventures.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            found = False
            for i in ['npcs', 'locations', 'secrets']:
                for j in data[author][name_of_adventure][i].keys():
                    if j == message[1:]:
                        found = True
                        object_of_interest = j
                        object_type = i
                        full_object = data[author][name_of_adventure][object_type][object_of_interest]
                        data[author]['background']['object_of_interest'] = object_of_interest
                        data[author]['background']['object_type'] = object_type
                        with open('user_written_adventures/adventures.json', 'w') as f:
                            json.dump(data, f, indent=4)
                        break
                if found:
                    break
            if not found:
                if message == '/done':
                    missing = check_for_completeness(author, name_of_adventure)
                    if isinstance(missing, bool):
                        write_adventure_from_data(author, name_of_adventure, adventure)
                        return True  # send full document?
                    else:
                        answer = f'/adventure writer/{name_of_adventure}/{object_type}/{object_of_interest}\n\n'
                        for i in missing:
                            answer = f'{answer}{i}\n'
                        answer = f'{answer}\nTherefore adventure could not be written.'
                        return answer
                elif message == '/exit':
                    return False
                return 'Error object not found.'
        print('Reached end of talk_and_write.')
        answer = f'/adventure writer/{name_of_adventure}/{object_type}/{object_of_interest}'
        answer = f'{answer}\n\n'
        for i in full_object.keys():
            answer = f'{answer}{i}: {full_object[i]}\n'
        instruction = 'Please enter'
        answer = f'{answer}\n{instruction}'
        return answer


def check_for_completeness(author, name_of_adventure):
    def list_in_list(list1, list2):
        for element in list1:
            if element not in list2:
                return False
        return True

    with open('user_written_adventures/adventures.json', 'r') as f:
        data = json.load(f)
    missing = []
    adventure = data[author][name_of_adventure]
    mandatory = ['name', 'description']
    all_objects = {}
    all_objects.update(adventure['npcs'])
    all_objects.update(adventure['locations'])
    all_objects.update(adventure['secrets'])
    for i in all_objects.keys():
        for j in all_objects[i].keys():
            if j in mandatory and all_objects[i][j] == '':
                missing.append(f'Object with name "{i}" is missing parameter "{j}".')
    if not missing == []:
        return missing
    validated = []
    for x in all_objects.keys():
        for i in all_objects.keys():
            if i not in validated and list_in_list(all_objects[i]['conditions'], validated):
                if 'where_to_find' in all_objects[i].keys():
                    if list_in_list(all_objects[i]['where_to_find'], validated):
                        validated.append(i)
                        break
                else:
                    validated.append(i)
                    break
    # now validated should be the perfectly ordered list of object-strings
    if not list_in_list(all_objects.keys(), validated):
        answer = ['There is a logical loop in your adventure. Not everything can be fully defined.\n']
        for i in all_objects.keys():
            if i not in validated:
                answer.append(f'The object with name "{i}" has unvalidated conditions or where to find.')
        return answer
    return True


def write_adventure_from_data(author, name_of_adventure, adventure):
    obj_commands = ''
    all_list_commands = ''
    for i in ['npcs', 'locations', 'secrets']:
        list_command = ''
        for j in adventure[i].keys():
            parameters = ''
            for k in adventure[i][j].keys():
                if k == 'name' or k == 'description':
                    parameters = f'{parameters}, {k}=\'{adventure[i][j][k]}\''
                else:
                    parameters = f'{parameters}, {k}={adventure[i][j][k]}'
            parameters = parameters[2:]
            obj_commands = f'{obj_commands}\t{j} = adv_str.{i[:-1].upper()}({parameters})\n'

            list_command = f'{list_command}, {j}'
        list_command = f'{i} = [{list_command[2:]}]'
        all_list_commands = f'{all_list_commands}\t{list_command}\n'
    nam_command = f'\tname = \'{name_of_adventure}\''
    sta_con_command = f'\tstarting_conditions = {adventure["starting_conditions"]}'
    adv_command = \
        '''
\tadventure = adv_str.ADVENTURE(name=name, major_npcs=npcs, major_locations=locations, major_secrets=secrets, trigger_dict={})
\twith open('data.json', 'r') as f:
\t\tdata = json.load(f)
\tdata['adventures'].update({name: {
\t\t'adventure': jsonpickle.encode(adventure, keys=True),
\t\t'conditions': jsonpickle.encode(starting_conditions, keys=True)
\t}})
\twith open('data.json', 'w') as f:
\t\tjson.dump(data, f, indent=4)
\treturn adventure, starting_conditions
'''
    full_function_content = f'{obj_commands}\n{all_list_commands}\n{nam_command}\n{sta_con_command}\n{adv_command}'
    imp_commands = 'import adventure_structure as adv_str\nimport json\nimport jsonpickle'
    full_doc = f'{imp_commands}\n\n\ndef {name_of_adventure.lower().replace(" ","_")}():\n{full_function_content}\n'
    with open(f'user_written_adventures/{author}_{name_of_adventure}.py', 'w') as f:
        f.write(full_doc)


def setup(author, name_of_adventure):
    background = {'object_of_interest': 'npcs', 'name_of_adventure': name_of_adventure, 'object_type': ''}
    content = {'background': background, name_of_adventure: {}}
    adventure_content = ['name', 'starting_conditions', 'npcs', 'locations', 'secrets']
    for i in adventure_content:
        content[name_of_adventure].update({i: {}})
    content[name_of_adventure]['name'] = name_of_adventure
    content[name_of_adventure]['starting_conditions'] = [None, []]
    with open('user_written_adventures/adventures.json', 'r') as f:
        data = json.load(f)
    if author not in data.keys():
        data.update({author: {}})
    if name_of_adventure in data[author].keys():
        data[author].update({'background': background})
        answer = 'Reopened adventure. You can now add objects to the adventure.'
    else:
        data[author].update(content)
        answer = 'Setup new adventure.'
    with open('user_written_adventures/adventures.json', 'w') as f:
        json.dump(data, f, indent=4)
    return answer + '\nPlease enter your npcs one by one. When you are done enter "/done".'


def main(author, message):
    if message.startswith('/new'):
        send = ''
        for i in message.split()[1:]:
            send = send + i
        return setup(author, send)
    else:
        return talk_and_write(message, author)
