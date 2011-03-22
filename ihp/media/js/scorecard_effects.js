function create_tooltip(target_object, options)
{
	default_options = {
		baseClass: 'callout-to',
		position: 'right',
		offset: [0, 10]
	};
	options = jQuery.extend(default_options, options);
	jQuery(target_object).simpletip(options);
}

jQuery(document).ready(function()
{
	// Disable animation in browsers that require the IE VML hack,
	// because polling for object size changes eats too much CPU 
	// and resizing objects causes positioning bugs in IE7.
	
	if (!jQuery.browser.msie || jQuery.browser.version >= 9)
	{
		jQuery('.infobox .item').hide();
		
		jQuery('.infobox h2 a').click(function()
		{
			var toShow = jQuery(this).closest('.infobox').children('.item');
			jQuery(toShow).slideToggle();
			return false;
		});
	}
		
	// Attach callouts to their content using Simpletip
	jQuery('.callout-from').each(function(i, callout_from)
	{
		// load content from the DIV with the same ID plus "_content"
		create_tooltip(jQuery(callout_from),
			{content: jQuery('#' + callout_from.id + "_content").html()});
	});
});