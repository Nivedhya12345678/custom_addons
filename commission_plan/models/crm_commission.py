from odoo import fields, models


class CrmCommission(models.Model):
    _name = "crm.commission"
    _description = "Commission Plan"

    name = fields.Char(string='Commission')
    active = fields.Boolean(string='Active', default=True)
    from_date = fields.Date(string='From date', required=True)
    to_date = fields.Date(string='To date',)
    commission_type = fields.Selection(selection=[
        ('product_wise', 'Product wise'),
        ('revenue_wise', 'Revenue wise')], default='product_wise')
    revenue_type = fields.Selection(selection=[
        ('straight', 'Straight'),
        ('graduated', 'Graduated')], string='Revenue type')
    product_commission_ids = fields.One2many('product.commission', inverse_name='commission_id', string='Product wise')
    revenue_commission_ids = fields.One2many('revenue.commission', inverse_name='commission_id', string='Revenue wise')
