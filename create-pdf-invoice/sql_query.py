GET_INVOICE_DETAILS = """SELECT T2.COMPANY_REGISTERED_NAME,
        T2.COMPANY_ADDRESS,
        T2.COMPANY_GST_NO,
        T1.INVOICE_NUMBER,
        T1.INVOICE_DATE,
        T3.CUSTOMER_COMPANY_NAME,
        T3.CUSTOMER_COMPANY_ADDRESS,
        T3.CUSTOMER_COMPANY_GST,
        T1.DC_NUMBER,
        T1.PURCHASE_ORDER_NUMBER,
        T1.DC_DATE,
        T4.ACCOUNT_NUMBER,
        T4.IFSC_CODE,
        T4.BANK_NAME,
        T4.ACCOUNT_BRANCH
    FROM INVOICE_T AS T1
    LEFT JOIN COMPANY_INFO_T AS T2 ON T1.COMPANY_ID = T2.COMPANY_ID
    LEFT JOIN CUSTOMER_INFO_T AS T3 ON T1.CUSTOMER_ID = T3.CUSTOMER_ID
    LEFT JOIN COMPANY_REGISTERED_BANK AS T4 ON T1.COMPANY_ID = T4.COMPANY_ID
    WHERE T1.INVOICE_ID = %s;"""

GET_PRODUCT_FOR_INVOICE_ID = """SELECT P.*
    FROM INVOICE_T I
    JOIN PRODUCT_INFO_T P ON P.PRODUCT_ID = ANY(I.PRODUCT_IDS)
    WHERE I.INVOICE_ID = 2;"""