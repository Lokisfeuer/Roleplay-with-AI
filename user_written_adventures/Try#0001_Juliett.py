import adventure_structure as adv_str
import json
import jsonpickle


def juliett():
	Jalpha = adv_str.NPC(name='Jalpha', hostile=False, conditions=['Jsecret1'], description='Persona')
	Jbeta = adv_str.NPC(name='Jbeta', hostile=False, conditions=[], description='Personb')
	Jaugsburg = adv_str.LOCATION(name='Jaugsburg', conditions=[], description='town.')
	Jsecret1 = adv_str.SECRET(name='Jalpha_found', where_to_find=['Jbeta'], relevance=1, positive=True, found=False, conditions=[], description='Persona_found', clue=True)

	npcs = [Jalpha, Jbeta]
	locations = [Jaugsburg]
	secrets = [Jsecret1]

	name = 'Juliett'
	starting_conditions = [None, [None]]

	adventure = adv_str.ADVENTURE(name=name, major_npcs=npcs, major_locations=locations, major_secrets=secrets, trigger_dict={})
	with open('data.json', 'r') as f:
		data = json.load(f)
	data['adventures'].update({name: {
		'adventure': jsonpickle.encode(adventure, keys=True),
		'conditions': jsonpickle.encode(starting_conditions, keys=True)
	}})
	with open('data.json', 'w') as f:
		json.dump(data, f, indent=4)
	return adventure, starting_conditions

