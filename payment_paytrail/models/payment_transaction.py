# -*- coding: utf-8 -*-
import logging
import pprint

from werkzeug import urls

from odoo.addons.payment_paytrail.controllers.main import PaytrailController

from odoo import _, models

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):

    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):

        res = super()._get_specific_rendering_values(processing_values)
        print('procs',res)
        if self.provider_code != 'paytrail':
            return res

        payload = self._paytrail_prepare_payment_request_payload()
        print('payloard',payload)
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._paytrail_make_request('/payments', data=payload)
        print('payment data',payment_data)

        # The provider reference is set now to allow fetching the payment status after redirection
        self.provider_reference = payment_data.get('id')

        checkout_url = payment_data['_link']['checkout']['href']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        print("print",url_params)
        return {'api_url': checkout_url, 'url_params': url_params}

    def _paytrail_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """
        # user_lang = self.env.context.get('lang')
        base_url = self.provider_id.get_base_url()
        print(base_url)
        print('self', self.reference)
        redirect_url = urls.url_join(base_url, PaytrailController._return_url)
        paytrail_values = {
            'reference': self.reference,
            'amount':self.amount,
            'currency':self.currency_id.id,
            'customer':{
                'email': self.partner_email,
            },

            'language':self.partner_lang,

            # 'provider_id': self

            # 'locale': user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
            # 'method': [const.PAYMENT_METHODS_MAPPING.get(
            #     self.payment_method_code, self.payment_method_code
            # )],
            # Since Mollie does not provide the transaction reference when returning from
            # redirection, we include it in the redirect URL to be able to match the transaction.
            'redirectUrl': redirect_url,
        }
        return paytrail_values