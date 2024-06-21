{
    'name': "Fleet_Auction",
    'version': '17.0.6.0',
    'depends': ['base','fleet','mail', 'contacts', 'account','website'],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Fleet Auction
    """,
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',

        'data/fleet_auction_sequence.xml',
        'data/fleet_product.xml',
        'data/email_template.xml',
        'data/ir_cron_data.xml',
        'data/fleet_cancel_reason_data.xml',

        'wizard/fleet_cancel_wizard_views.xml',
        'wizard/fleet_auction_wizard_views.xml',

        'view/fleet_auction_views.xml',
        'view/bid_fleet_views.xml',
        'view/confirmed_bid_views.xml',
        'view/fleet_expense_views.xml',
        'view/fleet_account_move_views.xml',
        'view/fleet_cancel_reason_views.xml',
        'view/fleet_auction_menus.xml',
        'view/fleet_auction_website_menu.xml',
        'view/website_template_views.xml',
        'view/auction_details_template.xml',
        'view/bid_form_template.xml',

        'report/fleet_auction_report.xml',
        'report/fleet_auction_report_template.xml',
        'report/report_paper_format.xml',

    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'fleet_auction/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'fleet_auction/static/src/css/website_fleet_auction.css',
            'fleet_auction/static/src/js/bid_form.js',
        ],
    },
    'license': 'LGPL-3',
}

