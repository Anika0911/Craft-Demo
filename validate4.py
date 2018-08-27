
from flask import *
import os, boto3
from datetime import datetime as dt
import config

app = Flask(__name__)
boto3.set_stream_logger('botocore', level='DEBUG')

@app.route('/')
def index():
	return '''<form method=POST enctype=multipart/form-data action="upload">
	<input type=file name=myfile>
	<input type=submit>
	</form>'''


@app.route('/upload', methods=['POST'])
def upload():
	file1 = request.files['myfile']
	filename = file1.filename
	output = validate_json(uploaded_file)
	#file1.seek(0,0)
	#return redirect(url_for('upload'))
	if output == True:
		s3 = boto3.resource('s3')
		prefix = str(s3_prefix(uploaded_file))
		file1.seek(0,0)
		try:
			s3.Bucket('my-bucket2134').put_object(Key=prefix+'/'+file1.filename, Body=request.files['myfile'], ACL='public-read')
			return "status: 'uploaded', error: """
			# s3.put_object(Bucket = 'my-bucket2134',
		# 			Body = request.files['myfile'],
		# 			Key = '20180405/' )
		except Exception as e:
			print (e)
	else:
		return str(output)

def validate_json(payload_file):
	with open(payload_file) as payload:
		try:
			data = json.load(payload)
			return True
		except Exception as e:
			return "status: 'not uploaded', error: 'not valid json - {}'".format(e)

def s3_prefix(payload_file):
	with open(payload_file) as payload:
		try:
			data = json.load(payload)
			ts = data["ts"]
			up_ts = dt.strptime(ts, '%Y-%m-%d %H:%M')
			new_ts = up_ts.replace(minute=(up_ts.minute)//5*5)
			return (new_ts.strftime('%Y%m%d%H%M'))
		except Exception as e:
			return e

if __name__ == "__main__":
    app.run(debug=True)