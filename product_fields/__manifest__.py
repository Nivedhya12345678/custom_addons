{
    'name': "Product Fields",
    'version': '17.0.1.0',
    'depends': ['base', 'product', 'sale', 'contacts'],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Product Fields
    """,
    'data': [
        'security/ir.model.access.csv',
        'view/product_views.xml',
        'view/res_partner_views.xml',
        'view/sale_order_views.xml',


    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
