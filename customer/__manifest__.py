{
    'name': "customer",
    'version': '17.0.1.0',
    'depends': ['base', 'sale', 'contacts'],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Customer
    """,
    'data': [
        'view/res_partner_views.xml',
        'view/product_product_views.xml',

    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
