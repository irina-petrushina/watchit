import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

def get_age(demo_tree):
	""" This function receives the demographic tree, and returns user_age as an integer.
	If the value is not found, a user input is requested."""

	print('getting age...')
	
	dob = demo_tree[0]['HKCharacteristicTypeIdentifierDateOfBirth']

	if not dob:
		user_age = input()
	else:
		user_age = int((datetime.today() - datetime.strptime(dob, '%Y-%m-%d')).days/365)  
	return user_age

def get_gender(demo_tree):
	""" This function receives the demographic tree, and returns user_gender as 0 [Female] or 1 [Male].If the value is not found, a user input is requested."""

	print('getting gender...')
	
	gender = demo_tree[0]['HKCharacteristicTypeIdentifierBiologicalSex']
	if not gender:
		user_gender = input()
	else:
		if gender[15:] == 'Female':
			user_gender = 0
		else:
			user_gender = 1
	return user_gender

def get_sleep(df):
	""" This function receives the main df, and returns user_sleep data as 
	a dataframe with columns ['date', 'sleep_hours']."""

	print('getting sleep...')

	sleep_df = df[df['type'] == "SleepAnalysis"]

	device_list = list(sleep_df['sourceName'].unique())
	watch_name = [el for el in device_list if 'watch' in el.lower()][0]
	sleep_df = sleep_df[sleep_df['sourceName']==watch_name]

	sleep_df['time_asleep'] = sleep_df['endDate'] - sleep_df['startDate']

	sleep_df_gb = sleep_df.groupby('startDate').agg(total_time_asleep=('time_asleep', 'min'), creationDate=('creationDate', 'max'))
	sleep = sleep_df_gb.reset_index().groupby('creationDate').agg(value=('total_time_asleep', 'sum'),bed_time=('startDate', 'min'), sleep_counts=('creationDate','count'))

	sleep['value'] = (sleep['value'].dt.total_seconds()/60/60)
	sleep = sleep['value']

	return sleep

def get_vo2max(df):
	""" This functions receives the main df, and returns user_vo2max data as 
	a dataframe with columns ['date', 'vo2max']. vo2max is measured in mL/min·kg. """

	print('getting vo2max...')

	vo2max = df[df['type']=='VO2Max']
	vo2max = vo2max[['creationDate', 'value']]
	vo2max.set_index('creationDate')

	return vo2max

def watch_data_analysis(filename):

	tree = ET.parse(filename)

	root = tree.getroot()
	record_list = [x.attrib for x in root.iter('Record')]
	demo_tree = [x.attrib for x in root.iter('Me')]
	data = pd.DataFrame(record_list)

	for col in ['creationDate', 'startDate', 'endDate']:
		data[col] = pd.to_datetime(data[col])

	data['value'] = pd.to_numeric(data['value'], errors='coerce')
	data['value'] = data['value'].fillna(1.0)
	data['type'] = data['type'].str.replace('HKQuantityTypeIdentifier', '')
	data['type'] = data['type'].str.replace('HKCategoryTypeIdentifier', '')

	user_data = dict()
	user_data['user_age'] = get_age(demo_tree)
	user_data['user_gender'] = get_gender(demo_tree)
	user_data['user_sleep'] = get_sleep(data)
	user_data['user_vo2max'] = get_vo2max(data)

	return user_data
