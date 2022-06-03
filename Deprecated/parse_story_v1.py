from pyparsing import Suppress, SkipTo, Word, nums, dblQuotedString, OneOrMore, Literal, ParserElement, removeQuotes
import os
from os.path import isfile, join, dirname
import pathlib
import re
import json

def print_selection( selection, level, file ):
	sel_count = 0
	for key, value in selection.items():
		sel_count = sel_count + 1
		for i in range(0, level):
			file.write('\t')
		file.write(str(sel_count) + ') ' + value['option'] + '\n')
		for response in value['responses']:
			if response['selection'] != {}:
				print_selection( response['selection'], level + 1, file )
				continue
			for i in range(0, level + 1):
				file.write('\t')
			file.write(response['chara'] + (': ' if response['chara'] != '' else '') + response['phrase'] + '\n')

replaced_names = {
	"Seven Rulers of Hell<img id=sns_emoji_00014>": "Seven Rulers of Hell (Lucifer)",
	"Seven Rulers of Hell<img id=sns_emoji_00015>": "Seven Rulers of Hell (Mammon)",
	"Seven Rulers of Hell<img id=sns_emoji_00016>": "Seven Rulers of Hell (Leviathan)",
	"Seven Rulers of Hell<img id=sns_emoji_00017>": "Seven Rulers of Hell (Satan)",
	"Seven Rulers of Hell<img id=sns_emoji_00018>": "Seven Rulers of Hell (Asmodeus)",
	"Seven Rulers of Hell<img id=sns_emoji_00012>": "Seven Rulers of Hell (Beelzebub)",
	"Seven Rulers of Hell<img id=sns_emoji_00013>": "Seven Rulers of Hell (Belphegor)"}

header = Suppress(SkipTo(Literal('Command commands'), True) + Literal('Array Array\n\t\tint size = ') + Word(nums))
command_name = (Suppress(SkipTo(Literal("string commandName = "), True)) + dblQuotedString).setParseAction(removeQuotes)('command_name')
string_data = Suppress(SkipTo(Literal("string data = "), True)) + dblQuotedString.setParseAction(removeQuotes)
strings = (string_data + string_data + string_data + string_data + string_data + string_data)("strings")
command = (command_name + strings).setParseAction(lambda t: {'command_name': t.command_name, 'strings':t.strings.asList()})
mono_behaviour = (header + OneOrMore(command))
ParserElement.parseWithTabs(mono_behaviour)

rem_tag = re.compile('<.*?>')
os.makedirs("output", exist_ok=True)

path = pathlib.Path(__file__).parent.absolute()
files = [f for f in os.listdir(path) if f.endswith(".txt")]
files.sort()
story_name = ''
selection = {}
selections = []
label = []
first_location_loaded = False

