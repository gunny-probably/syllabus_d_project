import csv
from flask import Flask, render_template, abort

app = Flask(__name__)

def get_csv():
	csv_path = './static/syllables_d_labelled_2.csv'
	# Open for reading using python's built-in open() function
	csv_file = open(csv_path, 'rb')
	# Parse csv and return as a list of dictionaries
	csv_obj = csv.DictReader(csv_file)
	# Convert list of dictionaries to permanent list.
	csv_list = list(csv_obj)
	# gunny dev note: supporting lines to clean data 
	rev_mapping_master = []
	index = 0
	for row in csv_list:
		index += 1
		keys_new = row.values()
		values_new = map(lambda x : str(index) + x, row.keys())
		rev_mapping = dict(zip(keys_new, values_new))
		rev_mapping_clean = []
		for pair in rev_mapping.items():
			if ';' in pair[0]:
				# confusion is a list of confusing substrings
				confusion = pair[0].split(';')
				confusion = map(lambda x : x.strip(), confusion)
				confusion = map(lambda x : (x, pair[1]), confusion)
				rev_mapping_clean += confusion
			else:
				rev_mapping_clean.append(pair)
		rev_mapping_clean = dict(rev_mapping_clean)
		rev_mapping_master.append(rev_mapping_clean)
		# gunny dev note: there are semi-colon delimited values 
	# gunny dev note: priority hit list
	'''
	priority = {}
	priority["u"] = 
	priority["ue"] = 
	priority["oo"] = 
	priority["ou"] = 
	priority["ew"] = 
	'''
	return rev_mapping_master


def precedence(dict_list, ):
	# gunny dev note: to enforce precedence for certain column mappings 
	pass

'''
what we need:
1. reverse dictionary representation (map substring to row-column)
2. function that acts on input string
'''

@app.route("/")
def index():
	template = 'index.html'
	# Still a list of dictionaries.
	object_list = get_csv()
	# Pull csv data and pass it on the top of the template as follows:
	# object_list param takes a list of dictionaries; each dict being a row
	return render_template(template, object_list=object_list)

@app.route("/<word>/")
def detail(word):
	template = "detail.html"
	object_list = get_csv()
	#word_list = bar.split(" ")
	# gunny dev note: finds first match in list of dicts as enforced by get_csv()
	#production = ""

	# gunny dev note: parse the whole word not just the endswith()
		# split word based on list of consonants used 
	# gunny dev note: use table of prefixes predceding vowels to decide *right* vowel fit

	# gunny dev note: save processed strings somewhere
	for row in object_list:
		for substring in row.keys():
			if word.endswith(substring):
				word = word[:-len(substring)]
				word += row[substring]
				word_list = word.split(" ")
				word_last = word_list[-1]
				word_last = "(" + word_last + ")"
				word_list[-1] = word_last
				word = " ".join(word_list)
				return render_template(template, object=word)
	abort(404)		

# This check allows you to run any python script as a program
if __name__ == "__main__":
	# Fire up the flask test server.
	app.run(debug=True, use_reloader=True)



