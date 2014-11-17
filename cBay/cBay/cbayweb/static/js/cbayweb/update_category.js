$(document).ready(function(){
    $('#categorypicker').change(function() {
    //alert($("#categorypicker option:selected").text());
    var category = $("#categorypicker option:selected").text();
    var $item_by_category = $('#items_by_category');

    $.ajax({
    	url: '/get_items_by_category/' + category,
    	type: 'GET',
    })
    .done(function(data) {
    	$item_by_category.empty();
    	$.each( data, function(i, item) {
			console.log(item['fields']['name']);
        });
    })

    .fail(function() {
    	console.log("error");
    })

    .always(function() {
    	console.log("complete");
    });
    
  });  
});
