import configparser, boto3, os, time, json
from pprint import pprint

bucket_name = 'yohanesgultom-transcribe-test'
file_path = '/home/yohanesgultom/Downloads/Pidato-Kenegaraan-Presiden-Joko-Widodo-2019-Part-1.mp3'
# source: Pidato Kenegaraan Presiden Joko Widodo (2:21-3:42) https://www.youtube.com/watch?v=yDdQ9pEfcnw&t=155s

config = configparser.ConfigParser()        
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aws.conf'))

# init AWS session
session = boto3.session.Session(
    aws_access_key_id=config['default']['aws_access_key_id'], 
    aws_secret_access_key=config['default']['aws_secret_access_key'],
    region_name=config['default']['region']
)
s3 = session.client('s3')
transcribe = session.client('transcribe')

# create bucket to store transcribe input/output file if not exists
res = s3.list_buckets()
buckets = [b['Name'] for b in res['Buckets']]
if bucket_name not in buckets:
    print(f'Creating new bucket: {bucket_name}...')
    res = s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': session.region_name}
    )

# upload audio input file if not exist
file_name = os.path.basename(file_path)
res = s3.list_objects(Bucket=bucket_name)
contents = res['Contents'] if 'Contents' in res else []
file_names = [c['Key'] for c in contents]
if file_name not in file_names:
    print(f'Uploading input file: {file_name}...')
    res = s3.upload_file(file_path, bucket_name, file_name)

# create new job if not exist
res = transcribe.list_transcription_jobs()
job_name = file_name
jobs = [j['TranscriptionJobName'] for j in res['TranscriptionJobSummaries']]
if job_name not in jobs:
    print(f'Starting transcribe job: {job_name}...')
    s3_file = f's3://{bucket_name}/{file_name}'
    res = transcribe.start_transcription_job(
        TranscriptionJobName=job_name, 
        LanguageCode='id-ID', 
        Media={'MediaFileUri': s3_file}, 
        OutputBucketName=bucket_name
    )

# wait until job to complete
completed = False
while not completed:
    res = transcribe.list_transcription_jobs(
        JobNameContains=job_name, 
        MaxResults=1
    )  
    if 'TranscriptionJobSummaries' in res:
        if len(res['TranscriptionJobSummaries']) > 0:
            job = res['TranscriptionJobSummaries'][0]
            completed = job['TranscriptionJobStatus'] == 'COMPLETED'
            print(f'Job has completed')
    if not completed:
        print(f'Waiting for job to complete...')
        time.sleep(5)

# download transcription result        
result_file = f'{file_name}.json'
if completed and not os.path.isfile(result_file):
    res = s3.list_objects(Bucket=bucket_name)
    contents = res['Contents'] if 'Contents' in res else []
    for c in contents:
        content_name = c['Key']
        if content_name == result_file:
            print(f'Downloading transcription result...')
            s3.download_file(bucket_name, content_name, content_name)
            print(f'File downloaded {content_name}')

# print transcription result
if os.path.isfile(result_file):
    with open(result_file, 'r') as f:
        res_file = json.load(f)
        print(res_file['results']['transcripts'][0]['transcript'])
backup_email.py
'''
Run mysqldump gzip and send result using SMTP
Reference: https://realpython.com/python-send-email
Config example:
{
    "subject" : "Daily backup",
    "body" : "This is a daily database backup",
    "sender_email" : "sender@gmail.com",
    "receiver_email" : "receiver@gmail.com",
    "password" : "supersecretpassword",
    "smtp_server" : "smtp.gmail.com",
    "smtp_host" : 465,
    "dbname" : "dbname",
    "file_prefix": "dbname_backup"
}
@Author yohanes.gultom@gmail.com
'''

import email, smtplib, ssl
import datetime
import subprocess
import shlex
import json
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CONFIG_FILE = 'backup_email.json'

with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

subject = config['subject']
body = config['body']
sender_email = config['sender_email']
receiver_email = config['receiver_email']
password = config['password']
smtp_server = config['smtp_server']
smtp_host = config['smtp_host']
dbname = config['dbname']
file_prefix = config['file_prefix']

cmd1 = "mysqldump {}".format(dbname)
cmd2 = "gzip -9"
filename = "{}_{}.sql.gz".format(file_prefix, datetime.datetime.now().strftime('%Y%m%d%H%M'))

# Backup database
print('Backing up database..')
with open(filename, 'w') as f:
    ps1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE)
    ps2 = subprocess.Popen(shlex.split(cmd2), stdin=ps1.stdout, stdout=f)
    ps1.wait()
    ps2.wait()
    if ps2.returncode == 2:
        exit(1)

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
print('Sending email..')
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, smtp_host, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)

print('Done.')
