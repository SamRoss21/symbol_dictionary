$(document).ready(function(){
	$(".delete").click(function(){
		id = $(this).data('id')
		image = $(this).data('image')
		word = $(this).data('word')
		concept = $(this).data('concept')
		$("#"+id).remove()

		$.ajax({
			url : '/deleteImage',
			dataType: "json",
			data: {'image': image, 'word': word, 'concept': concept},
			type: 'POST',
			});

	})
})


