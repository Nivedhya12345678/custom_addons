{
    'name': "Automated_sale_order",
    'version': '17.0.1.0',
    'depends': ['base','product','sale','stock'],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Automated Sale Order
    """,
    'data': [
        'security/ir.model.access.csv',
        'view/product_template_views.xml',
    
        'wizard/product_template_wizard_views.xml',


    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}



