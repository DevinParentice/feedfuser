$(document).ready(function () {

	$('#file-input').change(function () {
		$("form[name=image-form]").trigger('submit');
	});

	$("form[name=image-form]").submit(function (e) {
		var $form = $(this);
		var $error = $form.find(".error");
		var data = $form.serialize();
		let files = new FormData();

		files.append('profile-pic', $('#file-input')[0].files[0]);

		$.ajax({
			url: "/dashboard/",
			type: "POST",
			processData: false,
			contentType: false,
			data: files,
			dataType: "json",
			success: function (resp) {
				window.location.replace('/dashboard')
			},
			error: function (resp) {
				$error.text(resp.responseJSON.error).removeClass("error-hidden");
			}
		});

		e.preventDefault();
	});
});