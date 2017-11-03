odoo.define('ons_cust_opennet.pricing', function (require) {
"use strict";

var ajax = require('web.ajax');

	$(document).ready(function () {

		initializeValues();

		addRow($( ".area_checkbox" ));
		dependArea($( ".area_checkbox" ));
		addRow($( ".logi_checkbox" ));
		addRow($( ".tech_checkbox" ));
		addRow($( ".misc_checkbox" ));
		addRow($( ".hosting_checkbox" ));

		followScroll(40, 200);

		function initializeValues() {
			$( "#user_selected" ).text( "1 user" )

			var user_pricing = $( "#user_pricing" ).text();
			var users = $( "#user_select" ).val();

			writeUserPrice(user_pricing, users);

			var area_price = parseInt($( ".area_price_data" ).text());
			var area_annualy_price = area_price * 12
			$( ".area_price_data" ).text( area_price )
			$( ".area_annualy_price_data" ).text( area_annualy_price )

			computeTotal();
		}

		$( "#user_select" ).on('keyup mouseup', function() {
			var users = $( this ).val();
			var user_pricing = $( "#user_pricing" ).text();

			if (users == '') {
				$( "#user_selected" ).text( "0 user" )
			} 
			else if (users == '1'){
				$( "#user_selected" ).text( "1 user" )
			} 
			else {
				$( "#user_selected" ).text( users + " users" )
			}

			writeUserPrice(user_pricing, users);

			computeTotal();
		});

		function writeUserPrice(user_pricing, users) {
			var monthly_price = user_pricing * users
			var annualy_price = user_pricing * users * 12

			$( "#monthly_price" ).text( monthly_price )
			$( "#annualy_price" ).text( annualy_price )

			computeTotal();
		}

		function addRow(checkbox) {
			checkbox.click(function(event) {
				var myparent = $( this ).parent();

				if (myparent != null) {

					var id = myparent.attr( 'id' )
					var name = myparent.find( ".data_title" ).text();
					var price = parseInt(myparent.find( ".data_price" ).text());
					var annualy_price = price * 12
					var last_row = $( ".base_row:last" )
					var this_checkbox = $( "input[id='"+id+"']" )

					if (this_checkbox.is(':checked')) {
						last_row.after( '<tr row_id='+id+' class="base_row"><td>'+name+'</td><td class="text-right monthly"><span>'+price+'</span></td><td class="text-right annualy"><span>'+annualy_price+'</span></td></tr>' )
					}
					else {
						$( "tr[row_id='"+id+"']" ).remove();
					}

					computeTotal();
				}		
			});

		}

		function dependArea(checkbox) {
			checkbox.click(function(event) {
				if (checkbox.is(':checked')) {
					console.log('this checked')
				} else  {
					var parent = $( this ).parent();
					var depend_area_id = parent.find( ".depend_name" ).attr( 'depend-id' );
					var depend_checkbox = $( "input[id='"+depend_area_id+"']" )
					if (depend_checkbox.is(':checked')) {
						console.log('already checked')
					} else {
						depend_checkbox.prop( "checked", true );
						console.log(depend_checkbox);
						addDependRow(depend_checkbox);
					}
				}

				// For
				// if checked
				// if not continue
				// if checked for depends
				// if one of the depends is not checked -> uncheck area 

			});
		}

		function addDependRow(checkbox) {
			var myparent = checkbox.parent();
			console.log(myparent)

			if (myparent != null) {

				var id = myparent.attr( 'id' )
				var name = myparent.find( ".data_title" ).text();
				var price = parseInt(myparent.find( ".data_price" ).text());
				var annualy_price = price * 12
				var last_row = $( ".base_row:last" )
				var this_checkbox = $( "input[id='"+id+"']" )

				if (this_checkbox.is(':checked')) {
					last_row.after( '<tr row_id='+id+' class="base_row"><td>'+name+'</td><td class="text-right monthly"><span>'+price+'</span></td><td class="text-right annualy"><span>'+annualy_price+'</span></td></tr>' )
				}
				else {
					$( "tr[row_id='"+id+"']" ).remove();
				}

				computeTotal();
			}		
		}

		function computeTotal(){
			var monthly = 0
			var annualy = 0

			$( "tr.base_row" ).each(function() {
				monthly += parseInt($( this ).find( ".monthly span" ).text());
				annualy += parseInt($( this ).find( ".annualy span" ).text());
			});

			$( ".monthly_total" ).text( monthly );
			$( ".annualy_total" ).text( annualy );
		}

		function followScroll(topMargin, time) {
		    var element = $( '.follow-scroll' ),
		        originalY = element.offset().top;
		    
		    // Space between element and top of screen (when scrolling)
		    var topMargin = topMargin;
		    
		    // Should probably be set in CSS; but here just for emphasis
		    element.css('position', 'relative');
		    
		    $( window ).on('scroll', function(event) {
		        var scrollTop = $( window ).scrollTop();
		        
		        element.stop(false, false).animate({
		            top: scrollTop < originalY ? 0 : scrollTop - originalY + topMargin
		        }, this.time);
		    });
		}

	});

});