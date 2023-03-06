import adventure_structure
import openai
import os
import json


def talk_and_write(message, author):
    with open('adventures.json', 'r') as f:
        data = json.load(f)
    object_of_interest = data[author]['background']['object_of_interest']
    name_of_adventure = data[author]['background']['name_of_adventure']
    object_type = data[author]['background']['object_type']
    keyword_dict = {'npcs': {}, 'locations': {}, 'secrets': {}}  # need to be hardcoded
    if object_of_interest in keyword_dict.keys():
        if message == '/done':
            index = keyword_dict.keys().index(object_of_interest)
            if index == 2:
                object_of_interest = data[author][name_of_adventure]['npcs'].keys()[0]
                data[author]['background']['object_type'] = 'npcs'
                answer = f'You are now at npc "{object_of_interest}".'
            else:
                object_of_interest = keyword_dict.keys()[index+1]
                answer = f'Please enter now all your {object_of_interest}.'
            data[author]['background']['object_of_interest'] = object_of_interest
            with open('adventures.json', 'w') as f:
                json.dump(data, f, indent=4)
            return answer
        if message not in data[author][name_of_adventure][object_of_interest].keys():
            data[author][name_of_adventure][object_of_interest].update({message: keyword_dict[object_of_interest]})
            with open('adventures.json', 'w') as f:
                json.dump(data, f, indent=4)
            return f'Received {object_of_interest[:-1]} "{message}"'
        else:
            return f'This {object_of_interest[:-1]} already exists.'
    else:
        if message.slice(' ')[0][1:] in keyword_dict[object_type].keys() or not message.startswith('/'):
            full_object = data[author][name_of_adventure][object_type][object_of_interest]
            keyword = message.slice(' ')[0]
            if keyword.startswith('/'):
                keyword = keyword[1:]
            elif keyword.endswith(':'):
                keyword = keyword[:-1]
            if keyword not in full_object.keys():
                return 'Error keyword not in keywords.'
            value = message.slice(' ')[-1]
            data[author][name_of_adventure][object_type][object_of_interest][keyword] = value
            with open('adventures.json', 'w') as f:
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
                        data[author][name_of_adventure]['background']['object_of_interest'] = object_of_interest
                        data[author][name_of_adventure]['background']['object_type'] = object_type
                        with open('adventures.json', 'w') as f:
                            json.dump(data, f, indent=4)
                        break
                if found:
                    break
            if not found:
                if message == '/done':
                    missing = check_for_completeness(author, name_of_adventure)
                    if isinstance(bool):
                        write_adventure_from_data(author, name_of_adventure)
                        return 'adventure written successfully.'  # send full document?
                    else:
                        answer = f'/adventure writer/{name_of_adventure}/{object_type}/{object_of_interest}\n\n'
                        for i in missing:
                            answer = f'{answer}{i}\n'
                        answer = f'{answer}\nTherefore adventure could not be written.'
                        return answer
                elif message == '/exit':
                    pass  # /exit needs to be handled
                return 'Error object not found.'
        answer = f'/adventure writer/{name_of_adventure}/{object_type}/{object_of_interest}'
        answer = f'{answer}\n\n'
        for i in full_object.keys():
            answer = f'{answer}{i}: {full_object[i]}\n'
        instruction = 'Please enter'
        answer = f'{answer}\n{instruction}'
        return answer


def check_for_completeness(author, name_of_adventure):
    with open('adventures.json', 'r') as f:
        data = json.load(f)
    missing = []
    adventure = data[author][name_of_adventure]
    for k in ['npcs', 'locations', 'secrets']:
        for i in adventure[k].keys():
            for j in adventure[k][i].keys():
                if adventure[k][i][j] == '':
                    missing.append(f'Object of type "{k}" and name "{i}" is missing "{j}".')
    if missing == []:
        return True
    else:
        return missing


def write_adventure_from_data(author, name_of_adventure):
    with open('adventures.json', 'r') as f:
        data = json.load(f)
    adventure = data[author][name_of_adventure]
    running = True
    while running:
        for i in adventure.keys():
            pass
            # write quite a bit.






















docstring = ''
lines = docstring.split('\n')
for line in lines:
    if line.startswith(' — ge') or line.startswith(
            'Digi') or line == '':
        pass
    elif line.startswith('BOT'):
        print('BOT:')
    elif line.startswith('Lokisg'):
        print('ME:')
    else:
        print(line)


def dc_write_adventure(answer, previous=None):
    if previous is None:
        answer = 'An adventure consists of three things: LOCATIONS, NPCS, and SECRETS.\n' \
                 'Please start with the NPCs first. Just enter the name of a NPC and then enter all information you ' \
                 'are asked about. When you are done you have the option to continue with another NPC or start with ' \
                 'the locations.'
        return answer




def write_adventure():
    object_dict = {'npcs': {}, 'locations': {}, 'secrets': {}, 'trigger': {}}
    print(f'Please enter all your npcs, locations, secrets and trigger. When you are done with one just type "/next"')
    for i in object_dict.keys():
        a = input(f'({i}) <please enter:> ')
        while not a.startswith('/'):
            object_dict[i].update({a: []})
            a = input('<please enter:> ')
        print('now please enter all locations or if you already did that all secrets')
        for i in object_dict['secrets'].keys():
            print(f'Where can the secret "{i}"be found? Enter all locations and npcs. When you are done just type '
                  f'"/next"')
            a = input(f'({i}) <please enter:> ')
            while not a.startswith('/'):
                # ask for closest match in object_dict
                object_dict['secrets'][i].append(a)
                a = input('<please enter:> ')








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

    triggerfunctions = [prolouge, on_the_algebra, boss_fight, at_the_algebra, won, loveletter, money, alcohol, secret_message]

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
    data['adventures'].update({name: {'adventure': jsonpickle.encode(adventure, keys=True),
                                      'conditions': jsonpickle.encode(starting_conditions, keys=True)}})
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return adventure, starting_conditions