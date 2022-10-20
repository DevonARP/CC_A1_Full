import json
import boto3
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection

aws_access_key_id = '' 
aws_secret_access_key = ''

def lambda_handler(event, context):
    #Getting message from queue
    sqs = boto3.resource('sqs', region_name = 'us-east-1', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    queue = sqs.get_queue_by_name(QueueName = 'A1P3')
    response = queue.receive_messages(MaxNumberOfMessages = 1)
    values = response[0].body.split(',')
    Neighborhoods = values[0]
    Time = values[1]
    Cuisine = values[2]
    NOP = values[3]
    Contact = values[4]
    response[0].delete()

    #Connecting to ES
    host = 'search-restaurants-xcqsrrbhmnrp76v6nuipev2bd4.us-east-1.es.amazonaws.com' #I spent too much time not realizing the https:// is the problem
    path = '/restaurants/Restaurant/'
    region = 'us-east-1'
    service= 'es'
    session = boto3.Session(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region, service)
    client = OpenSearch(hosts = [{'host': host, 'port': 443}], http_auth = awsauth, use_ssl = True, verify_certs = True, connection_class = RequestsHttpConnection)

    #Query to get restuarants with the mentioned cuisine
    query = client.search(index="restaurants", 
                        body = {
                        "query":{
                            "match":{
                                    "cuisine": Cuisine[13:len(Cuisine)-1]
                            }
                        }})
    hits=query['hits']['hits']

    import random
    chosen = hits[random.randrange(0,len(hits))]

    chosen['_source']['id']

    #Grabbing data from DynamoDB
    rest = []
    dynamodb = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    grab_data = dynamodb.get_item(TableName = 'yelp-restaurants', Key = {'id' :{'S':chosen['_source']['id']}}) #Has to be a dict, the S is for string
    rest.append(grab_data)

    #Formatting data
    message = 'Hi, here is my ' + Cuisine[13:len(Cuisine)-1] + ' food reccomednation for ' +  NOP[20:len(NOP)-1] + ' person(s) in ' + Neighborhoods[20:len(Neighborhoods)-1] + ' at ' + Time[10:len(Time)-1] + ': '
    x = grab_data['Item']['location']['M']['display_address']['L'][0]['S']
    y = grab_data['Item']['location']['M']['display_address']['L'][1]['S']
    endresponse = grab_data['Item']['alias']['S'] +' located at ' + x + ' ' + y

    #Sending to user
    ses_client = boto3.client("ses", region_name="us-east-1", aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    ses_response = ses_client.verify_email_identity(EmailAddress = Contact[13:len(Contact)-3])
    ses_client.send_email(Source = 'ap5254@nyu.edu', Destination = {'ToAddresses': [Contact[13:len(Contact)-3]]}, 
                        Message = {'Subject': {'Data': 'Food Recommendation'}, 
                                    'Body' : { 'Text' : { 'Data' : message + endresponse}}})