for fil in files:
	with open(fil, 'r', encoding='utf8') as f:
		first_location_loaded = False
		parsed = mono_behaviour.parseString(f.read())
		story_name = fil
		if parsed[0]['command_name'] == 'show_title':
			del parsed[0]

		if story_name != '':
			with open(os.path.join("output", story_name), 'a', encoding='utf8') as file:
				for action in parsed:
					action['strings'] = list(map(lambda s: s.replace('オナマエ', 'MC'), action['strings']))

					#formats story texts
					if action['command_name'] == 'text':
						chara = action['strings'][2].split('@', 1)
						chara = chara[1] if len(chara) > 1 else ''
						phrase = action['strings'][3].split('@', 1)
						phrase = re.sub(rem_tag, '', phrase[1].replace('\\n', '')) if len(phrase) > 1 else ''
						if len(label) != 0:
							selection[label[-1]]['responses'].append({'chara': chara, 'phrase': phrase, 'selection': {}})
						else:
							file.write(chara + (': ' if chara != '' else '') + phrase + '\n')


					#formats messages
					if action['command_name'] == 'message':
						chara = action['strings'][0].split('@', 1)
						chara = chara[1] if len(chara) > 1 else ''
						phrase = action['strings'][1].split('@', 1)
						phrase = re.sub(rem_tag, '', phrase[1].replace('\\n', '')) if len(phrase) > 1 else ''
						if len(label) != 0:
							selection[label[-1]]['responses'].append({'chara': chara, 'phrase': phrase, 'selection': {}})
						else:
							file.write(chara + (': ' if chara != '' else '') + phrase + '\n')


					#formats story options (container)
					if action['command_name'] == 'start_sel_text':
						if selection != {}:
							selections.append(selection)
						selection = {}
						label.append('')

					#formats MC's option
					if action['command_name'] == 'sel_text':
						option = action['strings'][1].split('@', 1)
						option = option[1].replace('\\n', '') if len(option) > 1 else ''
						selection[action['strings'][0]] = {'option': re.sub(rem_tag, '', option), 'responses': []}

					#formats the reply to indivitual options
					if action['command_name'] == 'sel_label':
						label[-1] = action['strings'][0]

					#formats the end of the story options
					if action['command_name'] == 'end_sel':
						del label[-1]
						if len(selections) != 0:
							selections[-1][label[-1]]['responses'].append({'chara': '', 'phrase': '', 'selection': selection})
							selection = selections[-1]
							del selections[-1]
						else:
							print_selection( selection, 0, file )
							selection = {}


					#formats the output of change of background		
					if action['command_name'] == 'bg_switch':
						file.write('*fade to black*\n')
					if action['command_name'] == 'bg':
						if first_location_loaded == False:
							first_location_loaded = True
						else:
							file.write('*change location*\n')

					
					#formats the start of the sns
					if action['command_name'] == 'sns_start':
						file.write('*start chat*\n')

					#formats the end of the sns
					if action['command_name'] == 'sns_end':
						file.write('*end chat*\n')

					#formats the sns message
					if action['command_name'] == 'sns_text':
						chara = action['strings'][2].split('@', 1)
						chara = chara[1] if len(chara) > 1 else ''
						phrase = action['strings'][3].split('@', 1)
						phrase = re.sub(rem_tag, '', phrase[1].replace('\\n', '')) if len(phrase) > 1 else ''
						if len(label) != 0:
							selection[label[-1]]['responses'].append({'chara': chara, 'phrase': phrase, 'selection': {}})
						else:
							file.write(chara + (': ' if chara != '' else '') + phrase + '\n')

					#formats the sns stamps
					if action['command_name'] == 'sns_stamp':
						chara = action['strings'][2].split('@', 1)
						chara = chara[1] if len(chara) > 1 else ''
						if len(label) != 0:
							selection[label[-1]]['responses'].append({'chara': chara, 'phrase': action['strings'][3], 'selection': {}})
						else:
							file.write(chara + (': ' if chara != '' else '') + action['strings'][3] +'\n')

					#formats stamps options (container)
					if action['command_name'] == 'start_sel_stamp':
						if selection != {}:
							selections.append(selection)
						selection = {}
						label.append('')
					
					#formats the sns stamp output
					if action['command_name'] == 'sel_stamp':
						selection[action['strings'][0]] = {'option': action['strings'][1], 'responses': []}

					#formats the sns image output
					if action['command_name'] == 'sns_image':
						chara = action['strings'][2].split('@', 1)
						chara = chara[1] if len(chara) > 1 else ''
						if len(label) != 0:
							selection[label[-1]]['responses'].append({'chara': chara, 'phrase': action['strings'][3], 'selection': {}})
						else:
							file.write(chara + (': ' if chara != '' else '') + action['strings'][3] + '\n')


					#formats the start of the phone call
					if action['command_name'] == 'phone_start':
						file.write('*start call*\n')

					#formats the end of the phone call
					if action['command_name'] == 'phone_end':
						file.write('*end call*\n')
					
					#formats the phone text
					if action['command_name'] == 'phone_text':
						phrase = action['strings'][3].split('@', 1)
						phrase = (re.sub(rem_tag, '', phrase[1].replace('\\n', '')) if len(phrase) > 1 else '') + ' | ' + action['strings'][5]
						if len(label) != 0:
							selection[label[-1]]['responses'].append({'chara': '', 'phrase': phrase, 'selection': {}})
						else:
							file.write(phrase + '\n')