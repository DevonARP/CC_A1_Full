#Can start here if you have the file
import requests
import json
import boto3 #This is where the AWS SDK come's into play
from decimal import Decimal #Doesn't accept float types when adding to DynamoDB, so made them decimal instead

un = ''
pw = ''

loc_data = open('rest_data.txt')
loc_data = json.load(loc_data, parse_float=Decimal)

host = 'https://search-restaurants-xcqsrrbhmnrp76v6nuipev2bd4.us-east-1.es.amazonaws.com'
path = '/restaurants/Restaurant/'
region = 'us-east-1'
service= 'es'
credentials = boto3.Session().get_credentials() 
url = host + path

for i in loc_data.keys():
    try:
        loc_data[i]["categories"] = loc_data[i]["categories"][0]['alias']
    except:
        print(i)
loc_data['4LH4igBUSNk7TIH5p1A0pw']["categories"] = 'x'

for i in loc_data.keys():
    id = loc_data[i]["id"]
    cate = loc_data[i]["categories"]
    data = {"id":id,"cuisine":cate}
    r = requests.post(url, auth=(un,pw), json=data)