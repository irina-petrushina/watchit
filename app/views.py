# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, flash, redirect, url_for
from jinja2  import TemplateNotFound

# App modules
from app import app

# WatchIt modules
from app import get_yelp
from app import watch_data_analysis
#from app import get_medical

ALLOWED_EXTENSIONS = {'xml'}

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path, segment=segment )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None 
# Getting zip and finding local fitness classes
@app.route('/get_zip', methods=['POST']) 
def get_zip():
	zip = request.form.get('zip')
	yelp_request = get_yelp.get_yelp({'user_zip': zip,'health_metric':'both'})
	if yelp_request:
		return render_template('/map_preview.html')
	else:
		return render_template('/map_notfound.html')

# Uploading an Apple Watch file
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get_watch_data', methods=['POST'])
def get_watch_data():
	uploaded_file = request.files['file']
	if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
		uploaded_file.save('user_watch_data.xml')
		flash("Upload succesful!")
		return redirect(url_for("index")+"#tryitnow") 
	elif not allowed_file(uploaded_file.filename):
		flash("Wrong file extension! Please upload an XML file.")
		return redirect(url_for("index")+"#tryitnow")
	else:
		flash("Oops, something went wrong! Try again!")
		return redirect(url_for("index")+"#tryitnow")

# Analyzing uploaded data
@app.route('/analyze')
def analyze_watch_data():
	#user_data = watch_data_analysis.watch_data_analysis('user_watch_data.xml')
	#print(user_data)
	#medical_data = get_medical.get_medical(user_data['user_age'], user_data['user_gender'])
	#print(medical_data)
	return render_template('/result_preview.html')
