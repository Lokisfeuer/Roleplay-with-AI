import adventure_structure as adv_str
import json
import jsonpickle


def kilo():
	kalpha = adv_str.NPC(name='qalpha', hostile=False, conditions=[], description='q_as_k')
	kbravo = adv_str.NPC(name='qbravo', hostile=False, conditions=[], description='q_as_k')
	kaugsburg = adv_str.LOCATION(name='quaksburg', conditions=[], description='q_as_k')

	npcs = [kalpha, kbravo]
	locations = [kaugsburg]
	secrets = []

	name = 'Kilo'
	starting_conditions = [None, [None]]

	adventure = adv_str.ADVENTURE(name=name, major_npcs=npcs, major_locations=locations, major_secrets=secrets, trigger_dict={})
	with open('../data.json', 'r') as f:
		data = json.load(f)
	data['adventures'].update({name: {
		'adventure': jsonpickle.encode(adventure, keys=True),
		'conditions': jsonpickle.encode(starting_conditions, keys=True)
	}})
	with open('../data.json', 'w') as f:
		json.dump(data, f, indent=4)
	return adventure, starting_conditions

