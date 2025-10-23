import json
import boto3
import time

athena = boto3.client("athena")

# set your Athena workgroup and query output bucket
WORKGROUP = "primary"   # or your custom workgroup
S3_OUTPUT = "s3://cafe-intelligence-system/"

def lambda_handler(event, context):
    # query = "SELECT * FROM cafe_intelligence_system LIMIT 10;"  # simple select
    query = event['requestBody']['content']['application/json']['properties'][0]['value']
    
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            "Database": "cafe-intelligence-system-db"   # 👈 your Glue/Athena DB
        },
        ResultConfiguration={
            "OutputLocation": S3_OUTPUT
        },
        WorkGroup=WORKGROUP
    )
    
    query_execution_id = response["QueryExecutionId"]
    
    # wait until query finishes
    while True:
        status = athena.get_query_execution(QueryExecutionId=query_execution_id)
        state = status["QueryExecution"]["Status"]["State"]
        
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(1)
    
    if state == "SUCCEEDED":
        result = athena.get_query_results(QueryExecutionId=query_execution_id)
        rows = []
        
        # skip first row (column headers)
        for row in result["ResultSet"]["Rows"][1:]:
            values = [col.get("VarCharValue", "") for col in row["Data"]]
            rows.append(values)
        
        data = {
            "status": "success",
            "columns": [col.get("VarCharValue", "") for col in result["ResultSet"]["Rows"][0]['Data']],
            "rows": rows,
            "agent_event_debug": str(event)
        }
        return api_response(event, data)
    else:
        return {
            "status": "error",
            "message": f"Athena query failed with state {state}"
        }

def api_response(event, data):
    agent = event['agent']
    actionGroup = event['actionGroup']
    api_path = event['apiPath']
    # get parameters
    get_parameters = event.get('parameters', [])
    # post parameters
    post_parameters = event['requestBody']['content']['application/json']['properties']
    response_body = {
        'application/json': {
            'body': str(data)
        }
    }
    
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    api_response = {
        'messageVersion': '1.0', 
        'response': action_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
        
    return api_response