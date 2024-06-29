/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.bidDetails = publicWidget.Widget.extend({
    selector: '.bid_form',
    events: {
        'change #amount': '_onSelectName',
    },
    _onSelectName : function(ev){

    var record = document.getElementById("button").getAttribute('value')

    console.log(record,'fleet')
    $('#number').val(record)

    },
})

