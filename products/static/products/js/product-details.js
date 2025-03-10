$(document).ready(function () {
	var reviewBox = $("#post-review-box");
	var newReview = $("#new-review");
	var openReviewBtn = $("#open-review-box");
	var closeReviewBtn = $("#close-review-box");
	var ratingsField = $("#ratings-hidden");

	// Open Review Form
	openReviewBtn.click(function (e) {
		e.preventDefault();
		reviewBox.removeClass("hidden").slideDown(400, function () {
			newReview.focus();
		});
		openReviewBtn.fadeOut(100);
		closeReviewBtn.removeClass("hidden");
		addStars("#post-review-box");
	});

	// Close Review Form
	closeReviewBtn.click(function (e) {
		e.preventDefault();
		reviewBox.slideUp(300, function () {
			openReviewBtn.fadeIn(200);
		});
		closeReviewBtn.addClass("hidden");
		$(".starrr i").remove();
	});

	// Function to Add Dynamic Star Ratings
	function addStars(parent, rating = 0) {
		let starContainer = $(`${parent} .starrr`);
		starContainer.html(""); // Clear previous stars

		for (let i = 1; i <= 5; i++) {
			let isActive = i <= rating ? "fa-solid text-yellow-500" : "fa-regular text-gray-400";
			starContainer.append(
				`<i value="${i}" class="fa-star cursor-pointer text-xl ${isActive}"></i>`
			);
		}

		// Hover Effect
		starContainer.find("i").on("mouseover", function () {
			let val = $(this).attr("value");
			ratingsField.val(val); // Update hidden input value

			starContainer.find("i").each(function () {
				$(this).toggleClass("fa-solid text-yellow-500", $(this).attr("value") <= val);
				$(this).toggleClass("fa-regular text-gray-400", $(this).attr("value") > val);
			});
		});

		// Click Event (Set Rating)
		starContainer.find("i").on("click", function () {
			let val = $(this).attr("value");
			ratingsField.val(val); // Update hidden input value

			starContainer.find("i").each(function () {
				$(this).toggleClass("fa-solid text-yellow-500", $(this).attr("value") <= val);
				$(this).toggleClass("fa-regular text-gray-400", $(this).attr("value") > val);
			});
		});
	}

	// Open Edit Modal with Data
	$(document).on("click", ".edt-btn", function () {
		let reviewText = $(this).closest(".review-card").find(".review-text").text();
		let reviewRating = $(this).closest(".review-card").find(".fa-star.fa-solid").length;
		openReviewBtn.click(); // Open Review Box
		newReview.text(reviewText);
		ratingsField.val(reviewRating);
		addStars("#post-review-box", reviewRating);
		$([document.documentElement, document.body]).animate(
			{
				scrollTop: $(".review-form").offset().top - 200,
			},
			2000
		);
	});

	$("#message-cancel-delete").click(function () {
		$("#message-delete-confirm-modal").addClass("hidden");
	});

	// Handle delete message
	$(document).on("click", ".delete-btn", function () {
		let messageId = $(this).data("id");

		$("#message-delete-confirm-modal").removeClass("hidden");

		$("#message-confirm-delete").click(function () {
			$.ajax({
				url: `/products/delete_review/${messageId}`,
				type: "DELETE",
				headers: { "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val() },
				success: function (response) {
					$(`.delete-btn`)
						.closest(".review-card")
						.fadeOut(300, function () {
							$(this).remove();
						});
					$("#message-delete-confirm-modal").addClass("hidden");
				},
				error: function () {
					location.reload();
				},
			});
		});
	});

	// AJAX Submit Review
	$(document).on("submit", ".review-form", function (e) {
		e.preventDefault();
		var formData = $(this).serialize();
		$.ajax({
			type: "POST",
			url: $(this).data("url"),
			data: formData,
			success: function (response) {
				location.reload();
			},
			error: function (response) {
				console.log(response);
			},
		});
	});
});
