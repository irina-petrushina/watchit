import pandas as pd
import numpy as np
import altair as alt


def plot_demo_bar(med_score, user_healthscore):
	
	sch = 'plasma'
	fs = 30	
	source = pd.DataFrame({'a': [0.5, 2], 'b': [user_healthscore, med_score], 'x': [-0.8, 5.1], 'y': [0,0], 'label': ['You', 'Population Average']})

	base = alt.Chart(source).encode(alt.Y('b', axis = None, scale = alt.Scale(domain=[0, 70])),alt.X('a:Q', axis=None),color = alt.Color('b').scale(domain=[28, 68], scheme=sch, type='log'),text='b')


	text = alt.Chart(source).encode(x=alt.X('x'),y=alt.Y('y'),color = alt.Color('b', legend=None).scale(scheme=sch),text=alt.Text('label'))

	plot = (base.mark_bar(cornerRadiusTopLeft=20,cornerRadiusTopRight=20,cornerRadiusBottomLeft=20,cornerRadiusBottomRight=20,width = 100) + base.mark_text(align='center', dx=0, dy = -15, fontSize=40) + text.mark_text(dy = -15, fontSize=fs)).configure_view(strokeWidth=0).configure_scale(bandPaddingInner=0).properties(width=500, height=400).save('app/static/assets/img/user_demo_average.png', scale_factor=5.0)

def get_demo_sleep(age, gender, score):
	df = pd.read_csv('app/raw_data/demo_sleep.csv').astype('int32')
	user_demo = df[(df['age_low']<=age) & (df['age_high']>=age) & (df['gender']==gender)] 
	demo_sleep = {'sleep_avg': user_demo['sleep'].mean(), 'sleep_min':user_demo['sleep'].mean()-user_demo['sleep'].std(), 'sleep_max':user_demo['sleep'].mean()+user_demo['sleep'].std()}
	return demo_sleep

def get_demo_vo2max(age, gender, score):
	df = pd.read_csv('app/raw_data/demo_vo2max.csv').astype('int32')
	user_demo = df[(df['age_low']<=age) & (df['age_high']>=age) & (df['gender']==gender)] 	
	demo_vo2max = {'vo2max_avg': user_demo['vo2max'].mean(), 'vo2max_min':user_demo['vo2max'].mean()-user_demo['vo2max'].std(), 'vo2max_max':user_demo['vo2max'].mean()+user_demo['vo2max'].std()}
	
	plot_demo_bar(int(demo_vo2max['vo2max_avg']), score)
	
	return demo_vo2max
	

def get_athlete(age, gender, user_healthscore):
	'''This function uploads athlete data from a file and generates plots comparing the athlete scores to the user's score.'''
	
	athlete_df = pd.read_csv('app/raw_data/athlete_healthscore.csv')
	sports = ['Baseball', 'Basketball', 'Track & Field - Running']

	sch = 'plasma'
	fs = 30	
	for idx, sport in enumerate(sports):
		if gender == 0:
			col = 'Female'
		else:
			col = 'Male'
		labels = ['Pro Baseball Player', 'Pro Basketball Player', 'Pro Track & Field Runner']
		if sport == 'Track & Field - Running':
			if age >= 40:
				athlete = athlete_df[athlete_df['Sport']==sport][col].to_list()[1]
			else:
				athlete = athlete_df[athlete_df['Sport']==sport][col].to_list()[0]
		else:
			athlete = athlete_df[athlete_df['Sport']==sport][col].to_list()[0]
		athlete_min = int(athlete[1:3])
		athlete_max = int(athlete[5:7])
		athlete_score = np.mean([athlete_min, athlete_max])
		source = pd.DataFrame({'a': [0.5, 2], 'b': [user_healthscore, int(athlete_score)], 'x': [-0.8, 5.1], 'y': [0,0], 'label': ['You', labels[idx]]})

		base = alt.Chart(source).encode(alt.Y('b', axis = None, scale = alt.Scale(domain=[0, 70])),alt.X('a:Q', axis=None),color = alt.Color('b').scale(domain=[28, 68], scheme=sch, type='log'),text='b')


		text = alt.Chart(source).encode(x=alt.X('x'),y=alt.Y('y'),color = alt.Color('b', legend=None).scale(scheme=sch),text=alt.Text('label'))

		plot = (base.mark_bar(cornerRadiusTopLeft=20,cornerRadiusTopRight=20,cornerRadiusBottomLeft=20,cornerRadiusBottomRight=20,width = 100) + base.mark_text(align='center', dx=0, dy = -15, fontSize=40) + text.mark_text(dy = -15, fontSize=fs)).configure_view(strokeWidth=0).configure_scale(bandPaddingInner=0).properties(width=500, height=400).save('app/static/assets/img/user_'+sport.lower()+'.png', scale_factor=5.0)

def get_demo(age, gender, user_healthscore):
	
	demo = dict()
	get_athlete(age, gender, user_healthscore)
	demo['sleep'] = get_demo_sleep(age, gender, user_healthscore)
	demo['health'] = get_demo_vo2max(age, gender, user_healthscore)
	
	return demo
	
