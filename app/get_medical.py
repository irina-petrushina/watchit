import pandas as pd
import requests
import re
#import bs4



def get_medical_vo2max(age, gender):
	'''This function takes a vo2max data table from the website and returns the max amd min values for the user.'''

	url1 = 'https://www.brianmac.co.uk/vo2max.htm'

	df = pd.read_html(url1)[2]
	df.columns = df.iloc[0]
	df = df.drop([0])

	cols = ['Male', 'Female', 'Age']
	for col in cols:
		df[col.lower()+'_low'] = df[col].apply(lambda x: int(x[0:2]))
		df[col.lower()+'_high'] = df[col].apply(lambda x: int(x[3:5]))
		df =  df[(df['age_low']<=age) & (df['age_high']>=age)]    

	if gender == 0:
		return df[['female_low', 'female_high']].values.flatten().tolist()
	else:
		return df[['male_low', 'male_high']].values.flatten().tolist()


def get_medical_sleep(age):
	'''This function takes sleep data table from the website and returns the max and min values for the user.'''

	url = 'https://www.cdc.gov/sleep/about_sleep/how_much_sleep.html'

	response = requests.get(url)

	soup = BeautifulSoup(response.text)
	parent = soup.find('table', attrs={'class': 'table table-bordered themed opt-in show-more-div-249'}) 
	table_elements = parent.find_all('th')

	ages = []
	hours = []
	pattern = r'(\d*)–?(\d+)?\s((?:hours|years|or more hours))'
	count = 0
	for i, el in enumerate(table_elements):
		if re.match(pattern, el.text):
			count += 1
			if count == 1:
				ages.append(re.findall(pattern, el.text)[0])
			elif ('hours' in re.findall(pattern, el.text)[0][2]):
				hours.append(re.findall(pattern, el.text)[0])
			elif ('years' in re.findall(pattern, el.text)[0]):
				ages.append(re.findall(pattern, el.text)[0])

	age_low = [int(age[0]) for ind, age in enumerate(ages)]
	age_high = [int(age[1]) if age[1] else 100 for ind, age in enumerate(ages)]
	sleep_low = [int(hour[0]) for ind, hour in enumerate(hours)]
	sleep_high = [int(hour[1]) if hour[1] else 10 for ind, hour in enumerate(hours)]

	sleep = pd.DataFrame({'age_low': age_low[1:], 'age_high': age_high[1:], 'sleep_low': sleep_low[1:], 'sleep_high': sleep_high[1:]})

	df =  sleep[(sleep['age_low']<=age) & (sleep['age_high']>=age)]

	return df[['sleep_low', 'sleep_high']].values.flatten().tolist()[:2]



def get_medical(age, gender):

	medical = dict()

	medical['vo2max'] = get_medical_vo2max(age, gender)
	medical['sleep'] = get_medical_sleep(age)

	return medical
