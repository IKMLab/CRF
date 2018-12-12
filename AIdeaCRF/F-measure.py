#encoding:utf-8

import os
import sys
import os.path
import time
import numpy as np

def Fmeasure():
	if len(sys.argv) <= 1:
		print("Enter Input File!")
	else:
		inputfile = sys.argv[1]
	answerfile = "../Output/Answer_Instances.txt"

	fopen = open(inputfile, 'r', encoding='utf-8')
	context = fopen.readlines()
	A_Data = np.array(context)
	fopen = open(answerfile, 'r', encoding='utf-8')
	context = fopen.readlines()
	R_Data = np.array(context)

	C, E = 0, 0
	AT = np.size(A_Data)
	RT = np.size(R_Data)
	for row in A_Data:
		if row != '\n':
			if row in R_Data:
				search = np.where(R_Data == row)
				for s in search:
					result = np.array(s)
				ans = result[0]
				R_Data = np.delete(R_Data, ans)
				C = C + 1
			else:
				E = E + 1

	Precision = round((C/RT), 4)
	Recall = round((C/AT), 4)
	Fscore = round((2*Precision*Recall)/(Precision + Recall), 6)
	print("Precision: " + str(Precision))
	print("Recall: " + str(Recall))
	print("F-score: " + str(Fscore))
	print()

if __name__ == '__main__':
	start = time.time()
	Fmeasure()
	end = time.time()
	cost = round((end - start), 2)

	print("Finished")
	print(str(cost) + "s")