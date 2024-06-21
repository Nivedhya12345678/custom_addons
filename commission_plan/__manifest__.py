{
    'name': " Crm Commission",
    'version': '17.0.1.0',
    'depends': ['base', 'sale'],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Crm Commission
    """,
    'data': [
        'security/ir.model.access.csv',
        'view/crm_commission_views.xml',
        'view/product_wise_commission_views.xml',
        'view/revenue_wise_commission_views.xml',
        'view/res_users_views.xml',
        'view/sales_team_views.xml',
        'view/sale_order_views.xml',
        'view/crm_commission_menus.xml',




    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}