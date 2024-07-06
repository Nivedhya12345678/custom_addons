{
    'name': "Disable delivery",
    'version': '17.0.1.0',
    'depends': ['base', 'sale','stock'],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Disable delivery
    """,
    'data': [
        'view/sale_order_views.xml',
        'view/hide_button_views.xml',
    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_frontend': [

       ],
    },
    'license': 'LGPL-3',
}
