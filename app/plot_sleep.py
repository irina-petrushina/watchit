import pandas as pd
import altair as alt

def plot_sleep(user, demo, medical_data):
	
	sleep_df = user.reset_index()
	if len(sleep_df) < 14:
		window = len(sleep_df)
	else:
		window = 14

	sleep_df['Rolling Average'] = sleep_df['value'].rolling(window).mean()

	sleep_df.rename(columns = {'value': 'Your Data'}, inplace=True)

	df_long = sleep_df.melt(id_vars='creationDate', value_vars=
			    ['Your Data', 'Rolling Average'])
	df_long.sample(10, random_state=1)

	medical = pd.DataFrame({'creationDate': [sleep_df['creationDate'][0], sleep_df['creationDate'].iloc[-1]]*2, 'value': [medical_data['sleep'][1], medical_data['sleep'][1], medical_data['sleep'][0],medical_data['sleep'][0]], 'variable': ['Medical Average', 'Medical Average','Medical Average', 'Medical Average']})

	population = pd.DataFrame({'creationDate': [sleep_df['creationDate'][0], sleep_df['creationDate'].iloc[-1]]*2, 'value': [demo['sleep']['sleep_min'], demo['sleep']['sleep_min'], demo['sleep']['sleep_max'],demo['sleep']['sleep_max']], 'variable': ['Population Average', 'Population Average', 'Population Average', 'Population Average']})

	df_long = pd.concat([df_long, medical, population])

	selection = alt.selection_point(fields=['variable'], bind='legend')
	brush = alt.selection_interval(encodings=['x'], clear=False)


	colors = ['#545893', '#1F2344', '#CD5A67', '#DF9657']

	names = ['Your Data', 'Rolling Average', 'Medical Average', 'Population Average']

	scale = alt.Scale(domain=names, range=colors)

	your_data = alt.Chart(df_long[df_long['variable']=='Your Data']).mark_point().encode(alt.X('creationDate:T', axis=alt.Axis(format="%Y %B"), scale=alt.Scale(domain=brush)).title('Date'),\
	alt.Y('value', title=' ').title('Sleep Hours per day'),alt.Color('variable:N', scale=scale, legend=alt.Legend(title=None, labelFontSize=18)),\
	opacity=alt.condition(selection, alt.value(1), alt.value(0.05)),\
	tooltip = [alt.Tooltip('value', title = 'Hours Asleep', format='.1f'),\
		  alt.Tooltip('creationDate:T', title = 'Date')]\
	).properties(\
	height=240,width=600)

	rolling_average = alt.Chart(df_long[df_long['variable']=='Rolling Average']).mark_line().encode(\
	alt.X('creationDate:T', axis=alt.Axis(format="%Y %B")).title('Date'),\
	alt.Y('value', title=' ').title('Sleep Hours per day'),\
	alt.Color('variable:N', scale=scale, legend=alt.Legend(title=None, labelFontSize=18)),\
	opacity=alt.condition(selection, alt.value(1), alt.value(0.05)),\
	tooltip = [alt.Tooltip('value', title = '2-week Average Hours Asleep', format='.1f'),\
		  alt.Tooltip('creationDate:T', title = 'Date')]\
	).properties(\
	height=240,width=600)

	medical_band = alt.Chart(df_long[(df_long['variable']=='Medical Average')]).mark_errorband(extent="ci").encode(\
	alt.X('creationDate:T', axis=alt.Axis(format="%Y %B")).title('Date'),\
	alt.Y('value', title=' ').title('Sleep Hours per day'),\
	alt.Color('variable:N', scale=scale, legend=alt.Legend(title=None, labelFontSize=18)),\
	opacity=alt.condition(selection, alt.value(0.3), alt.value(0)),\
	tooltip=alt.value(None),\
	)

	medical_line = alt.Chart(df_long[(df_long['variable']=='Medical Average')]).mark_line().encode(\
	alt.X('creationDate:T', axis=alt.Axis(format="%Y %B")).title('Date'),\
	alt.Y('value', title=' ', aggregate = 'mean').title('Sleep Hours per day'),\
	alt.Color('variable:N', scale=scale, legend=alt.Legend(title=None, labelFontSize=18)),\
	opacity=alt.condition(selection, alt.value(1), alt.value(0)),\
	)

	population_band = alt.Chart(df_long[(df_long['variable']=='Population Average')]).mark_errorband(extent="ci").encode(\
	alt.X('creationDate:T', axis=alt.Axis(format="%Y %B")).title('Date'),\
	alt.Y('value', title=' ').title('Sleep Hours per day'),\
	alt.Color('variable:N', scale=scale, legend=alt.Legend(title=None, labelFontSize=18)),\
	opacity=alt.condition(selection, alt.value(0.3), alt.value(0)),\
	tooltip=alt.value(None),\
	)

	population_line = alt.Chart(df_long[(df_long['variable']=='Population Average')]).mark_line().encode(\
	alt.X('creationDate:T', axis=alt.Axis(format="%Y %B")).title('Date'),\
	alt.Y('value', title=' ', aggregate = 'mean').title('Sleep Hours per day'),\
	alt.Color('variable:N', scale=scale, legend=alt.Legend(title=None, labelFontSize=18)),\
	opacity=alt.condition(selection, alt.value(1), alt.value(0)),\
	)
	(medical_band+population_band+population_line+medical_line+your_data+rolling_average).add_params(selection).properties(width=900, height=400).configure_axis(labelFontSize=20,titleFontSize=20).add_params(brush).save('app/static/assets/img/user_sleep_trend.json')
