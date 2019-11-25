$(document).ready(function(){
	$(".delete").click(function(){
		word = $(this).data('word')
		concept = $(this).data('concept')
		$("#"+word).remove()

		$.ajax({
			url : '/deleteSearchWord',
			dataType: "json",
			data: {'word': word, 'concept': concept},
			type: 'POST',
			});

	})
})


