$(document).ready(function(){
	$(".delete").click(function(){
		concept = $(this).data('concept')
		$("#"+concept).remove()

		$.ajax({
			url : '/deleteConcept',
			dataType: "json",
			data: {'data': concept},
			type: 'POST',
			});

	})
})

