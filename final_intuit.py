from flask import *
import os, boto3
from datetime import datetime as dt
import config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024 # for 5GB max-limit.
boto3.set_stream_logger('botocore', level='DEBUG')

#Setting the Context Root
@app.route('/')
def index():
        return render_template('index.html')

# Uploading the file to S3
@app.route('/upload', methods=['POST'])
def upload():

        in_file = request.files['myfile']

        # Making sure that file is passed in curl
        if in_file.filename == "":
            return "Please select a file"

        file_name = in_file.filename
        blob = in_file.read()
        
        # file_size = len(blob)
        # if file_size>10*1025*1024*1024:
        #     print ("Alert! Big file")

        #Calling methon to validate payload
        output, prefix = validate_payload(blob)
        in_file.seek(0,0)

        if in_file and output == True:
                s3 = boto3.resource('s3')
                try:
                        print ("Uploading ....")
                        s3.Bucket('my-bucket2134').put_object(Key=prefix+'/'+file_name, Body=request.files['myfile'], ACL='public-read')
                        return "status: 'uploaded', error: ''\n"

                except Exception as e:
                        return "status: 'not uploaded', error: {}\n".format(e)
        else:
                return str(prefix)


#Validating the payload that it should be valid json and contains "ts" field in correct time format
def validate_payload(payload_file):
    try:
        data = json.loads(payload_file)
        ts = data["ts"]
        up_ts = dt.strptime(ts, '%Y-%m-%d %H:%M')
        new_ts = up_ts.replace(minute=(up_ts.minute)//5*5)
        return (True, new_ts.strftime('%Y%m%d%H%M'))
    except Exception as e:
        return (False, "status: 'not uploaded', error: 'not valid json {}'\n".format(e))


if __name__ == "__main__":
    app.run(debug=True)