import json
import random


# social, fight, action, knowledge

def main(author, input, skill, game):
    try:
        answer = eval(skill + '(author, input, skill, game)')
    except NameError:
        answer = None
    if isinstance(answer, str):
        return answer
    elif answer is None:
        with open('data.json', 'r') as f:
            data = json.load(f)
        pc = data['players'][author]['characters'][data['players'][author]['current_PC']]
        atts = data['skills'][skill]['attributes']
        chance = pc['skills'][skill] + ((pc['attributes'][atts[0]] ** 2) * pc['attributes'][atts[1]] / 1000000)
        poss = []
        if random.random() < chance:
            if data['skills'][skill]['type'] in ['social', 'knowledge']:
                for i in game.scene.secrets:
                    if game.object_of_interest in i.where_to_find:
                        if data['skills'][skill]['type'] == 'social' or i.knowledge:
                            poss.append(i)
                secret = random.choice(poss)
            elif data['skills'][skill]['type'] == 'action':
                return None
        else:
            return 'Your attempt was not successful'
    else:
        return 'skill trigger did not give back string nor None.'


def fight(author, input, skill, game):
    with open('data.json', 'r') as f:
        data = json.load(f)
    pc = data['players'][author]['characters'][data['players'][author]['current_PC']]
    atts = data['skills'][skill]['attributes']
    chance = pc['skills'][skill] + ((pc['attributes'][atts[0]] ** 2) * pc['attributes'][atts[1]] / 1000000)
    if random.random() < chance:
        return 'Your opponent loses life. (Fighting still bores me)'
        pass  # success
    else:
        return 'Your opponent beats you up and you lose life. (Fighting still bores me)'


def social(*args):
    pass


def action(*args):
    pass


def knowledge(*args):
    pass
