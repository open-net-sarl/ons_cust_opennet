odoo.define('ons_cust_opennet.pricing', function (require) {
"use strict";

var ajax = require('web.ajax');

	$(document).ready(function () {
		// var maFonction = function(){

		// }

		var users = $( "#user_select" ).val();
		var user_pricing = $( "#user_pricing" ).text();
		var monthly_price = user_pricing * users
		var annualy_price = user_pricing * users * 12

		$( "#user_selected" ).text( "1 user" )
		$( "#monthly_price" ).text( monthly_price )
		$( "#annualy_price" ).text( annualy_price )

		$( "#user_select" ).on('keyup mouseup', function(){
			users = $( this ).val();
			if (users == '') {
				$( "#user_selected" ).text( "0 user" )
			} else if (users == '1'){
				$( "#user_selected" ).text( "1 user" )
			} else {
				$( "#user_selected" ).text( users + " users" )
			}

			monthly_price = user_pricing * users
			$( "#monthly_price" ).text( monthly_price )
			annualy_price = user_pricing * users * 12
			$( "#annualy_price" ).text( annualy_price )
		});

	});

});