import requests
import os, glob
from dotenv import load_dotenv
import altair as alt
import pandas as pd
import folium
#from IPython.display import display
from folium.plugins import MarkerCluster

def get_yelp(data):
	"""Takes user data in format of a dictionary that has two fields user_zip and health_metric (which classes to look for)"""

	load_dotenv()
	token = os.getenv("YELP_API_TOKEN")
	if token is not None:
		headers = {'Authorization': "Bearer {}".format(token)}   
	else:
		headers = None 

	API_HOST = 'https://api.yelp.com'
	BUSINESS_PATH = '/v3/businesses/search'

	sleep_filters = ['meditation', 'yoga', 'stretching']
	cardio_filters = ['cycling','hiit','boxing','cardio']


	if data['health_metric'] == 'both':
		user_filters = [sleep_filters, cardio_filters]
	elif data['health_metric'] == 'sleep':
		user_filters = [sleep_filters]
	else:
		user_filters = [cardio_filters]

	url = API_HOST+BUSINESS_PATH

	params = {'location': data['user_zip'], 
	  'term': 'gym', 
	  'filter': user_filters, 
	  'sort_by': 'best_match'}


	response = requests.get(url, params=params, headers=headers)
	
	if not response:
		return False
	else:
		name = []
		long = []
		lat = []
		stars = []
		link = []
		for bus in response.json()['businesses']:
			name.append(bus['name'])
			long.append(bus['coordinates']['longitude'])
			lat.append(bus['coordinates']['latitude'])
			stars.append(bus['rating'])
			link.append(bus['url'])
		
		df = pd.DataFrame({'business_name': name, 'longitude': long, 'latitude': lat, 'rating': stars, 'link': link})
		
		fit_map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], 
				     zoom_start=13, tiles=None)
		folium.raster_layers.TileLayer(tiles='cartodbpositron', name='''<b style="font-size: 14px;"> Customer Rating: </b> ''').add_to(fit_map)

		mCluster_5 = MarkerCluster(name='''<b style="font-size: 14px"> &#9733 &#9733 &#9733 &#9733 &#9733 </b> ''').add_to(fit_map)
		mCluster_4 = MarkerCluster(name='''<b style="font-size: 14px;"> &#9733 &#9733 &#9733 &#9733 &#9734 </b> ''').add_to(fit_map)
		mCluster_3 = MarkerCluster(name='''<b style="font-size: 14px;"> &#9733 &#9733 &#9733 &#9734 &#9734 </b> ''').add_to(fit_map)
		mCluster_2 = MarkerCluster(name='''<b style="font-size: 14px;"> &#9733 &#9733 &#9734 &#9734 &#9734 </b> ''').add_to(fit_map)
		mCluster_1 = MarkerCluster(name='''<b style="font-size: 14px;"> &#9733 &#9734 &#9734 &#9734 &#9734 </b> ''').add_to(fit_map)

		for lat, lon, name, stars, link in zip(df['latitude'], df['longitude'], df['business_name'], df['rating'], df['link']):

			location = [lat, lon]

			html = '''<p style="font-size: 14px;"> <b> Gym: </b>  <a href="{link}">{name}</a> </p> <p style="font-size: 14px;"> <b> Rating: </b> {rating} </p>'''.format(name=name, link = link, rating=stars)

			marker = folium.Marker(location=location, radius=10, popup = folium.Popup(html, parse_html=False, max_width=500),fillColor='b', fill=True, fill_opacity=0.7)

			if stars >= 5:
				mCluster_5.add_child(marker)
			elif stars >= 4:
				mCluster_4.add_child(marker)
			elif stars >= 3:
				mCluster_3.add_child(marker)  
			elif stars >= 2:
				mCluster_2.add_child(marker)  
			else:
				mCluster_1.add_child(marker) 
		
		
		folium.LayerControl(collapsed = False).add_to(fit_map);
		    
		#print(glob.glob("app/static/assets/img/*.*"))
		#fit_map.save("app/static/assets/img/fit_map.html")
		return fit_map.get_root()._repr_html_()	
