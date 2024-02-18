$(document).ready(function(){

    $('.folder-link').click(function(){
        $('.folder').addClass('d-none')
       
        $($(this).data('id')).removeClass('d-none')
    })


    $('#id_profile_image').change(function () {
        // Get the selected file
        var fileInput = $(this)[0];
        var file = fileInput.files[0];

        if (file) {
            // You can access file properties such as name, size, type, etc.
            console.log('Selected file:', file.name, ', Size:', file.size, ', Type:', file.type);
            const $linkContainer = $(".img-link")
            var reader = new FileReader();
            reader.onload = function (e) {
                $('.img-account-profile').attr('src', e.target.result);
                $linkContainer.append(`<p class="h6">${file.name} ${file.size} ${file.type}</p>`)

            };
            reader.readAsDataURL(file);
        }
    });
})