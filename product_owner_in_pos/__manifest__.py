{
    'name': "Product owner in pos",
    'version': '17.0.1.0',
    'depends': ['base','point_of_sale' ],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Product owner in pos
    """,
    'data': [
        'view/product_product_views.xml',

    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'product_owner_in_pos/static/src/js/pos_session.js',
            'product_owner_in_pos/static/src/xml/pos_order_line_templates.xml',

       ],
    },
    'license': 'LGPL-3',
}