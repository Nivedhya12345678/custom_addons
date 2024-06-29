# -*- coding: utf-8 -*-
from odoo import fields, models, api, Command
from odoo.exceptions import ValidationError


class FleetAuction(models.Model):
    _name = "fleet.auction"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Fleet Auction"

    name = fields.Char(string="Number", copy=False, default='New', readonly=True)
    vehicle_name_id = fields.Many2one("fleet.vehicle", required=True, string="Vehicle Name")
    vehicle_brand_id = fields.Many2one("fleet.vehicle.model.brand", string="Vehicle Brand")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    current_user = fields.Many2one('res.users', string='Responsible',
                                   default=lambda self: self.env.user)
    active = fields.Boolean(default=True)
    state = fields.Selection(default='draft', copy=False, recuired=True,
                             tracking=True,
                             selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed'),
                                        ('ongoing', 'Ongoing'),
                                        ('success', 'Success'),
                                        ('cancelled', 'Cancelled')])
    description = fields.Text(string="Description")
    start_price = fields.Float(copy=False, string="Start Price")
    won_price = fields.Float(copy=False, string="Won Price")
    customer_id = fields.Many2one("res.partner", string="Customer")
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    phone = fields.Char(string="Phone", compute='_compute_phone', store=True)
    email_from = fields.Char(string="Email", compute='_compute_email_from', store=True)
    tag_ids = fields.Many2many("crm.tag", string="Tags")
    bid_count = fields.Integer(compute='_bid_count', string="Bid Count")
    bid_ids = fields.One2many('bid.fleet', inverse_name='auction_id', string="Bids",
                              domain=[('state', '=', 'confirmed')])
    current_value = fields.Monetary(string="Current Value")
    expenses = fields.One2many('fleet.expense', inverse_name="auction_id")
    total_expense = fields.Monetary(string="Total Expense", compute='_get_price', store=True)

    invoice_id = fields.One2many('account.move', inverse_name="fleet_id")
    invoice_count = fields.Integer(string="Invoice count", compute='_invoice_count')

    related_invoice_id = fields.Many2one('account.move', string="Invoice")
    fleet_payment_state = fields.Selection(related='related_invoice_id.payment_state', string="Payment state")


    def scheduled_action(self):
        for rec in self.search([('state', '!=', 'ongoing')]):
            if rec.start_date and rec.start_date == fields.Date.today():
                rec.write({'state': 'ongoing'})

        for rec in self.search([('state', '!=', 'success')]):
            if rec.end_date and rec.end_date == fields.Date.today():
                if rec.bid_ids:
                    rec.customer_id = rec.bid_ids[0].customer_id
                    rec.won_price = rec.bid_ids[0].bid_amount
                    rec.write({'state': 'success'})

    def action_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('fleet_id', '=', self.name)]
        }

    def _invoice_count(self):
        """ calculating the invoice count"""
        for record in self:
            record.invoice_count = self.env['account.move'].search_count(
                [('fleet_id', '=', self.name)])

    def action_create_auction(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'bid.fleet',
            'view_mode': 'form',
            'target': 'new'
        }

    def action_create_invoice(self):
        """invoice creation"""
        for record in self:
            new_invoice = self.env["account.move"].create([{
                'move_type': 'out_invoice',
                'partner_id': record.customer_id.id,
                'invoice_date': fields.Date.context_today(record),
                'currency_id': record.currency_id.id,
                'fleet_id': self.id,
                'invoice_line_ids': [Command.create({
                    'product_id': 43,
                    'name': record.vehicle_name_id.name,
                    'price_unit': record.won_price
                })],
            }])
            self.related_invoice_id = new_invoice.id
            for record in record.expenses:
                self.env["account.move.line"].create({
                    'product_id': 51,
                    'name': record.expense,
                    'price_unit': record.price_unit,
                    'move_id': new_invoice.line_ids.move_id.id
                })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': new_invoice.id,
                'target': 'current'
            }

    def action_bid(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'bids',
            'res_model': 'bid.fleet',
            'view_mode': 'tree',
            'domain': [('auction_id', '=', self.name), ('state', '=', 'confirmed')],
            'context': "{'create': False}"
        }

    def _bid_count(self):
        """ calculating the bid count"""
        for record in self:
            record.bid_count = self.env['bid.fleet'].search_count(
                [('auction_id', '=', self.name), ('state', '=', 'confirmed')])

    def action_confirm(self):
        """ confirm button"""
        self.write({'state': 'ongoing'})
        for record in self:
            self.current_value = record.start_price

    def action_cancel(self):
        """ cancel button """
        # self.write({'state': 'cancelled'})
        return {
            'name': 'Cancel Reason',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.cancel.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'context': {'default_cancel_id': self.id},
            'target': 'new'
        }

    def action_end(self):
        """ end button """
        self.write({'state': 'success'})
        for record in self:
            if record.bid_ids:
                self.customer_id = record.bid_ids[0].customer_id
                self.won_price = record.bid_ids[0].bid_amount

                mail_template = self.env.ref('fleet_auction.fleet_mail_template')
                mail_template.send_mail(self.id, force_send=True)

    @api.model
    def create(self, vals):
        """ Create a sequence for the fleet auction model """
        vals['name'] = self.env['ir.sequence'].next_by_code('fleet.sequence.code')
        return super(FleetAuction, self).create(vals)

    @api.depends('customer_id.phone')
    def _compute_phone(self):
        """ Sync all  phone number fields """
        for fleet in self:
            if fleet.customer_id.phone:
                fleet.phone = fleet.customer_id.phone

    @api.depends('customer_id.email')
    def _compute_email_from(self):
        """ Sync all customer email fields """
        for fleet in self:
            if fleet.customer_id.email:
                fleet.email_from = fleet.customer_id.email

    @api.constrains('start_date', 'end_date')
    def date_constrains(self):
        """ function to validate start date and end date"""
        for date in self:
            if date.end_date < date.start_date:
                raise ValidationError('Sorry, End Date Must be greater Than Start Date...')

    @api.depends('expenses')
    def _get_price(self):
        for record in self:
            self.total_expense = sum(record.expenses.mapped('price_unit'))


