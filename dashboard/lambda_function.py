import psycopg2
from datetime import datetime
import logging
from datetime import date
import sql_query
import field_map
import psycopg2.extras

logger = logging.getLogger("dashboard")
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
        

def get_dashboard_tile_info(connect):
    try:
        month = date.today().month
        year = date.today().year 
        monthly_revenue = 0
        yearly_revenue = 0
        pending_invoices = 0
        cursor = connect.cursor()
        cursor.execute(sql_query.GET_MONTHLY_REVENUE, (month, year,))
        monthly_revenue = cursor.fetchone()[0]
        monthly_revenue = 0 if monthly_revenue is None else monthly_revenue
        cursor.execute(sql_query.GET_FINANCIAL_YEAR_REVENUE, (year, year, year,))
        yearly_revenue = cursor.fetchone()[0]
        yearly_revenue = 0 if yearly_revenue is None else yearly_revenue
        cursor.execute(sql_query.GET_PENDING_INVOICES)
        pending_invoices = cursor.fetchone()[0]
        pending_invoices = 0 if pending_invoices is None else pending_invoices
        return monthly_revenue, yearly_revenue, pending_invoices
    except Exception as exc:
        logger.error("An error occured finding revenue: %s", exc)
        raise ExecutionError("An error fidning the revenue info.") from exc

def get_invoice_details(connect, company_id):
    try:
        dict_cur = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute(sql_query.GET_RECENT_INVOICE_INFO, (company_id,))
        result = dict_cur.fetchall()
        print(result)
        return [convert_to_dict(row, field_map.INVOICE_FIELDS) for row in result]
    except Exception as exc:
        logger.error("An error occured in finding invoice details: %s",exc)
        raise ExecutionError("An error finding the invoice information.")

def lambda_handler(event, content):
    connect = psycopg2.connect(
        host= "localhost",
        dbname = "postgres",
        port= "5432",
        user= "postgres",
        password= "AdminSinga@6530",
    )
    monthly_revenue, yearly_revenue, pending_invoices = get_dashboard_tile_info(connect)
    recent_invoices = get_invoice_details(connect, 1)
    
    return {
        'statusCode': 200,
        'totalRevenue' : yearly_revenue,
        'monthlyRevenue' : monthly_revenue,
        'pendingInvoices' : pending_invoices,
        'table_data' : {
            'invoices' : recent_invoices
        }
    }
    
result = lambda_handler(1,2)
print(result)