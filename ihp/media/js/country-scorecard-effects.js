jQuery(document).ready(function()
{
	jQuery('.infobox .item').hide();
	jQuery('.infobox h2 a').click(function(){
		var toshow = jQuery(this).closest('.infobox').children('.item');
		var tohide = jQuery('.infobox .item').not(toshow);
		tohide.slideUp();
		toshow.slideDown();
	});
});
