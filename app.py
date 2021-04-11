from flask import Flask, render_template, request
import boto3
from werkzeug.utils import secure_filename
import time as time
from cryptography.fernet import Fernet
import os 
import sys
import k_k

import random
import string

# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

key=k_k.k_k

crypter= Fernet(key)

# import api

# aws_access_key_id = 'AKIAXQGTBX4MY6LCXCPT'
# aws_secret_access_key = '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'

aws_access_key_id= crypter.decrypt(b'gAAAAABgcQ1ThmY2Fk_w-xGqHKe4M85mqUf_MdmPPculibZVX1KoXYocFE8mSaWOsD3yNMSfZqKp3CBKTCUXl12kZjncqF9MOWdFST0FuJSACD9fuAyWwdk=')
aws_access_key_id=aws_access_key_id.decode("utf-8")

aws_secret_access_key= crypter.decrypt(b'gAAAAABgcQ1TS0TxsuofiAy4rvTzpHoqiWqyXVcEYwMPIW6cYctcOlX-AcspApcq1a_40968jUiX69aBLRmMSdMat1anRQrXd_YKs9QTqhp53lc5FpY7GFBAk1WDsjVeWqgmEAToGzcN')
aws_secret_access_key=aws_secret_access_key.decode("utf-8")



application= app = Flask(__name__)





# aws_access_key_id='12323'
# aws_secret_access_key= ''


s3 = boto3.resource('s3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key= aws_secret_access_key,
                    # aws_session_token=keys.AWS_SESSION_TOKEN
                     )

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name='us-east-1')





BUCKET_NAME='transcriberbucket2'
# BUCKET_NAME='transcriber2.0bucket'

@app.route('/')  
def home():

    return render_template("file_upload_to_s3.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        #loading and saving the mp3 file locally as a variable mp3 (we have loaded it but havent uploaded it to s3 yet)
        mp3 = request.files['file']
        email=request.form['email']
        speakers=request.form['speaker']

        speakers=str(speakers)+str('-')

        # res = make_response(jsonify({"message": "File uploaded"}), 200)



        # time=time.ctime()

# #         # USED FOR CREATING THE TABLE INITIALLY
#         table = dynamodb.create_table(
#     TableName='newtable',
#     KeySchema=[
#         {
#             'AttributeName': 'email',
#             'KeyType': 'HASH'
#         }
         
#     ],
#     AttributeDefinitions=[
#              {
#             'AttributeName': 'time',
#             'AttributeType': 'S',

#             'AttributeName': 'time-number',
#             'AttributeType': 'S',

#             'AttributeName': 'email',
#             'AttributeType': 'S',

#         } 
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 1,
#         'WriteCapacityUnits': 1,
#     }

# )
        # table = dynamodb.Table('newtable')
        # Wait until the table exists.
        # table.meta.client.get_waiter('table_exists').wait(TableName='newtable')

        # IPopulating the table created with users input
        table = dynamodb.Table('newtable')
        
        table.put_item(
                Item={
        
        'email': email,
        'date': time.ctime(),
        'time-number': str(time.time()),
        
            }
        )


        



        #Put the stipe payment here:
        #ONLY if the stripe payment is 'successful' upload the mp3 to the s3 bucket which will trigger the lambda func.
        
        # hence the upload successfull should come before uploading to s3.
        #Need to create a 'payment successful your file is being transcribed' once the payment is successful 
        #(somehow get a message through some api )
        

        #also need to create a fixed linear function for charging the rate. 

        if mp3:
                letters = string.ascii_lowercase
                rand_letter=''.join(random.choice(letters) for i in range(10))

                filename = secure_filename(mp3.filename)
                filename=speakers+rand_letter[0]+filename
                mp3.save(filename)
                s3.meta.client.upload_file(filename, BUCKET_NAME, 'mp3_files/%s' % (filename))
                # s3.upload_file(
                #     Bucket = BUCKET_NAME,
                #     Filename=filename,
                #     Key = filename
                # )
                msg= 'Upload Done! Your file is being proccessed and will be emailed to you shortly'


        


    return render_template("file_upload_to_s3.html",msg =msg)





if __name__ == "__main__":
    
    app.run( host="0.0.0.0",
    port=5000, debug=True)
