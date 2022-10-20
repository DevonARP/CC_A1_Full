import json
import boto3

def lambda_handler(event, context):
    
    client = boto3.client('lex-runtime')
    botName = "Concierge"
    botAlias = "ConA"
    userId = "User"
    messages = event['messages'][0]['unstructured']['text']
    
    response = client.post_text(botName = botName, botAlias = botAlias, userId = userId, inputText = messages)
    reply = response['message']
    
    return {
        'statusCode': 200,
        'body': json.dumps(reply),
        'messages': [
                {
                    'type': 'unstructured',
                    'unstructured': {
                        'id': 'string',
                        'text': reply,
                        'timestamp': 'string'
                    }
                }
            ]
        }