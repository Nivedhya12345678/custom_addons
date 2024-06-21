from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route('/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        details = request.env['fleet.auction'].search([])

        # print(details.ids)
        return request.render('fleet_auction.web_form_template', {'details': details})

    @route(['/detail_web_page/<int:id>'], type='http', auth='public', website=True)
    def detail_web_page(self, id):
        print(id)
        auction_details = request.env['fleet.auction'].browse(id)
        print(auction_details)
        return request.render('fleet_auction.detail_web_page_template', {'auction_detail': auction_details})

    @route('/bid_form/<int:id>', type='http', auth='public', website=True)
    def bid_form(self,id):
        print(id)
        auction = request.env['fleet.auction'].browse(id)
        users = request.env.user.name
        print(users)
        return request.render('fleet_auction.bid_form_template', {'auction': auction, 'user': users})

    @route('/bid_form/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        name = post.get('amount')
        print(name)
        print(post)
        # request.env['bid.fleet'].sudo().create({
        #     # 'auction_id': post.get('number'),
        #     'customer_id': ,
        #     # 'phone': post.get('phone'),
        #     #
        #     'bid_amount': post.get('amount'),
        #     # 'bid_date': post.get('date')
        #     # 'email': post.get('email'),
        # })






    # @route('/webform/submit', type='http', auth='public', website=True, methods=['POST'])
    # def web_form_submit(self, **post):
    #     request.env['fleet.auction'].sudo().create({
    #                 'name': post.get('name'),
    #                 # 'phone': post.get('phone'),
    #                 # 'email': post.get('email'),
    #             })