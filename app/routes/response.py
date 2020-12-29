from flask import jsonify

from app.helpers import get_order_stats_str


def make_response(code, message, data):
    status = {'code': code, 'message': message}
    response = jsonify({'status': status, 'data': data})
    response.status_code = code if code != 401 else 400
    return response


def order_response(order):
    response = {
        'id': order.id,
        'status': get_order_stats_str(order.status),
        'total_price': order.total_price,
        'created_at': order.created_at.strftime('%d %B %Y, %H:%M:%S'),
        'updated_at': order.updated_at.strftime('%d %B %Y, %H:%M:%S'),
        'payment_method': order.payment_method,
        'payment_status': order.payment_status,
        'payment_details': {
            'va': order.va,
            'deeplink': order.deeplink,
            'qr-link': order.qr_code
        }
    }
    return response
