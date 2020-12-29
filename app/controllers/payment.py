import requests
from flask import request, current_app as app
from flask_restful import Resource

from app.helpers import generate_signature, ORDER_PAID, db, ORDER_PENDING, ORDER_FAILURE
from app.helpers.midtrans import payment_channels, header_request
from app.models.order import OrderModel
from app.routes.errors import unauthorized, make_response


class PaymentChannelAPI(Resource):
    def get(self):
        results = [x for x in payment_channels() if x['sysname'] in app.config['PAYMENT_METHODS']]
        return make_response(200, 'success', results)


class PaymentNotificationAPI(Resource):
    # call from midtrans
    # https://api-docs.midtrans.com/#best-practice-to-handle-notification

    def post(self):
        # incoming data from midtrans
        data = request.get_json(force=True, silent=True)

        # verify signature
        signature = generate_signature(
            data['order_id'], data['status_code'], data['gross_amount']
        )
        print(signature)

        if signature != data['signature_key']:
            return unauthorized()

        # get status payment every get notification
        urls = app.config['MIDTRANS_BASE_URL'] + '/%s/status' % data['order_id']
        resp = requests.get(url=urls, headers=header_request()).json()
        print(resp)

        order = OrderModel.query.filter(OrderModel.id == resp['order_id']).first()
        order.payment_status = resp['transaction_status']

        # handling notifications:
        # https://docs.midtrans.com/en/after-payment/http-notification?id=example-on-handling-http-notifications
        if resp['transaction_status'] == "settlement" or (
                resp['transaction_status'] == "capture" and resp['fraud_status'] == "accept"):
            order.status = ORDER_PAID
        elif resp['transaction_status'] == "pending":
            order.status = ORDER_PENDING
        else:
            order.status = ORDER_FAILURE

        db.session.commit()

        # always return 200
        # https://docs.midtrans.com/en/after-payment/http-notification?id=responding-http-notification-from-midtrans
        return make_response(200, 'success', {})


class PaymentStatusAPI(Resource):
    def get(self, id):
        urls = app.config['MIDTRANS_BASE_URL'] + '/%s/status' % id
        resp = requests.get(url=urls, headers=header_request()).json()
        return resp
