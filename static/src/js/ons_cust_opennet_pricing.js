/*
	ONS pricing
	© 2017 Open Net Sarl
*/

odoo.define('ons_cust_opennet.pricing', function (require) {
	"use strict";

	var ajax = require('web.ajax');

	$(document).ready(function () {

		initializeValues();
		onChangeNbUser($( "#user_select" ));
		onChangeHostingType($( ".radio-hosting-type" ));
		addRow($( ".area-checkbox" ));
		dependArea($( ".area-checkbox" ));
		addRow($( ".logi_checkbox" ));
		addRow($( ".tech_checkbox" ));
		addRow($( ".misc_checkbox" ));
		addRow($( ".hosting_checkbox" ));
		uncheckHosting($( ".hosting_checkbox" ));
		toggleInfo($( "#showInfo" ));

		$( "#hosting_default" ).trigger('click');

		$( window ).scroll(function(){
			if ($(this).scrollTop() > 100) {
				$( '.scrollToTop' ).fadeIn();
			} else {
				$( '.scrollToTop' ).fadeOut();
			}
		});
		
		$( '.scrollToTop' ).click(function(){
			$('html, body').animate({ scrollTop: 0 }, "slow");
			return false;
		});

		$( "#sendButton" )[ 0 ].addEventListener("click", sendInfo);

		$( '.follow-scroll' ).simpleScrollFollow({
			limit_elem: '#limit_follow',
			min_width: 992
		});
	});

	function initializeValues() {

		var user_text = "Nombre d'utilisateur non défini"
		var user_price = 0

		var area_price = parseFloat($( ".base_row_price" ).text());
		area_price = area_price.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")
		user_price = user_price.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")

		$( ".base_row_price" ).text( area_price )
		$( "#user_selected" ).text( user_text )
		$( "#monthly_price" ).text( user_price )

		var users = $( "#user_select" ).val()
		checkNbUser(users);
		computeTotal();
	}

	function addRow(checkbox) {
		checkbox.click(function(event) {
			var myparent = $( this ).parent().parent();
			var parent_row = myparent.parent();
			var this_tbody = $( "#tbody_area" )
			if (this.className == 'logi_checkbox' || this.className == 'tech_checkbox' || this.className == 'misc_checkbox') {
				this_tbody = $( "#tbody_option" )
			}
			if (this.className == 'hosting_checkbox') {
				this_tbody = $( "#tbody_hosting" )
			}
			if (myparent != null) {

				var id = myparent.attr( 'id' )
				var name = myparent.find( ".data_title" ).text();
				var price = parseFloat(myparent.find( ".data_price" ).text());
				var sequence = parseInt(myparent.find( ".sequence" ).text());
				var this_checkbox = $( "input[id='"+id+"']" )
				var price_type = this_checkbox.attr( "price_type" )
				var second_price = 0
				console.log(price_type)

				price = price.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")

				if (this_checkbox.is(':checked')) {
					if (price_type == "base") {
						this_tbody.append( '<tr row_id='+id+' class="base_row" sequence="'+sequence+
						'"><td>'+name+'</td><td class="text-right base"><span>'
						+price+'</span></td><td class="text-right monthly"><span style="display:none;">'
						+second_price+'</span></td></tr>' )
					} else if (price_type == "monthly") {
						this_tbody.append( '<tr row_id='+id+' class="base_row" sequence="'+sequence+
						'"><td>Hébergement</td><td class="text-right base"><span  style="display:none;">'
						+second_price+'</span></td><td class="text-right monthly"><span>'
						+price+'</span></td></tr>' )
					}
					parent_row.addClass( "selected" )
				}
				else {
					$( "tr[row_id='"+id+"']" ).remove();
					parent_row.removeClass( "selected" )
				}

				orderBySequence(this_tbody.get(0));

				computeTotal();
			}
		});

	}

	function computeTotal(){
		var base = 0
		var monthly = 0

		$( "tr.base_row" ).each(function() {
			base += parseFloat($( this ).find( ".base span" ).text().replace(' ',''));
			monthly += parseFloat($( this ).find( ".monthly span" ).text().replace(' ',''));
		});

		base = base.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")
		monthly = monthly.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")

		$( ".base_total" ).text( base )
		$( ".monthly_total" ).text( monthly );
	}

	function dependArea(checkbox) {
		checkbox.click(function(event) {
			if (!this.checked) {
				checkDependencies();
			} else  {
				// var parent = this.parentNode
				var parent = $( this ).parent();
				var depend_areas = parent.contents( ".depend_name" )

				for (var idx = 0; idx < depend_areas.length; idx++) {
					var depend_area_id = $(depend_areas[idx]).attr( 'depend-id' )
					var depend_checkbox = $( "input[id='"+depend_area_id+"']" )

					if (depend_checkbox.is(':checked')) {

					} else {
						updateDependRow(depend_checkbox);
						depend_checkbox.trigger( 'click' );
					}
				}
				
			}
		});
	}

	function checkDependencies() {
		var areas = $( '.functionnal-area' )

		for (var idx = 0; idx < areas.length; idx++) {
			var checkbox = $(areas[idx]).find( 'input' )
			var dependencies = $(areas[idx]).find( '.depend_name' )

			if (checkbox.is(':checked')) {
				var is_checked = true

				for (var i = 0; i < dependencies.length; i++) {
					var depend_id = $(dependencies[i]).attr( 'depend-id' )
					var depend_area_checkbox = $( "input[id='"+depend_id+"']" )

					if (!depend_area_checkbox.is(':checked')) {
						is_checked = false
					}
				}

				if (!is_checked){
					checkbox.trigger( "click" )
				}
			}
		}
	}

	function updateDependRow(checkbox) {
		var myparent = checkbox.parent();

		if (myparent != null) {

			var id = myparent.attr( 'id' )
			var name = myparent.find( ".data_title" ).text();
			var price = parseInt(myparent.find( ".data_price" ).text());
			var last_row = $( ".base_row:last" )
			var this_checkbox = $( "input[id='"+id+"']" )

			computeTotal();
		}
	}

	function orderBySequence(tbody) {
		var new_tbody = tbody.cloneNode(false);

		// Add all rows to an array
		var rows = [];
		for (var i = tbody.childNodes.length; i--;) {
			if (tbody.childNodes[i].nodeName === 'TR')
				rows.push(tbody.childNodes[i]);
		}

		// Sort the rows in descending order
		rows.sort(function(a, b){
			return a.getAttribute( 'sequence' ) - 
				b.getAttribute( 'sequence' );
		});

		// Add them into the tbody in order
		for(var i = 0; i < rows.length; i++)
			new_tbody.appendChild(rows[i]);
		tbody.parentNode.replaceChild(new_tbody, tbody);
	}

	function checkNbUser(users) {
		if (users == '') {
			$( "#user_selected" ).text( "0 utilisateur" )
		}
		else if (users == '0') {
			$( "#user_selected" ).text( "0 utilisateur" )
		}
		else if (users == '1') {
			$( "#user_selected" ).text( "1 utilisateur" )
		}
		else if (users < '0') {
			$( "#user_selected" ).text( "Ceci n'est pas possible" )
		}
		else {
			$( "#user_selected" ).text( users + " utilisateurs" )
		}
	}

	function onChangeNbUser(input) {
		input.on('keyup mouseup', function() {
			var users = $( this ).val();

			checkNbUser(users)

			getUserPrice()
		});
	}

	function onChangeHostingType(radio) {
		radio.on('click', function() {
			var inputValue = $(this).attr("value");
			if (inputValue == 'enterprise') {
				console.log('input value is enterprise')
				$( '.other-row' ).hide()
				$( '.enterprise-row' ).show()
			}

			if (inputValue == 'community') {
				console.log('input value is community')
				$( '.enterprise-row' ).hide()
				$( '.other-row' ).show()
			}

			getUserPrice()
		});
	}

	function getUserPrice() {
		var nb_users = $( "#user_select" ).val();
		var radios = $( ".radio-hosting-type" );
		var type = ""
		var checked_radio = ""
		var checked_hosting = ""
		var all_hostings = $( "#hostings" )
		var all_prices = $( "#price_table" )
		var hosting_checkbox = $( '.hosting_checkbox' )

		for (var idx = 0; idx < radios.length; idx++){
			if ($(radios[idx]).is(':checked')){
				checked_radio = $(radios[idx])
			}
		}

		if ($(checked_radio).val() == 'enterprise'){
			type = "enterprise"
		} else if ($(checked_radio).val() == 'community') {
			type = "community"
		}
		

		all_hostings.children( 'div' ).each(function () {
			if ($(this).find( 'input' ).is(':checked')) {
				checked_hosting = $(this)
			}
		});

		hosting_checkbox.each(function () {
			if ($(this).is( ':checked' )) {
				var hosting_checked_checkbox = $(this)
				var hosting_id = hosting_checked_checkbox.attr( 'id' )
				var hosting_flat_price = parseInt(hosting_checked_checkbox.parent().parent().find( ".data_price" ).text())

				var filtred_hosting_prices = []
				var hosting_prices = all_prices.children('span[hosting_id="'+hosting_id+'"]')

				for (var i = 0; i < hosting_prices.length; i++) {
					var hosting_price = $(hosting_prices[i])
					var nb_user = hosting_price.attr( 'nb_user' )

					nb_user = parseInt(nb_user)
					nb_users = parseInt(nb_users)

					if (nb_users >= nb_user) {
						filtred_hosting_prices.push(hosting_price);
						if (nb_users == nb_user) {
							break;
						}
					}
					else {
						filtred_hosting_prices.push(hosting_price);
						break;
					}
				}

				var compute_details = []
				var previous_nb_user = 0
				var final_price = 0

				for (var i=0; i < filtred_hosting_prices.length-1; i++) {
					var hosting_price = $(filtred_hosting_prices[i])
					var nb_user = parseInt(hosting_price.attr( 'nb_user' ))
					var price = parseInt(hosting_price.attr( 'price' ))
					compute_details.push("(" + (nb_user - previous_nb_user) + " x " + price.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ")")
					final_price += (nb_user -previous_nb_user) * price
					previous_nb_user = nb_user
				}

				var last_host_price = parseInt($(filtred_hosting_prices[filtred_hosting_prices.length-1]).attr('price'))
				compute_details.push("(" + (nb_users - previous_nb_user) + " x " + last_host_price.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ")")
				compute_details = compute_details.join(" + ")
				final_price += (nb_users - previous_nb_user) * last_host_price

				$( "#user_calcul" ).text( compute_details )
				$( "#monthly_price" ).text( final_price.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") )

				computeTotal()
			}
		});

	}

	function uncheckHosting(checkbox) {
		checkbox.click(function(event) {
			var areas = $( '.hosting-area' )

			if (this.checked) {
				for (var idx = 0; idx < areas.length; idx++) {
					var checkbox = $(areas[idx]).find( 'input' )

					if (checkbox.is(':checked')) {
						if (checkbox[0] != this) {
							checkbox.trigger( "click" )
						}
					}
				}
				getUserPrice()
			}
			
		});
	}

	function toggleInfo(button){
		button.click(function(event) {
			var parent = $(this).parent()
			var form = parent.find( "#contact" )
			form.toggle( "blind" )
		});
	}

	function sendInfo(){
		var name = $( '#name' ).val()
		var company = $( '#company' ).val()
		var email = $( '#email' ).val()
		var phone = $( '#phone' ).val()
		var name_div = $( '#name' ).parent()
		var phone_div = $( '#phone' ).parent()
		var table_html = $( '#pricing_table' ).html()
		var isValid = true

		if (name == ""){
			isValid = false
			name_div.addClass( 'has-error' )
		} else {
			name_div.removeClass( 'has-error' )
		}

		if (phone == ""){
			isValid = false
			phone_div.addClass( 'has-error' )
		}
		else {
			phone_div.removeClass( 'has-error' )
		}

		if (isValid == false) {
			$( "#sendError" ).show("blind")
			$( "#sendSucces" ).hide("blind")
		}

		if (isValid == true) {
			ajax.jsonRpc('/pricing/send', 'call', {
				'name': name,
				'company': company,
				'email': email,
				'phone': phone,
				'html': table_html,
			})
			.then(function (result) {
				$( "#sendSucces" ).show("blind")
				$( "#sendError" ).hide("blind")
				name_div.removeClass( 'has-error' )
				phone_div.removeClass( 'has-error' )

				$( '#name' ).val( '' )
				$( '#company' ).val( '' )
				$( '#email' ).val( '' )
				$( '#phone' ).val( '' )

				console.log('succes')
			})
			.fail(function () {
				console.log('fail')
			});
		}
	}
});
