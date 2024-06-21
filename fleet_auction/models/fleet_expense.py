from odoo import fields, models, api


class FleetExpense(models.Model):
    _name = "fleet.expense"
    _description = "Fleet Expense"

    auction_id = fields.Many2one('fleet.auction', string="Number")
    expense = fields.Char(string="Expense")
    company_id = fields.Many2one('res.company', string="Company", invisible="1",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", invisible="1",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    price_unit = fields.Monetary(string="Unit Price")






