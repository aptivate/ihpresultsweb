function create_tooltip(target_object, options)
{
	default_options = {
		baseClass: 'callout-to',
		position: 'right',
		offset: [10, 0]
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
	jQuery('.callout-from').add('.has-callout-below').each(function(i, callout_from)
	{
		// load content from the DIV with the same ID plus "_content"
		options = {content: jQuery('#' + callout_from.id + "_content").html()};
		callout_from_jquery = jQuery(callout_from);
		
		if (callout_from_jquery.hasClass('has-callout-below'))
		{
			options.position = 'bottom';
			options.offset = [0, 10];
		}
		
		create_tooltip(callout_from_jquery, options);
	});
});