import adventure_structure as adv_str
import json
import jsonpickle


def myadventure():
	malpha = adv_str.NPC(name='Cha1', hostile=False, conditions=[], description='This is Cha 1')
	mbeta = adv_str.NPC(name='Cha 2', hostile=False, conditions=[], description='This is CHa 2')
	ghjkl = adv_str.LOCATION(name='Tavernia', conditions=[], description='gnaul')

	npcs = [malpha, mbeta]
	locations = [ghjkl]
	secrets = []

	name = 'myadventure'
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

