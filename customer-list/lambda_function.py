from datetime import datetime
import psycopg2
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

def get_customer_list_for_company_id(connect, company_id):
    try:
        cursor = connect.cursor()
        cursor.execute(sql_query.GET_CUSTOMER_INFO, (company_id,))
        result = cursor.fetchall()
        return [convert_to_dict(row, field_map.CUSTOMER_INFO) for row in result]
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
        company_id = 2

        customer_list = get_customer_list_for_company_id(connect, company_id)
        
        return {
            'body' : 'Successfully executed.',
            'customer_list_info' : customer_list
        }
    except Exception as exc:
        return {
            'body' : f'An exception occured in Lambda: {exc}'
        }

result = lambda_handler(1,1)
print(result)