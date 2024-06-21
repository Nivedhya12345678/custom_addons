# -*- coding: utf-8 -*-
from odoo import api,Command,fields, models
from odoo.fields import Datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commission_amount = fields.Float(string='Commission Amount', compute='_compute_commission_amount', store=True)

    @api.depends('order_line')
    def _compute_commission_amount(self):
        today_date = Datetime.today().date()
        if self.user_id.commission_id.from_date and self.user_id.commission_id.to_date:
            if self.user_id.commission_id.from_date <= today_date and today_date <= self.user_id.commission_id.to_date:
                commission = self.user_id.commission_id
                if commission.commission_type == 'product_wise':
                    commission_plan = self.user_id.commission_id.product_commission_ids
                    product_wise_total = 0.0
                    for rec in self.order_line:
                        for record in commission_plan:
                            if rec.product_id == record.product_id:
                                commission_total = (rec.price_unit * (record.rate_percentage / 100)) * rec.product_uom_qty
                                if commission_total > record.maximum_amount:
                                    commission_total = record.maximum_amount
                                    product_wise_total = product_wise_total + commission_total
                                    self.commission_amount = product_wise_total
                                else:
                                    product_wise_total = product_wise_total + commission_total
                                    self.commission_amount = product_wise_total

                elif commission.revenue_type == 'straight':
                    revenue_commission = self.user_id.commission_id.revenue_commission_ids
                    straight_total = 0.0
                    for record in revenue_commission:
                        if self.amount_untaxed >record.from_amount and  self.amount_untaxed < record.to_amount:
                            commission_total = self.amount_untaxed * (record.rate / 100)
                            straight_total = straight_total + commission_total
                            self.commission_amount = straight_total
                else:
                    revenue_commission = self.user_id.commission_id.revenue_commission_ids
                    graduated_total = 0.0
                    for record in revenue_commission:
                        if self.amount_untaxed > record.to_amount and record.to_amount !=0:
                            graduated_total += (record.to_amount - record.from_amount) * (record.rate / 100)
                        elif (self.amount_untaxed >=record.from_amount and  self.amount_untaxed <= record.to_amount) or record.to_amount==0:
                            if self.amount_untaxed - record.from_amount > 0:
                                commission = (self.amount_untaxed - record.from_amount)*(record.rate / 100)
                                graduated_total += commission
                                self.commission_amount = graduated_total

    def action_confirm(self):
        if self.user_id:
            self.user_id.update({
                'sale_order_ids': [(fields.Command.link(self.id))]
            })
        if self.team_id:
            self.team_id.update({
                'sale_order_ids': [(fields.Command.link(self.id))]
            })
        for rec in self:
            rec.user_id.total_commission = rec.user_id.total_commission + self.commission_amount
            rec.team_id.total_commission = rec.team_id.total_commission + self.commission_amount


