{
    'name': "Most view and most sold product",
    'version': '17.0.1.0',
    'depends': ['base', 'website', 'sale'],
    'author': "Joyal",
    'category': 'Category',
    'description': """
    Most view and most sold product
    """,
    'data': [
        'view/most_sold_template_views.xml',
        'view/most_view_template_views.xml',
        'view/website_snippet_views.xml',
    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_frontend': [
            'most_view_most_sold_products/static/src/js/most_sold.js',
            'most_view_most_sold_products/static/src/js/most_viewed.js',
            'most_view_most_sold_products/static/src/xml/most_sold_snippet_templates.xml',
            'most_view_most_sold_products/static/src/xml/most_view_snippet_templates.xml',
       ],
    },
    'license': 'LGPL-3',
}
