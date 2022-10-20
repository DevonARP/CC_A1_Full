import boto3
import json

def lambda_handler(event, context):
    
    intent = event["currentIntent"]["name"]

    if intent == "GreetingIntent":
        
        Name = event["currentIntent"]["slots"]["Name"]
        
        response =  {
                            "dialogAction":
                            {
                                "fulfillmentState":"Fulfilled",
                                "type":"Close",
                                "message":
                                    {
                                        "contentType":"PlainText",
                                        "content": "Hi " + Name + ", how can I help you today?"
                                    }
                            }
                    }
        return response

    if intent == "DiningSuggestionsIntent":
        
        Neighborhoods = event["currentIntent"]["slots"]["Neighborhoods"]
        Time = event["currentIntent"]["slots"]["Time"]
        Cuisine = event["currentIntent"]["slots"]["Cuisine"]
        NOP = event["currentIntent"]["slots"]["NumberOfPeople"]
        Contact = event["currentIntent"]["slots"]["Contact"]
        
        data = [
            {
                "Neighborhoods" : Neighborhoods, 
                "Time" : Time, 
                "Cuisine" : Cuisine, 
                "NumberOfPeople" : NOP, 
                "Contact" : Contact
            }
            ]
        
        response =  {
                            "dialogAction":
                            {
                                "fulfillmentState":"Fulfilled",
                                "type":"Close",
                                "message":
                                    {
                                        "contentType":"PlainText",
                                        "content": "Review: " + NOP + " person(s) for " + Time + " in " + Neighborhoods + " for " + Cuisine + " food with contact email: " + Contact + ". Please respond with 'Correct' if that's correct."
                                    }
                            }
                    }
        
        client = boto3.client("sqs")
        resforsqs = client.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/411926377614/A1P3", 
        MessageBody=json.dumps(data))
        
        return response
        
    if intent == "ThankYouIntent":

        response =  {
                            "dialogAction":
                            {
                                "fulfillmentState":"Fulfilled",
                                "type":"Close",
                                "message":
                                    {
                                        "contentType":"PlainText",
                                        "content": "We have received and confimed your request and we'll send you a list of reccomendations soon. Thank you and enjoy!"
                                    }
                            }
                    }
        return response