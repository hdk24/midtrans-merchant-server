from flask import Blueprint
from flask_restful import Api

from app.controllers.orders import OrderAPI, OrdersAPI
from app.controllers.payment import PaymentChannelAPI, PaymentNotificationAPI, PaymentStatusAPI

v1 = Blueprint('api.v1', __name__)
api = Api(v1)

resources = (
    (PaymentChannelAPI, '/payment/channels',
     dict(methods=['GET'], endpoint='channels')),

    (OrdersAPI, '/orders',
     dict(methods=['POST', 'GET'], endpoint='orders')),

    (OrderAPI, '/order/<int:id>',
     dict(methods=['GET'], endpoint='order')),

    (PaymentNotificationAPI, '/payment/notifications',
     dict(methods=['POST'], endpoint='notifications')),

    (PaymentStatusAPI, '/payment/<int:id>/status',
     dict(methods=['GET'], endpoint='status')),
)

# add resource to api
for r in resources:
    api.add_resource(r[0], r[1], **r[2])
