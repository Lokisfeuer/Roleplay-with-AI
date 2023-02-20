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
