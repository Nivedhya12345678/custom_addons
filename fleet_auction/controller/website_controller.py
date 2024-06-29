# -*- coding: utf-8 -*-
from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route('/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        details = request.env['fleet.auction'].sudo().search([])

        return request.render('fleet_auction.web_form_template', {'details': details})

    @route(['/detail_web_page/<int:id>'], type='http', auth='public', website=True)
    def detail_web_page(self, id):
        print(id)
        auction_details = request.env['fleet.auction'].sudo().browse(id)
        print(auction_details)
        return request.render('fleet_auction.detail_web_page_template', {'auction_detail': auction_details})

    @route('/bid_form/<int:id>', type='http', auth='user', website=True)
    def bid_form(self, id):
        # auction = request.env['fleet.auction'].browse(id)
        users = request.env.user.name

        return request.render('fleet_auction.bid_form_template', {'auction': id, 'user': users})

    @route('/bid_form/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        customer = post.get('customer')
        print("customer", customer)

        customer_id = request.env.user
        print(customer_id)

        request.env['bid.fleet'].sudo().create({
            'auction_id': post.get('name'),
            'customer_id': customer_id.partner_id.id,
            'bid_amount': post.get('amount'),
            'bid_date': post.get('date')
        })
        return request.render('fleet_auction.thank_you_page')
