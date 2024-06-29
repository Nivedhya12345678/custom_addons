# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DynamicSnippets(http.Controller):
    @http.route('/most_sold_products', type='json', auth='public')
    def most_sold(self):
        """Finding most sold products"""
        products = []
        product_search = request.env['product.product'].sudo().search_read(
               [('is_published', '=', True)],
               ['name', 'image_1920', 'sales_count', 'list_price'])
        products = [product for product in product_search if product['sales_count'] != 0]
        products = sorted(products, key=lambda i: i['sales_count'], reverse=True)
        return products

    @http.route('/most_viewed_products', type='json', auth='public')
    def most_viewed(self):
        """Finding most viewed products"""
        product_list = []
        product_search = request.env['product.product'].sudo().search([])
        for product in product_search:
            most_view = request.env['website.track'].sudo().search_count([('url', '=', 'http://localhost:8017'
                                                                    + product.website_url)])
            products = {
                'id': product.id,
                'product': product.name,
                'view_count': most_view,
                'image': product.image_1920,
            }
            product_list.append(products)
        product_list = sorted(product_list, key=lambda i: i['view_count'], reverse=True)
        return product_list
