from odoo import fields, models, api


class FleetBid(models.Model):
    _name = "bid.fleet"
    _description = "Bid"
    _rec_name = "auction_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'bid_amount desc'

    auction_id = fields.Many2one("fleet.auction", domain="['|', ('state', '=', 'confirmed'),('state', '=', 'ongoing')]",
                                 string="Auction", ondelete='cascade')
    bid_amount = fields.Float(string="Bid Amount")
    bid_price = fields.Float(string="Bid Price", compute='_get_price')
    bid_date = fields.Date(string="Bid Date")
    phone = fields.Char(string="Phone Number", compute='_compute_phone', store=True)
    state = fields.Selection(default='draft', copy=False, recuired=True,
                             selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),])
    customer_id = fields.Many2one("res.partner", string="Customer")

    def action_confirm(self):
        """ confirm button"""
        self.write({'state': 'confirmed'})

    @api.depends('auction_id')
    def _get_price(self):
        for record in self:
            self.bid_price = record.auction_id.start_price

    @api.depends('customer_id.phone')
    def _compute_phone(self):
        """ Sync all  phone number fields """
        for fleet in self:
            if fleet.customer_id.phone:
                fleet.phone = fleet.customer_id.phone
