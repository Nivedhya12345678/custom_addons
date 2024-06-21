{
    'name': "Employee Level",
    'version': '17.0.1.0',
    'depends': ['base','contacts','hr',],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Employee Level
    """,
    'data': [
        'security/ir.model.access.csv',
        'view/employee_level_views.xml',
        'view/hr_employee_views.xml',
        'view/employee_level_menus.xml',


    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}