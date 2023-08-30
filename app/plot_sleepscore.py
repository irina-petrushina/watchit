import pandas as pd
import altair as alt

def plot_sleepscore(sleep_range, user_score):
	"""This function plots the medical ranges and indicates which range the user's score falls into"""

	df = pd.DataFrame({'SleepScore Range': ['Poor', 'Good'], 'SleepScoreAbsolute': sleep_range})
	df['SleepScore'] = df['SleepScoreAbsolute'].diff().fillna(df['SleepScoreAbsolute'][0])
	df['y'] = 1

	user_df = pd.DataFrame({'x': [user_score, user_score], 'y': [0, 30]})
	user_label = pd.DataFrame({'x': [user_score], 'y': [30]})

	health_width = 100
	sch = 'plasma'
	fs = 30

	base1 = alt.Chart(df[df['SleepScore Range']=='Good']).encode(x = alt.X('SleepScoreAbsolute',axis=alt.Axis(labelFontSize=fs, domainOpacity=0, gridOpacity = 0, tickOpacity = 0), sort='-x', scale=alt.Scale(domain=(4, 10))).stack(None),color = alt.Color('SleepScore Range', sort = df['SleepScore Range'].to_list()).scale(scheme=sch)).mark_bar(height = health_width)

	base2 = alt.Chart(df[df['SleepScore Range']=='Poor']).encode(x = alt.X('SleepScoreAbsolute',axis=alt.Axis(values=[4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], labelFontSize=fs, domainOpacity=0, gridOpacity = 0), sort='-x', scale=alt.Scale(domain=(4, 10))).stack(None), color = alt.Color('SleepScore Range', sort = df['SleepScore Range'].to_list(), legend=alt.Legend(title="SleepScore Range", titleFontSize = 17, labelFontSize = 20)).scale(scheme=sch)).mark_bar(height = health_width)

	base3 = alt.Chart(user_df).encode(x = alt.X('x').title('SleepScore'),y = alt.Y('y',axis = None)).mark_line(color = 'black',strokeWidth = 5 )
	text = alt.Chart(user_label).mark_text(dy = -15, color="black", fontSize=fs).encode(x=alt.X('x'),y=alt.Y('y'),text=alt.Text('x'))


	return (base1 + base2 + base3 + text).properties(width=800, height=health_width+30).configure_view(strokeWidth=0).configure_axis(labelFontSize=fs,titleFontSize=fs).to_json()
	#(base1 + base2 + base3 + text).properties(width=800, height=health_width+30).configure_view(strokeWidth=0).configure_axis(labelFontSize=fs,titleFontSize=fs).save('app/static/assets/img/user_sleepscore.json')
