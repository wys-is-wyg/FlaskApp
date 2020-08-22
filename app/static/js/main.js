$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	$('[data-toggle="popover"]').popover();
	
	var $grid = $('.grid').masonry({
		gutter: 30
	});
	  // layout Masonry after each image loads
	$grid.imagesLoaded().progress( function() {
		$grid.masonry('layout');
	});
});