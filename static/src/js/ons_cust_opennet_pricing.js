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
					var sequence = parseInt(myparent.find( ".sequence" ).text());
					var annualy_price = price * 12
					var last_row = $( ".base_row:last" )
					var this_checkbox = $( "input[id='"+id+"']" )

					if (this_checkbox.is(':checked')) {
						last_row.after( '<tr row_id='+id+' class="base_row" sequence="'+sequence+'"><td>'+name+'</td><td class="text-right monthly"><span>'+price+'</span></td><td class="text-right annualy"><span>'+annualy_price+'</span></td></tr>' )
					}
					else {
						$( "tr[row_id='"+id+"']" ).remove();
					}

					var this_tbody = $( "#tbody_sort" ).get(0)

					orderBySequence(this_tbody);

					computeTotal();
				}		
			});

		}

		function checkDependencies() {
			var areas = $( '.functionnal-area' )
			// var dependencies = $( '.depend_name' )

			for (var idx = 0; idx < areas.length; idx++) {
				var checkbox = $(areas[idx]).find('input')
				var dependencies = $(areas[idx]).find('.depend_name')
				//var input_dependencies
				if (checkbox.is(':checked')) {
					// For depends
					var is_checked = true
					for (var i = 0; i < dependencies.length; i++) {
						var depend_id = $(dependencies[i]).attr( 'depend-id' )
						// var depend_parent = depend_id.parent()
						var depend_area_checkbox = $( "input[id='"+depend_id+"']" )

						// if one of the dependencies is not checked -> uncheck the current input
						if (!depend_area_checkbox.is(':checked')) {
							is_checked = false
							// $( "tr[row_id='"+depend_id+"']" ).remove();
						}
					}
					if (!is_checked){
						checkbox.trigger("click")
					}
					// if one of the depends is not checked -> uncheck area
					console.log('checked dependencies')
				}
			}
		}

		function dependArea(checkbox) {
			checkbox.click(function(event) {
				if (!this.checked) {
					console.log('calling checkDependencies')
					checkDependencies();
				} else  {
					// var parent = this.parentNode
					var parent = $( this ).parent();
					var depend_areas = parent.contents( ".depend_name" )

					for (var idx = 0; idx < depend_areas.length; idx++) {
						var depend_area_id = $(depend_areas[idx]).attr( 'depend-id' )

						// var depend_area_id = parent.contents( ".depend_name" ).attr( 'depend-id' )
						var depend_checkbox = $( "input[id='"+depend_area_id+"']" )

						if (depend_checkbox.is(':checked')) {
							console.log('already checked')

						} else {
							updateDependRow(depend_checkbox);
							depend_checkbox.trigger('click');
						}
					}
					
				}
			});
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
		       return a.getAttribute('sequence') - 
		              b.getAttribute('sequence');
		    });

		    // Add them into the tbody in order
		    for(var i = 0; i < rows.length; i++)
		        new_tbody.appendChild(rows[i]);
		    tbody.parentNode.replaceChild(new_tbody, tbody);
		}

		function updateDependRow(checkbox) {
			var myparent = checkbox.parent();

			if (myparent != null) {

				var id = myparent.attr( 'id' )
				var name = myparent.find( ".data_title" ).text();
				var price = parseInt(myparent.find( ".data_price" ).text());
				var annualy_price = price * 12
				var last_row = $( ".base_row:last" )
				var this_checkbox = $( "input[id='"+id+"']" )

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