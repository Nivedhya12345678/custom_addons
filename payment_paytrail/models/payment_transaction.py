# -*- coding: utf-8 -*-
import hashlib
import hmac
import uuid

import requests
import json
from odoo import _, models
from odoo.exceptions import ValidationError
from odoo.http import request, _logger
from odoo.tools.safe_eval import datetime


class PaymentTransaction(models.Model):

    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):

        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'paytrail':
            return res

        secret_key = self.provider_id.paytrail_secret_key
        merchant_id = self.provider_id.paytrail_merchant_id
        order_stamp = str(uuid.uuid4())
        base_url = "https://7626-115-245-156-254.ngrok-free.app/"
        current_datetime = datetime.datetime.utcnow()
        timestamp = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        checkout_nonce = self.reference
        product_list = []
        for records in request.website.sale_get_order():
            for vals in records.website_order_line:
                product_stamp = str(uuid.uuid4())
                orderline = {
                    "unitPrice": int(vals.price_total),
                    "vatPercentage": 0,
                    "units": vals.product_uom_qty,
                    "productCode": vals.product_id.default_code,
                    "stamp": product_stamp
                }
                product_list.append(orderline)

        payload = {
            "stamp": order_stamp,
            "reference": self.reference,
            "amount": int(self.amount),
            "currency": "EUR",
            "language": "EN",
            "items": product_list,
            "customer": {
                "email": self.partner_email
            },
            "redirectUrls": {
                "success": base_url + "/paytrail-payment/success",
                "cancel": base_url + "/paytrail-payment/cancel",
            },
            "callbackUrls": {
                "success": base_url + "/paytrail-payment/success",
                "cancel": base_url + "/paytrail-payment/cancel",
            },

        }
        payload_json = json.dumps(payload)
        signature_header = {"checkout-account": merchant_id,
                            "checkout-algorithm": "sha256",
                            "checkout-method": "POST",
                            "checkout-nonce": checkout_nonce,
                            "checkout-timestamp": f"{timestamp}"}
        sha = self.calculate_hmac(secret_key, signature_header, payload_json)
        headers = {
            'checkout-account': merchant_id,
            'checkout-algorithm': 'sha256',
            'checkout-method': 'POST',
            'checkout-nonce': checkout_nonce,
            'checkout-timestamp': timestamp,
            'signature': sha,
            'content-type': 'application/json; charset=utf-8',
        }

        url = "https://services.paytrail.com/payments/"

        response = requests.post(url, headers=headers, data=payload_json)
        dict = response.json()['href']
        return {'api_url': dict}

    @staticmethod
    def compute_sha256_hash(message: str, secret: str) -> str:

        hash = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
        return hash.hexdigest()

    def calculate_hmac(self, secret, headerParams: dict,
                       body: str = '') -> str:
        data = []
        for key, value in headerParams.items():
            if key.startswith('checkout-'):
                data.append('{key}:{value}'.format(key=key, value=value))

        data.append(body)
        item = '\n'.join(data)
        return self.compute_sha256_hash(item, secret)


    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'paytrail' or len(tx) == 1:
            return tx

        reference = notification_data.get('checkout-reference')
        if not reference:
            raise ValidationError(
                "Paytrail: " + _("Received data with missing reference %(ref)s.", ref=reference)
            )

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'paytrail')])
        if not tx:
            raise ValidationError(
                "Paytrail: " + _("No transaction found matching reference %s.", reference)
            )

        return tx

    def _process_notification_data(self, notification_data):

        super()._process_notification_data(notification_data)
        if self.provider_code != 'paytrail':
            return

        self.provider_reference = notification_data.get('checkout-reference')
        payment_method_type = notification_data.get('checkout-provider', '')
        payment_method = self.env['payment.method']._get_from_code(payment_method_type)
        self.payment_method_id = payment_method or self.payment_method_id

        status = notification_data.get('checkout-status')
        if status == 'ok':
            self._set_done()
            self.env['ir.config_parameter'].sudo().set_param('sale.automatic_invoice', 'True')
        else:
            error_code = notification_data.get('Error')
            self._set_error(
                "Paytrail: " + _("The payment encountered an error with code %s", error_code)
            )
