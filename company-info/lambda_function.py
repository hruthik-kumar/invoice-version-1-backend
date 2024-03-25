from datetime import datetime
import psycopg2
import json
import logging
import sql_query
import field_map

logger = logging.getLogger('company-info')
logger.setLevel(10)

class ExecutionError(Exception):
    "Custome class to raise execution error."

def convert_to_dict(row, keys):
    # Convert each value to a string representation if it's not JSON serializable
    def stringify_value(value):
        if isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, float):
            # Ensure floats are formatted correctly to avoid issues with JSON serialization
            return "{:.2f}".format(value)
        else:
            return str(value)

    # Convert the row tuple into a dictionary
    return {keys[i]: stringify_value(row[i]) for i in range(len(keys))}

def get_company_info_for_company_id(connect, company_id):
    try:
        cursor = connect.cursor()
        cursor.execute(sql_query.GET_COMPANY_INFO, (company_id,))
        result = cursor.fetchone()
        return convert_to_dict(result, field_map.COMPANY_DETAILS)
    except Exception as exc:
        logger.error("Error occured in finding company info: %s", exc)
        raise ExecutionError("An error finding the company info.") from exc

def lambda_handler(event, content):
    try:
        connect = psycopg2.connect(
        host= "localhost",
        dbname = "postgres",
        port= "5432",
        user= "postgres",
        password= "AdminSinga@6530",
        )
        
        # company_id = event['query']['company_id']
        company_id = 1
        
        company_info = get_company_info_for_company_id(connect, company_id)
        
        return {
            'body' : 'Successfully executed.',
            'company_info' : company_info
            
        }
    except Exception as exc:
        return {
            'body' : f'An exception occured in Lambda: {exc}'
        }

result = lambda_handler(1,1)
print(result)