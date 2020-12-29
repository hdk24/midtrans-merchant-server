import hashlib
import re
from random import randint

from flask import current_app as app, request
from flask_sqlalchemy import SQLAlchemy

from app.helpers.constants import ORDER_PENDING, ORDER_PAID, ORDER_SENT, ORDER_FAILURE

db = SQLAlchemy()


def random_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def generate_signature(order_id, code, amount):
    # signature logic : SHA512(order_id+status_code+gross_amount+serverkey)
    keys = ''.join([order_id, code, amount, app.config['MIDTRANS_SERVER_KEY']])
    signature = hashlib.sha512(str(keys).encode("utf-8")).hexdigest()
    return signature


def get_order_stats_str(status_id):
    if status_id == ORDER_PENDING:
        return "pending"
    elif status_id == ORDER_PAID:
        return "paid"
    elif status_id == ORDER_SENT:
        return "sent"
    elif status_id == ORDER_FAILURE:
        return "failed"


def is_mobile():
    platform = request.user_agent.platform
    uas = request.user_agent.string
    pattern = r'iPad|iPhone|iPod|Android Mobile|Windows Phone|blackberry|CUPCAKE|webOS|webmate'
    return platform in ['android', 'iphone', 'ipad', 'blackberry'] or re.search(pattern, uas, re.I)
