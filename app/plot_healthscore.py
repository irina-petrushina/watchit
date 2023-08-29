import pandas as pd
import altair as alt

def plot_healthscore_bar(med_score, user_healthscore):
	
	sch = 'plasma'
	fs = 30	
	source = pd.DataFrame({'a': [0.5, 2], 'b': [user_healthscore, med_score], 'x': [-0.8, 5.1], 'y': [0,0], 'label': ['You', 'Medical Average']})

	base = alt.Chart(source).encode(alt.Y('b', axis = None, scale = alt.Scale(domain=[0, 70])),alt.X('a:Q', axis=None),color = alt.Color('b').scale(domain=[28, 68], scheme=sch, type='log'),text='b')


	text = alt.Chart(source).encode(x=alt.X('x'),y=alt.Y('y'),color = alt.Color('b', legend=None).scale(scheme=sch),text=alt.Text('label'))

	plot = (base.mark_bar(cornerRadiusTopLeft=20,cornerRadiusTopRight=20,cornerRadiusBottomLeft=20,cornerRadiusBottomRight=20,width = 100) + base.mark_text(align='center', dx=0, dy = -15, fontSize=40) + text.mark_text(dy = -15, fontSize=fs)).configure_view(strokeWidth=0).configure_scale(bandPaddingInner=0).properties(width=500, height=400).save('app/static/assets/img/user_medical_average.png', scale_factor=5.0)

def plot_healthscore(df, user_healthscore):
	"""This function plots the medical ranges and indicates which range the user's score falls into"""

	df = df.copy()
	df_transp = df.T.reset_index()
	df_transp.columns = ["HealthScore Range", "HealthScoreAbsolute"]
	df_plot = df_transp[(df_transp['HealthScore Range']!='gender')&(df_transp['HealthScore Range']!='Age')]
	df_plot['HealthScore'] = df_plot['HealthScoreAbsolute'].diff().fillna(df_plot['HealthScoreAbsolute'][1])
	df_plot['y'] = 1
	med_score = df_plot[df_plot['HealthScore Range']=='Good']['HealthScoreAbsolute'].iloc[0]
	
	plot_healthscore_bar(med_score, user_healthscore)

	user_df = pd.DataFrame({'x': [user_healthscore, user_healthscore], 'y': [0, 30]})
	user_label = pd.DataFrame({'x': [user_healthscore], 'y': [30]})

	health_width = 100
	sch = 'plasma'
	fs = 30

	base1 = alt.Chart(df_plot[df_plot['HealthScore Range']=='Superior']).encode(x = alt.X('HealthScoreAbsolute',axis=alt.Axis(labelFontSize=fs, domainOpacity=0, gridOpacity = 0, tickOpacity = 0), sort='-x', scale=alt.Scale(domain=(24, 60))).stack(None),color = alt.Color('HealthScore Range', sort = df_plot['HealthScore Range'].to_list()).scale(scheme=sch)).mark_bar(height = health_width)

	base2 = alt.Chart(df_plot[df_plot['HealthScore Range']=='Excellent']).encode(x = alt.X('HealthScoreAbsolute', axis=alt.Axis(labelFontSize=fs, domainOpacity=0, gridOpacity = 0, tickOpacity = 0), sort='-x', scale=alt.Scale(domain=(24, 60))).stack(None),color = alt.Color('HealthScore Range', sort = df_plot['HealthScore Range'].to_list()).scale(scheme=sch)).mark_bar(height = health_width)
	
	base3 = alt.Chart(df_plot[df_plot['HealthScore Range']=='Good']).encode(x = alt.X('HealthScoreAbsolute',axis=alt.Axis(labelFontSize=fs, domainOpacity=0, gridOpacity = 0, tickOpacity = 0), sort='-x', scale=alt.Scale(domain=(24, 60))).stack(None),color = alt.Color('HealthScore Range', sort = df_plot['HealthScore Range'].to_list()).scale(scheme=sch)).mark_bar(height = health_width)

	base4 = alt.Chart(df_plot[df_plot['HealthScore Range']=='Fair']).encode(x = alt.X('HealthScoreAbsolute',axis=alt.Axis(labelFontSize=fs, domainOpacity=0, gridOpacity = 0, tickOpacity = 0), sort='-x', scale=alt.Scale(domain=(24, 60))).stack(None),color = alt.Color('HealthScore Range', sort = df_plot['HealthScore Range'].to_list(), legend=alt.Legend(title="HealthScore Range", titleFontSize = 17, labelFontSize = 20)).scale(scheme=sch),
).mark_bar(height = health_width)

	base5 = alt.Chart(df_plot[df_plot['HealthScore Range']=='Poor']).encode(x = alt.X('HealthScoreAbsolute',axis=alt.Axis(values=[20, 25, 30, 35, 40, 45, 50, 55, 60], labelFontSize=fs, domainOpacity=0, gridOpacity = 0), sort='-x', scale=alt.Scale(domain=(24, 60))).stack(None),color = alt.Color('HealthScore Range', sort = df_plot['HealthScore Range'].to_list()).scale(scheme=sch)).mark_bar(height = health_width)

	base6 = alt.Chart(user_df).encode(x = alt.X('x').title('HealthScore'),y = alt.Y('y',axis = None)).mark_line(color = 'black',strokeWidth = 5 )

	text = alt.Chart(user_label).mark_text(dy = -15, color="black", fontSize=fs).encode(x=alt.X('x'),y=alt.Y('y'),text=alt.Text('x'))


	(base1 + base2 + base3 + base4 + base5 + base6 + text).properties(width=800, height=health_width+30).configure_view(strokeWidth=0).configure_axis(labelFontSize=fs,titleFontSize=fs).save('app/static/assets/img/user_healthscore.json')
