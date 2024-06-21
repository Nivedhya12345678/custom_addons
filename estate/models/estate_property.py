from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    available_from = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(default='new', copy=False, recuired=True, selection=[('new', 'New'),
                                                                                  ('offer received', 'Offer Received'),
                                                                                  ('offer accepted', 'Offer Accepted'),
                                                                                  ('sold', 'Sold '),
                                                                                  ('canceled', 'Canceled')],)
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one('res.users', string='Salesman', index=True, tracking=True,
                              default=lambda self: self.env.user)
    property_type = fields.Many2one("estate.property.type", string="Property type")
    tag = fields.Many2many("estate.property.tag", string="Tag")
    offer = fields.One2many("estate.property.offer", inverse_name="property_id")

