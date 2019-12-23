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

	$("#export").click(function(){
		concept = $(this).data('concept')
		console.log(concept)
		$.ajax({
			url : '/export_JSON',
			dataType: "text",
			data: {'data': concept},
			type: 'POST',
			success:function(exported_json){ 
				$('#exported_json').text(exported_json)
			}
			});


	})
})


