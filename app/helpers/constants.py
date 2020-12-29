# string template
TRANSACTION_ID = '%(order_id)d%(timestamp)d'

# status code
ORDER_PENDING = 1
ORDER_PAID = 2
ORDER_SENT = 3
ORDER_FAILURE = 4

customer = {
    "email": "user_test@example.com",
    "first_name": "user",
    "last_name": "test",
    "phone": "+628112341234"
}

payment_type = [
    'credit_card',
    'bank_transfer',
    'echannel',
    'bca_klikpay',
    'bca_klikbca',
    'bri_epay',
    'cimb_clicks',
    'danamon_online',
    'cstore',
    'akulaku',
    'gopay',
]

banks = [
    'permata',
    'bca',
    'bri',
    'bni',
]

channels = [
    {
        'name': 'GoPay',
        'sysname': 'gopay'
    },
    {
        'name': 'Permata Virtual Account',
        'sysname': 'permata'
    },
    {
        'name': 'BNI Virtual Account',
        'sysname': 'bni'
    },
    {
        'name': 'BRI Virtual Account',
        'sysname': 'bri'
    },
    {
        'name': 'BCA Virtual Account',
        'sysname': 'bca'
    },
    {
        'name': 'Credit Card',
        'sysname': 'credit_card'
    }
]
