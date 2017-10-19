var last_id = -100;
$('.ons-pricing-area').on("click", function(){
	// Récupérer l'id de l'attribut
	var attr_id = $(this).attr('index-number')
	console.log(attr_id);
	// Afficher la div correspondant à l'id
	if(last_id == attr_id){
		$("[index-number-info="+last_id+"]").toggleClass('hide')
	}
	else{
		$("[index-number-info="+last_id+"]").addClass('hide')
		$("[index-number-info="+attr_id+"]").removeClass('hide')
	}
	last_id = attr_id;
});