$(function () {
	$(".nav-toggle").on("click", function () {
		if ($(".nav-item").hasClass("active")) {
			$(".nav-item").removeClass("active");
		} else {
			$(".nav-item").addClass("active");
		}
	});
});