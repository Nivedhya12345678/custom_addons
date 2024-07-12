{
    'name': "Remove order lines",
    'version': '17.0.1.0',
    'depends': ['base','point_of_sale' ],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Remove order lines
    """,
    'data': [

    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'remove_order_lines/static/src/xml/pos_order_line_templates.xml',
            'remove_order_lines/static/src/js/remove_orderline.js',
            'remove_order_lines/static/src/xml/pos_clear_button_templates.xml',
            'remove_order_lines/static/src/js/clear_button.js',

       ],
    },
    'license': 'LGPL-3',
}