$(document).ready(function() {
	$("#add").click(function() {
		$('.to_duplicate:last').clone(true).insertAfter('.to_duplicate:last');
		$justInserted = $('.to_duplicate:last');
		$justInserted.hide();
		$justInserted.find('input').val(''); // it may copy values from first one
		$justInserted.find('input').attr('style','');
		$justInserted.find('label').attr('style','');
		$justInserted.slideDown(500);
	});

	$(".remove_line").each(function() {
		$(this).bind("click",function() {
			if($('.to_duplicate').size() > 1) {  
				parent_duplicate = $(this).closest('.to_duplicate');
				parent_duplicate.slideUp("normal", function(){$(this).remove();});
			}
		})
	});

	$('#filters_checkbox').on('change', function() {
		var box = $('#filters_hidden_box')
		if (box.is( ":hidden" ) ) {
			box.show("slow");
		} else {
			box.slideUp();
		}
    });	
});
