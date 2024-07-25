{
    'name': "Stock report",
    'version': '17.0.1.0',
    'depends': ['base','stock','web' ],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Stock report
    """,
    'data': [
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'data/ir_cron_data.xml',

        'report/stock_report.xml',
        'report/stock_report_template.xml',

        'wizard/stock_report_wizard_views.xml',

    ],
    'demo': [

    ],
    'application': True,
    'installable': True,

    'license': 'LGPL-3',
}