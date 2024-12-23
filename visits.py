import json
import boto3
from datetime import datetime

# DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = "WebpageVisitData"  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    action = event.get("queryStringParameters", {}).get("action")
    
    if action == "register":
        return register_visit()
    elif action == "get_data":
        return get_visit_data()
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid action"})
        }

def register_visit():
    # Current timestamp
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    # Register a visit
    table.put_item(Item={"timestamp": timestamp, "count": 1})
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Visit registered", "timestamp": timestamp})
    }

def get_visit_data():
    # Scan the table to retrieve all records
    response = table.scan()
    items = response.get("Items", [])
    
    # Process data for analytics
    data = {}
    for item in items:
        date = item["timestamp"].split(" ")[0]  # Group by date
        data[date] = data.get(date, 0) + item["count"]
    
    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
