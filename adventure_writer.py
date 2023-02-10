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

