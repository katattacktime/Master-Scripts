# Used to format anything that isn't a devilgram. Now with added support to choose the language to format. Default is EN. Can be changed by adding -l [lang code] to the end of the command line argument

from pyparsing import Suppress, SkipTo, Word, nums, dblQuotedString, OneOrMore, Literal, ParserElement, removeQuotes
import os
import pathlib
import re
import argparse

LANGS = {
	"ja" : 0,
	"en" : 1,
	"zh" : 2,
	"ko" : 3
}

FORMATTING_TAG_REGEX = re.compile('<.*?>')

args = None
current_lang = "en"
output_file = None

current_selection = {}
selection_hierarchy = {}
current_label = None

def get_arguments():
	arg_parser = argparse.ArgumentParser(description='Parse card story from Obey Me!')
	arg_parser.add_argument('-l', '--languages', type=str, nargs='+', default=["en"],
		choices=LANGS.keys(), help='Languages to output')
	arg_parser.add_argument('-t', '--tags', type=bool, default=True, help='If true tags will be removed (e.g. <b>)')
	arg_parser.add_argument('-r', '--rename', type=bool, default=False, help='Change file name to title')
	arg_parser.add_argument('--fixname', type=bool, default=True, help="Remove symbols from name that aren't supported by windows")
	return arg_parser.parse_args()

def get_raw_files():
	path = pathlib.Path(__file__).parent.absolute()
	files = [f for f in os.listdir(path) if f.endswith(".txt")]
	files.sort()
	return files

def get_script_parser():
	header = Suppress(SkipTo(Literal('Command commands'), True) + Literal('Array Array\n\t\tint size = ') + Word(nums))
	command_name = (Suppress(SkipTo(Literal("string commandName = "), True)) + dblQuotedString).setParseAction(removeQuotes)('command_name')
	string_data = Suppress(SkipTo(Literal("string data = "), True)) + dblQuotedString.setParseAction(removeQuotes)
	strings = (string_data + string_data + string_data + string_data + string_data + string_data)("strings")
	command = (command_name + strings).setParseAction(lambda t: {'command_name': t.command_name, 'strings':t.strings.asList()})
	mono_behaviour = (header + OneOrMore(command))
	ParserElement.parseWithTabs(mono_behaviour)
	return mono_behaviour

def get_translation(full_string):
	lang_index = LANGS[current_lang]
	translations = full_string.split('@')
	if len(translations) <= lang_index:
		raise ValueError(f'No {current_lang} translation for line {full_string}')
	return translations[lang_index]

def process_title(full_string):
	title = get_translation(full_string)
	title = title.replace('\\n', '')
	output_file.write(title + '\n\n')

def push_phrase(phrase):
	if current_label is not None:
		current_selection[current_label]['responses'].append(phrase)
	else:
		output_file.write(phrase['chara'] + (': ' if phrase['chara'] != '' else '') + phrase['text'] + '\n')

def process_text(character_full, phrase_full):
	chara = '' if character_full == '' else get_translation(character_full)
	phrase = '' if phrase_full == '' else get_translation(phrase_full)
	phrase = phrase.replace('\\n', '') #use strip to retain newlines between sentences?
	if args.tags:
		phrase = re.sub(FORMATTING_TAG_REGEX, '', phrase)

	push_phrase({'chara': chara, 'text': phrase, 'selection': {}})

def start_selection():
	global selection_hierarchy
	global current_selection

	if current_label is not None:
		new_selection = {}
		current_selection[current_label]['responses'].append({'chara': '', 'text': '', 'selection': new_selection})
		current_selection = new_selection
	else:
		current_selection = selection_hierarchy

def start_response(label):
	global current_label
	current_label = label

def add_selection_option(label, full_phrase):
	phrase = get_translation(full_phrase).replace('\\n', '')
	if args.tags:
		phrase = re.sub(FORMATTING_TAG_REGEX, '', phrase)
	current_selection[label] = {'option': phrase, 'responses': []}

def move_to_previous_selection(parent_selection):
	global current_label
	global current_selection

	found_selection = False

	for label, branch in parent_selection.items():
		for response in branch['responses']:
			if response['selection'] == current_selection:
				current_label = label
				current_selection = parent_selection
				return True
			elif response['selection'] != {}:
				found_selection = move_to_previous_selection(response['selection'])
				if found_selection:
					return True

	return False

