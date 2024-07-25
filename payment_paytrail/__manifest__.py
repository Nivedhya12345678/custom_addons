# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Payment Provider: Paytrail',
    'version': '17.0.1.0',
    'depends': ['base','payment'],
    'category': 'Category',
    'author': "Joyal",
    'description': """
    Patrail payment
    """,
    'data': [
        'view/payment_provider_views.xml',
        'view/payment_paytrail_templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
        'data/payment_method.xml',

    ],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_frontend': [

        ],
    },
    'license': 'LGPL-3',
}