import requests
from flask import request, current_app as app
from flask_restful import Resource
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from app.helpers import random_digits, db
from app.helpers.constants import ORDER_PENDING, customer
from app.helpers.midtrans import generate_payment, header_request, collect_payment_info
from app.models.order import OrderModel
from app.routes.errors import bad_request
from app.routes.response import order_response, make_response


class OrderForm(FlaskForm):
    payment_methods = StringField(validators=[DataRequired()])
    total_price = IntegerField(validators=[DataRequired()])


class OrderActionForm(FlaskForm):
    action = IntegerField(validators=[DataRequired()])


class OrdersAPI(Resource):

    def post(self):
        form = OrderForm.from_json(request.get_json(force=True, silent=True))
        if not form.validate():
            return bad_request("Please complete input form")

        if form.payment_methods.data not in app.config['PAYMENT_METHODS']:
            return bad_request("Invalid payment method")

        # save to db
        order = OrderModel()
        order.id = random_digits(8)
        order.status = ORDER_PENDING
        order.total_price = form.total_price.data
        order.payment_method = form.payment_methods.data

        # do payment
        urls = app.config['MIDTRANS_BASE_URL'] + '/charge'
        payload = generate_payment(order, customer)
        resp = requests.post(url=urls, headers=header_request(), json=payload).json()
        print('charge : ', resp)

        # handle response charge
        if resp['status_code'] == '201':
            payment_info = collect_payment_info(resp, order)
            order.va = payment_info.va
            order.deeplink = payment_info.deeplink
            order.qr_code = payment_info.qr_code

        # save to db
        db.session.add(order)
        db.session.commit()

        return make_response(201, 'created', order_response(order))

    def get(self):
        query = [order_response(x) for x in OrderModel.query.order_by(OrderModel.created_at.desc()).all()]
        return make_response(200, 'success', query)


class OrderAPI(Resource):

    def get(self, id):
        order = OrderModel.query.filter(OrderModel.id == id).first()
        return make_response(200, 'success', order_response(order))
