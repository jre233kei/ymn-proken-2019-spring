import estimation_silent

import json

def lambda_handler(event, context):
    result = estimation_silent.main(event['text'])

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
