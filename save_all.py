import json
import sys
import re
without_formatting = ["master_item", "master_collection"]
with open("dump.txt", "r", encoding='utf-8') as read_file:
	masters = json.load(read_file)
	for (k, v) in masters.items():
		with open(k + ".json", 'w', encoding='utf-8') as f:
			if k not in without_formatting:
			    json.dump(v, f, ensure_ascii=False, indent=4)
			else:
				unformatted_string = json.dumps(v, ensure_ascii=False)
				unformatted_string = unformatted_string.replace("}, {", "},\n{")
				unformatted_string = unformatted_string.replace("[{", "[\n{")
				f.write(unformatted_string)