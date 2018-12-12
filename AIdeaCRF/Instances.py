#encoding:utf-8

import os
import sys
import os.path
import time
import numpy as np

def Instances():
	if len(sys.argv) <= 1:
		print("Enter Input File!")
	else:
		inputfile = sys.argv[1]
		outputfile = sys.argv[2]
		errorfile = sys.argv[3]

	fopen = open(inputfile, 'r', encoding="utf-8")
	context = fopen.readlines()

	data = []
	tagged = ""
	count = 0
	for row in context:
		if row != '\n':
			if not "\tO" in row:
				count = count + 1
				tagged = tagged + row
				data.append(row)
	tags = np.array(data)

	rowcount = 0
	entity, entities, previous_tag, errordata = "", "", "", ""
	for rows in tags:
		rowcount = rowcount + 1
		row = rows.strip('\n')
		row = row.split('\t')
		length = len(row)
		word = row[0]
		tag = row[length-1]
		
		if tag == "B-Disease":
			if entity != "":
				entities = entities + entity + "\n"
			entity = "Disease\t" + word
		elif tag == "I-Disease":
			if previous_tag == "B-Disease":
				entity = entity + " " + word
			elif previous_tag == "I-Disease":
				entity = entity + " " + word
			else:
				error = str(rowcount) + word + "\t" + tag + "\n"
				errordata = errordata + error
				print(error)

		if tag == "B-Gene":
			if entity != "":
				entities = entities + entity + "\n"
			entity = "Gene\t" + word
		elif tag == "I-Gene":
			if previous_tag == "B-Gene":
				entity = entity + " " + word
			elif previous_tag == "I-Gene":
				entity = entity + " " + word
			else:
				error = str(rowcount) + word + "\t" + tag + "\n"
				errordata = errordata + error
				print(error)

		if tag == "B-Chemical":
			if entity != "":
				entities = entities + entity + "\n"
			entity = "Chemical\t" + word
		elif tag == "I-Chemical":
			if previous_tag == "B-Chemical":
				entity = entity + " " + word
			elif previous_tag == "I-Chemical":
				entity = entity + " " + word
			else:
				error = str(rowcount) + word + "\t" + tag + "\n"
				errordata = errordata + error
				print(error)

		if tag == "O":
			if previous_tag == "B-Disease":
				entities = entities + entity + "\n"
			elif previous_tag == "I-Disease":
				entities = entities + entity + "\n"

			if previous_tag == "B-Gene":
				entities = entities + entity + "\n"
			elif previous_tag == "I-Gene":
				entities = entities + entity + "\n"

			if previous_tag == "B-Chemical":
				entities = entities + entity + "\n"
			elif previous_tag == "I-Chemical":
				entities = entities + entity + "\n"

		previous_tag = tag

	fopen = open(outputfile, 'w', encoding='utf-8')
	fopen.write(entities)
	fopen = open(errorfile, 'w', encoding='utf-8')
	fopen.write(errordata)

if __name__ == '__main__':
	start = time.time()
	Instances()
	end = time.time()
	cost = round((end - start), 2)

	print("Finished")
	print(str(cost) + "s")