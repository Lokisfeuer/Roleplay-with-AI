# classes in classifier
#   question
#   knowledge
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

openai.api_key = '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'


def classify(a):
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
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=12)
    response = response['choices'][0]['text']
    if response == ' Action.':
        # Here could abilities get added.
        prompt = f'''The following classifies what an action does. Actions either start a conversation, end a
conversation, change the room, start a fight or do something else.

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

Action: I stop talking to Mary.
Result: End a conversation.

Action: I go there.
Result: Change the room.

Action: I go to the table.
Result: Something else.

Action: {a}
Result:'''
        action_type = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=12)
        action_type = action_type['choices'][0]['text']
        return [response, action_type, a]
    else:
        return [response]