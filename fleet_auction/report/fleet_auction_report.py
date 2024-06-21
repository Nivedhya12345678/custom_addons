# -*- coding: utf-8 -*-
from odoo import models, api, exceptions


class FleetAuctionReport(models.AbstractModel):
    _name = 'report.fleet_auction.fleet_auction_report'

    @api.model
    def _get_report_values(self,  docids, data=None):

        query = """select  fv.name as vehicle, re.name, fl.start_date, fl.end_date, fl.customer_id , 
                   fl.state ,  fl.current_value, bi.state as bid_state, bi.bid_amount, fl.current_user,
                   fl.won_price from fleet_auction as fl 
                   inner join res_partner as re on re.id = fl.customer_id
                   inner join res_users as ru on ru.id = fl.current_user
                   inner join bid_fleet as bi on bi.customer_id = fl.customer_id and bi.auction_id = fl.id
                   inner join fleet_vehicle as fv on fv.id = fl.vehicle_name_id where 1=1 """

        if data['customer']:
            query += f" and re.name = '{data['customer']}'"
        if data['responsible']:
            query += f" and fl.current_user = {data['responsible']}"
        if data['from_date']:
            query += f" and fl.start_date >= '{data['from_date']}'"
        if data['to_date']:
            query += f" and fl.end_date <= '{data['to_date']}'"
        if data['state']:
            query += f" and fl.state = '{data['state']}'"

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        if report:
            return {
                'doc_model': 'fleet.auction',
                'docs': report,
                'data': data,
            }
        else:
            raise exceptions.UserError('There is no data to generate reports')
