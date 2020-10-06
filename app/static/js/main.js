$(document).ready(function(){
	var $grid = $('.grid').masonry({
		gutter: 30
	});
	  // layout Masonry after each image loads
	$grid.imagesLoaded().progress( function() {
		$grid.masonry('layout');
	});

	$('.grid-item').click(function(){
		var image_data = $(this).data(image);
		var image = image_data.image;
		var description = `<p>${image.description}</p>`;
		var title = `<h5 class="modal-title">${image.name}<i class="fa fa-times" class="close" data-dismiss="modal" aria-label="Close" aria-hidden="true"></i></h5>`;
		var img = `<img src="${image.upload_location}" alt="${image.name}" />`;
		$('#image-modal .modal-body').html(img + title + description);
		$('.modal').modal('show');
	});

	$('i.like').bind('click', function() {

		var like 		= $(this).hasClass('not-liked');
		var image_id 	= $(this).data('image');
		var _this 		= $(this);

		$.getJSON($SCRIPT_ROOT + '/like', {
			like: like,
			image_id: image_id
		}, function(result) {
			console.log('line 29');
			if (result == 'true') {
				if (like) {
					_this.removeClass('far');
					_this.removeClass('not-liked');
					_this.addClass('fas');
					_this.addClass('liked');
				} else {
					_this.removeClass('fas');
					_this.removeClass('liked');
					_this.addClass('far');
					_this.addClass('not-liked');
				}
			}
		});
		return false;
	});

});