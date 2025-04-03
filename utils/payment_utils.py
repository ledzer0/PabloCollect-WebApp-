# utils/payment_utils.py

import requests
from config import TOYYIB_SECRET_KEY, TOYYIB_CATEGORY_CODE, TOYYIB_USER_EMAIL
import time

def create_invoice(user_id, package, amount):
    bill_data = {
        'userSecretKey': TOYYIB_SECRET_KEY,
        'categoryCode': TOYYIB_CATEGORY_CODE,
        'billName': f'{package} Package - PabloCollect',
        'billDescription': f'{package} plan for user {user_id}',
        'billPriceSetting': 1,
        'billPayorInfo': 1,
        'billAmount': str(amount * 100),
        'billReturnUrl': 'https://yourdomain.com',
        'billCallbackUrl': 'https://yourdomain.com/verify-payment',
        'billExternalReferenceNo': str(user_id),
        'billTo': f'User{user_id}',
        'billEmail': TOYYIB_USER_EMAIL,
        'billPhone': '000',
        'billSplitPayment': 0
    }
    res = requests.post('https://dev.toyyibpay.com/index.php/api/createBill', data=bill_data)
    try:
        bill_code = res.json()[0]['BillCode']
        return f'https://toyyibpay.com/{bill_code}'
    except:
        return None

def verify_payment(bill_code, user_id):
    url = f'https://dev.toyyibpay.com/index.php/api/getBillTransactions?billCode={bill_code}'
    res = requests.get(url).json()
    for tx in res:
        if tx.get('billExternalReferenceNo') == str(user_id) and tx.get('transactionStatus') == '1':
            return True
    return False
