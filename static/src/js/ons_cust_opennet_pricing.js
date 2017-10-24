odoo.define('ons_cust_opennet.pricing', function (require) {
"use strict";

var ajax = require('web.ajax');

	$(document).ready(function () {
		var writePrice = function(user_pricing, users){
			let monthly_price = user_pricing * users
			$( "#monthly_price" ).text( monthly_price )
			let annualy_price = user_pricing * users * 12
			$( "#annualy_price" ).text( annualy_price )
		}

		$( "#user_selected" ).text( "1 user" )
		var user_pricing = $( "#user_pricing" ).text();
		var users = $( "#user_select" ).val();

		writePrice(user_pricing, users);

		$( "#user_select" ).on('keyup mouseup', function(){
			users = $( this ).val();
			if (users == '') {
				$( "#user_selected" ).text( "0 user" )
			} else if (users == '1'){
				$( "#user_selected" ).text( "1 user" )
			} else {
				$( "#user_selected" ).text( users + " users" )
			}

			writePrice(user_pricing, users);

		});

		var area_price = parseInt($( "#area_price" ).text());
		var area_annualy_price = area_price * 12
		$( "#area_price" ).text( area_price )
		$( "#area_annualy_price" ).text( area_annualy_price )

		$( ".area_checkbox" ).click(function(){
			console.log('test')
			$( "#valais" ).append( '<tr class="active"><td>Total</td><td class="text-right"></td><td class="text-right"></td></tr>' )
		});

	});

});