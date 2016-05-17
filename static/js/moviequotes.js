var rh = rh || {}; // If rh exists dont blow it away just use the old one
rh.mq = rh.mq || {}; // MovieQuote(mq) namespace in RoseHulman(rs) namespace to avoid the not so posible in this project overlapping

rh.mq.editing = false; //instead of calling it editing, rh.mq.editing in the rh.mq namespace.

rh.mq.hideNavbar = function() {
	$navbar = $(".collapse.navbar-collapse");
	if ($navbar.hasClass("in")) {
		$navbar.collapse("hide");
	}
};

rh.mq.enableButtons = function() {
	$("#toggle-edit").click( function() {
		if (rh.mq.editing) {
			rh.mq.editing = false;
			$(".edit-actions").addClass("hidden");
			$(this).html("Edit");
		} else {
			rh.mq.editing = true;
			$(".edit-actions").removeClass("hidden");
			$(this).html("Done");
		}
		rh.mq.hideNavbar();
	});	
	
	$("#add-quote").click (function() {
		$("#insert-quote-modal .modal-title").html("Add a MovieQuote");
		$("#insert-quote-modal button[type=submit]").html("Add Quote");
		
		$("#insert-quote-modal input[name=quote]").val("");
		$("#insert-quote-modal input[name=movie]").val("");
		$("#insert-quote-modal input[name=entity_key]").val("").prop("disabled", true);
		rh.mq.hideNavbar();
	});
	
	$(".edit-movie-quote").click (function() { // We use a class(.) edit-movie-quote to access its this, using id would bring us the first element only
		$("#insert-quote-modal .modal-title").html("Edit this MovieQuote");
		$("#insert-quote-modal button[type=submit]").html("Edit Quote");
		
		quote = $(this).find(".quote").html();
		movie = $(this).find(".movie").html();
		entityKey = $(this).find(".entity-key").html();
		$("#insert-quote-modal input[name=quote]").val(quote);
		$("#insert-quote-modal input[name=movie]").val(movie);
		$("#insert-quote-modal input[name=entity_key]").val(entityKey).prop("disabled", false); // To send it to the server
	});
	
	$(".delete-movie-quote").click (function() { 
		entityKey = $(this).find(".entity-key").html();
		$("#delete-quote-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});
};

rh.mq.attachEventHandlers = function () {
	$("#insert-quote-modal").on("shown.bs.modal" , function() {
		$("input[name=quote]").focus();
	});
};

$(document).ready( function() {
	rh.mq.enableButtons();
	rh.mq.attachEventHandlers();
});
