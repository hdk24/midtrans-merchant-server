import base64

from flask import current_app as app

from app.helpers import is_mobile
from app.helpers.constants import banks, channels


def header_request():
    user_pass = app.config['MIDTRANS_SERVER_KEY'] + ':'
    encoded_u = base64.b64encode(user_pass.encode()).decode()
    auth = 'Basic %s' % encoded_u
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': auth
    }
    return header


def generate_payment(order, customer):
    payment_type = "bank_transfer" if order.payment_method in banks else order.payment_method
    payload = {
        'payment_type': payment_type,
        'transaction_details': {
            'order_id': order.id,
            'gross_amount': order.total_price
        },
        'customer_details': customer,
    }

    # custom va number : https://docs.midtrans.com/en/core-api/advanced-features?id=bank-transfer-va
    # validate va : https://api-docs.midtrans.com/#bank-transfer-object
    if payment_type == "bank_transfer":
        payload['bank_transfer'] = {'bank': order.payment_method, 'va_number': ''}

    elif payment_type == "gopay":
        callback_url = "someapps://callback" if is_mobile() else "https://example.com"
        payload['gopay'] = {'enable_callback': True, 'callback_url': callback_url}

    # todo generate other payment_type
    return payload


def collect_payment_info(resp, order):
    va = None
    generate_qr = None
    deeplink = None
    masked_card = None

    if resp['payment_type'] == 'bank_transfer':
        va = resp['permata_va_number'] if 'permata_va_number' in resp else resp['va_numbers'][0]['va_number']

    elif resp['payment_type'] == 'gopay':
        generate_qr = [x for x in resp['actions'] if x['name'] == 'generate-qr-code'][0]['url']
        deeplink = [x for x in resp['actions'] if x['name'] == 'deeplink-redirect'][0]['url']

    # todo collect other payment_type

    order.va = va
    order.deeplink = deeplink
    order.qr_code = generate_qr
    order.masked_card = masked_card
    order.payment_status = resp['transaction_status']
    return order


def payment_channels():
    # handle transaction fee
    # https://midtrans.com/id/pricing

    for x in channels:
        if x['sysname'] in banks:
            x['payment_type'] = 'bank_transfer'
        elif x['sysname'] == 'gopay':
            x['payment_type'] = 'gopay'
        else:
            x['payment_type'] = None

    for x in channels:
        if x['payment_type'] == 'bank_transfer':
            x['transaction_fee'] = 5000.0
        elif x['payment_type'] == 'gopay':
            x['transaction_fee'] = 0.02
        else:
            x['transaction_fee'] = 0

    # todo transaction fee other payment_type
    return channels
