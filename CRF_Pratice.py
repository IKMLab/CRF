import os

def readCorpus(path):
	set_dict = dict()
	pmID_list = list()
	with open(path,'r') as file:
		for row in file:
			row = row.strip("\n\r")
			if "|t|" in row:
				pmID = row.split("|t|")[0]
				pmID_list.append(pmID)
				content = row.split("|t|")[1]
				# store the title
				set_dict[pmID] = [row]
			elif "|a|" in row:
				pmID = row.split("|a|")[0]
				content += ' ' + row.split("|a|")[1]
				# store the abtract
				set_dict[pmID].append(row)
				# store the whole article without the pmID, '|t|' & '|a|'
				set_dict[pmID].append(content)

	return set_dict, pmID_list

def load_resultFile(path):
	# store all the mentions of all the articles
	all_disease_list = list()
	# store all the mentions of the article
	mentions_list = list()
	# store every token in a mention
	part_of_mention = list()

	with open(path,'r') as predict_file:
		for row in predict_file:
			row = row.rstrip('\n\r')

			# if the row is empty means this article is ended
			if len(row) == 0:
				# if the mention appears at the end of the article, and store it
				if len(part_of_mention) != 0:
					mentions_list.append(part_of_mention)
				# store all the mention that appear in this article into mention_list, and clear the lists
				all_disease_list.append(mentions_list)
				part_of_mention = list()
				mentions_list = list()
			else:
				# get the token and tag
				token = row.split()[0]
				tag = row.split()[-1]

				if tag.split('-')[0] == 'B':
					# if the tag is 'B' may be a beginning of a mention or a independent mention that only includes one token
					# 'B' with 'B', store the previous mention and clear the list
					if len(part_of_mention) != 0:
						mentions_list.append(part_of_mention)
						part_of_mention = list()
					part_of_mention = [token]
				elif tag.split('-')[0] == 'I':
					part_of_mention.append(token)
				elif tag.split('-')[0] == 'E':
					part_of_mention.append(token)
					# 'E' is the last label in a mention, store the mention and clear the list
					mentions_list.append(part_of_mention)
					part_of_mention = list()
				else:
					if len(part_of_mention) != 0:
						mentions_list.append(part_of_mention)
						part_of_mention = list()
		
	return all_disease_list

def NER(pd_path, set_dict, pmID_list):

	# load the result file
	all_disease_list = load_resultFile(pd_path)
	print('load file done')

	# run through every article
	for idx in range(len(pmID_list)):
		pmID = pmID_list[idx]
		
		content = set_dict[pmID][2]
		prd_mentions_list = all_disease_list[idx]
		NER_list = list()

		tmp_position = 0

		for prd_part_of_mention in prd_mentions_list:

			mention = ''
			for part_idx in range(len(prd_part_of_mention)):
				if content.find(mention + prd_part_of_mention[part_idx], tmp_position) != -1:
					mention = mention + prd_part_of_mention[part_idx]
					
					start_offset = content.find(mention, tmp_position)

				elif content.find(mention + ' ' + prd_part_of_mention[part_idx] , tmp_position) != -1:
					mention = mention + ' ' + prd_part_of_mention[part_idx]
					
					start_offset = content.find(mention, tmp_position)

			NER = pmID + '\t' + str(start_offset) + '\t' + str(start_offset+len(mention)) + '\t' + mention + '\t' + 'Disease' + '\n'
			NER_list.append(NER)
			tmp_position = content.find(mention, tmp_position) + len(mention)

		set_dict[pmID].append(NER_list)
	return set_dict

def product_NERFile(set_dict, pmID_list, R_path):
	NER_file = open(R_path, 'w')

	for pmID in pmID_list:
		title = set_dict[pmID][0] + '\n'
		abstract = set_dict[pmID][1] + '\n'
		NER_list = set_dict[pmID][3]

		NER_str = ''
		for NER in NER_list:
			NER_str += NER

		NER_file.write(title+abstract+NER_str+'\n')

	NER_file.close()


def main():
	
	# Train CRF++
	template_file = "data/D_template" 
	train_data = "data/D_training.data"
	model_path = "data/D_training.model"
	os.system("./CRF++-0.58/crf_learn -f 1 -c 1.0 -p 1 "+ template_file +" "+ train_data +" "+ model_path)
	print('Train CRF Done.')

	# Test CRF++
	test_data = "data/D_testing.data"
	pd_result = "data/predict_res"
	os.system("./CRF++-0.58/crf_test -m "+ model_path +" "+ test_data+" > "+ pd_result)
	print('Test CRF Done.')

	# Turn predict result into PubTator format
	gt_path = 'corpus/CDR_TestSet.PubTator.txt'
	gt_dict, gt_PMID_list = readCorpus(gt_path)
	pd_dict = NER(pd_result, gt_dict, gt_PMID_list)
	pd_NER_path = 'data/NER'
	product_NERFile(pd_dict, gt_PMID_list, pd_NER_path)
	print('NER Done.')

	# Evaluate the result using BC5 evaluate tool
	eva_result_path = 'evaluation/eva_result'
	
	os.system("sh ./evaluation/eval_mention.sh PubTator " + gt_path + " " + pd_NER_path + " " + eva_result_path)
	print('Evaluate Done.')

main()