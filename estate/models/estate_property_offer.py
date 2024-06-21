from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Partner", recuired=True)
    property_id = fields.Many2one("estate.property", recuired=True)
