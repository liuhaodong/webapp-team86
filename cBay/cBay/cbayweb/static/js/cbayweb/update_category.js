$(document).ready(function(){
	console.log('ready');
	$('#categorypicker').change(function() {
    //alert($("#categorypicker option:selected").text());
    console.log('category changed');
    var category = $("#categorypicker option:selected").text();
    var $item_by_category = $('#items_by_category');
    var $panel_sale = $('#panel-fixed-price');
    var $panel_auction = $('#panel-auction');


    //Template html for new comment
    var saleTemplate = ""+
    "<div class='col-md-12 column well well-lg' >" + 
    "<div class='col-md-6 column'>"+
    "<span><a href='/viewSale/{{pk}}'><img src='/item_picture/{{pk}}' style='height:280px' class='img-thumbnail'></a></span>"+
    "</div><div class='col-md-6 column'><h1>Name: {{fields.name}}</h1><h2>Price: {{fields.price}}</h2><p>Start Time: {{fields.start_time}}</p><p>End Time: {{fields.end_time}}</p></div></div>";


    var auctionTemplate = ""+
    "<div class='col-md-12 column well well-lg' >" + 
    "<div class='col-md-6 column'>"+
    "<span><a href='/viewAuction/{{pk}}'><img src='/auction_picture/{{pk}}' style='height:280px' class='img-thumbnail'></a></span>"+
    "</div><div class='col-md-6 column'><h1>Name: {{fields.name}}</h1><h2>Current Max Bid: {{fields.current_max_bid}}</h2><p>Start Time: {{fields.start_time}}</p><p>End Time: {{fields.end_time}}</p></div></div>";


    $.ajax({
    	url: '/get_items_by_category/' + category,
    	type: 'GET',
    })
    .done(function(data) {
    	$panel_sale.empty();
    	$panel_auction.empty();
    	var sales_jsonObj = jQuery.parseJSON( data['sales_data'] );
    	var auctions_jsonObj = jQuery.parseJSON( data['auctions_data'] );

    	var output = "";
    	$.each( sales_jsonObj, function(i, item) {
    		output = Mustache.render(saleTemplate, item);
    		$(output).hide().appendTo($panel_sale).slideDown(300);
    	});

    	$.each( auctions_jsonObj, function(i, item) {
    		output = Mustache.render(auctionTemplate, item);
    		$(output).hide().appendTo($panel_auction).slideDown(300);
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
