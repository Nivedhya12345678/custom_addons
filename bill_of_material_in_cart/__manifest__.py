{
    'name': "Bill of material in cart",
    'version': '17.0.1.0',
    'depends': ['base', 'website','website_sale','mrp',],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Bill of material in cart
    """,
    'data': [
        'view/res_config_settings_views.xml',
        'view/website_sale_cart_views.xml',

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
