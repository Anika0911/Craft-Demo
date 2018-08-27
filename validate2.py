#from flask import Flask, request
from flask import *
import os
from werkzeug import secure_filename
from datetime import datetime as dt

UPLOAD_FOLDER = '/Users/anikarathi/Documents'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024 # for 5GB max-limit.

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
	in_file = request.files['myfile']
	#print (dir(in_file))
	blob = in_file.read()
	file_size = len(blob)
	if file_size>10 :
		print ("Alert! Big file")
	filename = in_file.filename
	output = validate_json(blob)
	#return redirect(url_for('upload'))
	return str(output)

def validate_json(payload_file):
	try:
		data = json.loads(payload_file)
		ts = data["ts"]
		up_ts = dt.strptime(ts, '%Y-%m-%d %H:%M')
		new_ts = up_ts.replace(minute=(up_ts.minute)//5*5)
		return (new_ts.strftime('%Y%m%d%H%M'))
	except Exception as e:
		return 'Invalid Payload\n',e

if __name__ == "__main__":
    app.run(debug=True)