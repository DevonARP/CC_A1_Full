import requests
import json

#API for Yelp configuration
url = 'https://api.yelp.com/v3/businesses/search'
key = "xMCPPOhtawW-mqIVYt3et1o4jixs_dCsEcGEnfjLsh2BZY8ni46fq3uThs099H47dbY3JRSjkM8jWnssCp5KdsyC_KjlOevPtmJuGrChQgJSjiwYNt7U54aUWhhJY3Yx"
header = {'Authorization': 'Bearer %s' % key}

aws_access_key_id = '' 
aws_secret_access_key = ''

#Filters 
food = ['Italian', 'Mexican', 'French', 'Chinese', 'Indian']

#Grabs the data feom Yelp and makes it into a JSON file
data = [] #Going to be a list of lists of dictionaries
for offset in range(0, 1500, 25):
    for loc in locations:
        for fud in food:
            params = {
                'limit': 25, 
                'location': 'Manhattan',
                'categories': fud,
                'term': 'restaurants',
                'offset': offset, #Get's over 1000 restaurants for each cuisine type
                'radius': 20000
            }
            response = requests.get(url, headers=header, params=params)
            data.append(response.json()['businesses'])
			
end ={} #Making the list of lists of dictionaries a dictionary alone
for i in range(len(data)):
    for j in range(len(data[i])):
        end[data[i][j]['id']] = data[i][j]

with open('rest_data.txt', 'w') as json_file:
  json.dump(end, json_file)
  
#Can start here if you have the file
import requests
import json
from decimal import Decimal #Doesn't accept float types when adding to DynamoDB, so made them decimal instead
loc_data = open('rest_data.txt')
loc_data = json.load(loc_data, parse_float=Decimal)

import boto3 #This is where the AWS SDK come's into play
from datetime import datetime #Update the time it was inserted
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
table = dynamodb.Table('yelp-restaurants')

for i in loc_data.keys(): #Adds the data to DynamoDB
    loc_data[i]["insertedAtTimestamp"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    table.put_item(Item=loc_data[i])