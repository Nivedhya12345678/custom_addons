
import logging
import pprint

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class PaytrailController(http.Controller):

    @http.route(
        '/paytrail-payment/success', type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def paytrail_return_from_checkout(self, **data):

        _logger.info("handling redirection from paytrail with data:\n%s", pprint.pformat(data))
        request.env['payment.transaction'].sudo()._handle_notification_data('paytrail', data)
        return request.redirect('/payment/status')