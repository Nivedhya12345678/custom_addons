from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Estate Model"

    name = fields.Char(required=True)



