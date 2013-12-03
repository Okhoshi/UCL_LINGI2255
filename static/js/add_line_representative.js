$(document).ready(function() {
	$("#add").click(function() {
		$('.to_duplicate:last').clone(true).insertAfter('.to_duplicate:last');
		$justInserted = $('.to_duplicate:last');
		$justInserted.hide();
		$justInserted.find('input').val(''); // it may copy values from first one
		$justInserted.slideDown(500);
	});
});