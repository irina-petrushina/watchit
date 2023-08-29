import pandas as pd
import requests
import re
from app import plot_healthscore, plot_sleepscore
 

def get_medical_vo2max(age, gender, user_healthscore):
	'''This function takes a vo2max data table from the website and returns the max amd min values for the user.'''

	df = pd.read_csv('app/raw_data/medical_vo2max.csv', index_col=False).astype('int32')
	if age < 20:
		med_age_group = 29
	elif age >= 80:
		med_age_group = 79
	else:	
		med_age_group = (age//10)*10+9
	
	plot_healthscore.plot_healthscore(df[(df['gender']==gender) & (df['Age']==med_age_group)], user_healthscore)	
	health_dict = df[(df['gender']==gender) & (df['Age']==med_age_group)][['Poor', 'Fair', 'Good', 'Excellent', 'Superior',]].to_dict('list')
	health_indicator = {val[0]: key for key, val in health_dict.items()} 
	for ind, el in enumerate(health_indicator.keys()):
		if ind == 0 and user_healthscore < el:
			return health_indicator[el]
		elif ind == len(health_indicator.keys())-1 and user_healthscore>el:
			return health_indicator[el]
		elif el == user_healthscore:
			return health_indicator[el]
		elif list(health_indicator.keys())[ind-1] < user_healthscore and el > user_healthscore:
			return health_indicator[list(health_indicator.keys())[ind-1]]	
	

def get_medical_sleep(age, user_sleepscore):
	'''This function takes sleep data table from the website and returns the max and min values for the user.'''
	
	sleep = pd.read_csv('app/raw_data/medical_sleep.csv').astype('int32')

	df =  sleep[(sleep['age_low']<=age) & (sleep['age_high']>=age)]

	sleep_range = df[['sleep_low', 'sleep_high']].values.flatten().tolist()[:2]
	
	plot_sleepscore.plot_sleepscore(sleep_range, user_sleepscore)

	if user_sleepscore < sleep_range[0]:
		return ('Poor', sleep_range)
	else:
		return ('Good', sleep_range)



def get_medical(age, gender, user_healthscore, user_sleepscore):

	medical = dict()

	medical['vo2max'] = get_medical_vo2max(age, gender, user_healthscore)
	medical['sleep_tag'], medical['sleep'] = get_medical_sleep(age, user_sleepscore)

	return medical
