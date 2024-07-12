# -*- coding: utf-8 -*-

import logging
import pprint

import requests
from werkzeug import urls

from odoo import _, fields, models, service
from odoo.exceptions import ValidationError

# from odoo.addons.payment_paytrail import const

_logger = logging.getLogger(__name__)
class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('paytrail', "Paytrail")], ondelete={'paytrail': 'set default'})
    paytrail_merchant_id = fields.Char(
        string="Merchant Id",
        required_if_provider='paytrail',
    )
    paytrail_secret_key = fields.Char(
        string="Paytrail Secret key",
        required_if_provider='paytrail',
        groups='base.group_system',
    )

    def _paytrail_make_request(self, endpoint, data=None, method='POST'):
        print('data',data)

        self.ensure_one()
        endpoint = f'/{endpoint.strip("/")}'
        print('end',endpoint)
        url = urls.url_join('https://services.paytrail.com/', endpoint)

        headers = {
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, json=data, headers=headers, timeout=60)
        print('data',data)
        response.raise_for_status()
        #     except requests.exceptions.HTTPError:
        #         _logger.exception(
        #             "Invalid API request at %s with data:\n%s", url, pprint.pformat(data)
        #         )
        #         raise ValidationError(
        #             "Paytrail: " + _(
        #                 "The communication with the API failed."
        #             ))
        # except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        #     _logger.exception("Unable to reach endpoint at %s", url)
        #     raise ValidationError(
        #         "Paytrail: " + _("Could not establish the connection to the API.")
        #     )
        return response.json()

