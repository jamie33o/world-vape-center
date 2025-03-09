$(document).ready(function () {
	$("#nl_form").submit(function (e) {
		e.preventDefault(); // Prevent form from refreshing the page

		let formData = $(this).serialize(); // Serialize form data
		let formUrl = $(this).attr("action"); // Get the form URL

		$.ajax({
			type: "POST",
			url: formUrl,
			data: formData,
			dataType: "json",
			success: function (response) {
				$("#nl_message")
					.removeClass("hidden text-red-500")
					.addClass("text-green-500")
					.text(response.message);
				$("#nl_form")[0].reset(); // Clear the form
			},
			error: function (xhr) {
				let errorMsg = "An error occurred. Please try again.";

				if (xhr.responseJSON && xhr.responseJSON.error) {
					errorMsg = xhr.responseJSON.error;
				}

				$("#nl_message")
					.removeClass("hidden text-green-500")
					.addClass("text-red-500")
					.text(errorMsg);
			},
		});
	});

	// Show Age Verification Modal if not previously accepted
	if (!localStorage.getItem("ageVerified")) {
		$("#age-modal").removeClass("hidden");
	}

	$("#age-verified").click(function () {
		localStorage.setItem("ageVerified", "true"); // Save verification
		$("#age-modal").addClass("hidden");
	});

	// Show Cookies Modal if not accepted
	if (!localStorage.getItem("cookiesAccepted")) {
		$("#cookies-modal").removeClass("hidden");
	}

	$("#cookies-accept").click(function () {
		localStorage.setItem("cookiesAccepted", "true"); // Save acceptance
		$("#cookies-modal").addClass("hidden");
	});

	$(".user-menu-button").click(function (event) {
		event.stopPropagation(); // Prevents event bubbling
		$(".user-menu").toggleClass("hidden").toggleClass("opacity-0").toggleClass("opacity-100");
		$(".chev-down").toggleClass("rotate-180");
	});

	// Close menu when clicking outside
	$(document).click(function (event) {
		if (!$(event.target).closest(".user-menu, .user-menu-button").length) {
			$(".user-menu").addClass("hidden").removeClass("opacity-100").addClass("opacity-0");
			$(".chev-down").removeClass("rotate-180");
		}
	});

	$(".new-message").parent().removeClass("hidden");

	// Auto fade out messages after 3 seconds
	setTimeout(function () {
		$("[data-message]").fadeOut(500, function () {
			$(this).addClass("hidden"); // Fully hide after fadeout
		});
	}, 3000);

	// Allow manual dismiss of messages
	$(".dismiss-message").click(function () {
		$("[data-message]").fadeOut(500, function () {
			$(this).addClass("hidden"); // Fully hide after fadeout
		});
	});

	// Mobile menu
	$(".menu-btn").click(function () {
		$("body").css("overflow", "hidden");
		$(".mobile-menu-container").removeClass("translate-x-full").addClass("translate-x-0");
		$(".mobile-menu-overlay").removeClass("opacity-0").addClass("opacity-100");
	});

	$(".close-menu").click(function () {
		$("body").css("overflow", "auto");
		$(".mobile-menu-container").removeClass("translate-x-0").addClass("translate-x-full");
		$(".mobile-menu-overlay").removeClass("opacity-100").addClass("opacity-0");
	});

	$(".more-btn").click(function (e) {
		e.preventDefault();

		// Toggle dropdown
		$(".more-dropdown").toggleClass("hidden");

		// Rotate icon
		$(".more-icon").toggleClass("rotate-180");
	});

	// Hide dropdown when clicking outside
	$(document).click(function (event) {
		if (!$(event.target).closest(".more-btn, .more-dropdown").length) {
			$(".more-dropdown").addClass("hidden");
			$(".more-icon").removeClass("rotate-180");
		}
	});

	let searchInput = $(".large-search-form .search-input");
	let text = [
		"Search for vape products...",
		"Find your favorite e-liquid!",
		"Discover new flavors today...",
		"Explore top-rated devices!",
		"Start your vaping journey...",
	]; // Change this to whatever text you want
	let index = 0;
	let lineIndex = 0;
	if (window.innerWidth > 1022) {
		let typingEffect = setInterval(function () {
			// If the input is still empty, keep adding letters
			if (searchInput.val() === "" && index < text[lineIndex].length) {
				searchInput.attr("placeholder", text[lineIndex].substring(0, index + 1));
				index++;
			} else if (searchInput.val() !== "") {
				// Stop typing effect if user types manually
				clearInterval(typingEffect);
				searchInput.attr("placeholder", "search...");
			} else {
				index = 0;
				searchInput.attr("placeholder", "");
				if (lineIndex >= text.length - 1) {
					lineIndex = 0;
				} else {
					lineIndex++;
				}
			}
		}, 200); // Adjust speed (300ms per letter)
	}

	$(".search-btn").click(function () {
		$(".mobile-search-form")
			.toggleClass("max-h-[500px] opacity-100")
			.toggleClass("max-h-0 opacity-0");
		$(".mobile-search-form").find("input").focus();
	});
});