def print_selection(selection, level):
	sel_count = 0
	for key, value in selection.items():
		sel_count = sel_count + 1
		for i in range(0, level):
			output_file.write('\t')
		output_file.write(str(sel_count) + ') ' + value['option'] + '\n')
		for response in value['responses']:
			if response['selection'] != {}:
				print_selection(response['selection'], level + 1)
			else:
				for i in range(0, level + 1):
					output_file.write('\t')
				output_file.write(response['chara'] + (': ' if response['chara'] != '' else '') + response['text'] + '\n')

def process_bg(bg):
	if bg != '':
		output_file.write(f'*change background to {bg}*\n')
	else:
		output_file.write('*fade to black*\n')

def start_sns():
	output_file.write('*start chat*\n')

def end_sns():
	output_file.write('*end chat*\n')

def process_stamp(character_full, stamp):
	chara = '' if character_full == '' else get_translation(character_full)
	push_phrase(chara, stamp)

def start_call():
	output_file.write('*start call*\n')

def end_call():
	output_file.write('*end call*\n')

def process_phone_text(phrase_full, voice):
	phrase = '' if phrase_full == '' else get_translation(phrase_full)
	phrase = phrase.replace('\\n', '') #use strip to retain newlines between sentences?
	if args.tags:
		phrase = re.sub(FORMATTING_TAG_REGEX, '', phrase)

	phrase = phrase + ' | ' + voice

	push_phrase({'chara': '', 'text': phrase, 'selection': {}})

def main():
	global args
	global current_lang
	global output_file

	args = get_arguments()

	os.makedirs("output", exist_ok=True)
	files = get_raw_files()
	parser = get_script_parser()

	title = ''

	for file_name in files:
		global current_label
		with open(file_name, 'r', encoding='utf8') as raw_file:
			prepared_text = raw_file.read().replace('オナマエ', 'MC')
			parsed_text = parser.parseString(prepared_text)

		for lang in args.languages:
			current_lang = lang
			output_file_name = pathlib.Path(file_name).stem + "_" + lang
			output_file_path = os.path.join("output", output_file_name + '.txt')
			with open(output_file_path, 'w', encoding='utf8') as output_file:
				for action in parsed_text:
					try:
						if action['command_name'] == 'show_title':
							title = get_translation(action['strings'][0])
							process_title(action['strings'][0])
							continue

						if action['command_name'] == 'text' or action['command_name'] == 'sns_text':
							process_text(action['strings'][2], action['strings'][3])
							continue

						if action['command_name'] == 'message':
							process_text(action['strings'][0], action['strings'][1])
							continue

						if action['command_name'] == 'start_sel_text' or action['command_name'] == 'start_sel_stamp':
							start_selection()
							continue

						if action['command_name'] == 'sel_text' or action['command_name'] == 'sel_stamp':
							add_selection_option(action['strings'][0], action['strings'][1])
							continue

						if action['command_name'] == 'sel_label':
							start_response(action['strings'][0])

						if action['command_name'] == 'end_sel':
							global selection_hierarchy
							global current_selection

							moved_successfully = move_to_previous_selection(selection_hierarchy)

							if not moved_successfully:
								print_selection(selection_hierarchy, 0)
								current_selection = {}
								selection_hierarchy = {}
								current_label = None

							continue

						#TODO bg names
						if action['command_name'] == 'bg' or action['command_name'] == 'bg_switch':
							process_bg(action['strings'][0])
							continue

						if action['command_name'] == 'sns_start':
							start_sns()
							continue

						if action['command_name'] == 'sns_end':
							end_sns()
							continue

						#TODO stamp names
						if action['command_name'] == 'sns_stamp' or action['command_name'] == 'sns_image':
							process_stamp(action['strings'][2], action['strings'][3])
							continue

						if action['command_name'] == 'phone_start':
							start_call()
							continue

						if action['command_name'] == 'phone_end':
							end_call()
							continue

						if action['command_name'] == 'phone_text':
							process_phone_text(action['strings'][3], action['strings'][5])

					except ValueError as err:
						print(f'Encountered error while processing {file_name}: {err}')
						break

			if args.rename and title != '':
				title = title.replace('\\n', '')
				if args.fixname:
					title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
				new_file_path = os.path.join('output', title + '.txt')
				os.rename(output_file_path, new_file_path)


main()
