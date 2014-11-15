$(document).ready(function() {
	startInterval();
});

// declare interval and delay
var interval,delay = 10000;// miliseconds


// function that gets ran on interval
function runIntervalAjax(){
	var auction_id = $("#hidden_auction_id").attr('value');
	if($("#auction_ended_alert").length ==1 ){
		stopInterval();
		return;
	}
	$.ajax({
		url: '/check_auction/'+auction_id,
		type: 'GET',
	})
	.done(function(data) {
		var $view_auction_content = $("#viewAuctionContent");
		
		var $place_bid_form = $("#placeBidForm");
		if(data['is_ended'] == true){
			$view_auction_content.prepend("<div class='alert alert-danger' role='alert'><p>This Auction has ended</p></div>");
			$view_auction_content.prepend("<h2 class='bg-success'>Winner: "+ data['winner_name'] +"</h2>");
			$view_auction_content.append("");
			$place_bid_form.hide();
			window.alert("auction is ended");
			stopInterval();
		}
		
		
	})
	.fail(function() {
		console.log("error");
	})
}

// function to stop interval
function stopInterval(){ // stop interval
	clearInterval(interval);
}

// function to start interval
function startInterval(){ // start interval
	runIntervalAjax();
	interval = setInterval(function(){
		runIntervalAjax();
	},delay);
}