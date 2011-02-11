<?php
/*
Plugin Name: HTML Page Sitemap
Plugin URI: http://www.pluginspodcast.com/plugins/html-page-sitemap/
Description: <a href="http://www.pluginspodcast.com/plugins/html-page-sitemap/" target="_blank">HTML Page Sitemap</a> Adds an HTML (Not XML) sitemap of your blog pages (not posts) by entering the shortcode [html-sitemap]. A plugin from <a href="http://www.pluginspodcast.com/" target="_blank">Plugins: The WordPress Plugins Podcast</a>.
Version: 1.1.1
Author: Angelo Mandato
Author URI: http://www.pluginspodcast.com/
Change Log:
	See readme.txt for complete change log

Contributors:
	Angelo Mandato, CIO RawVoice and host of the PluginsPodcast.com - Plugin author
	
Copyright 2009=2010 Angelo Mandato, host of the Plugins Podcast (http://www.pluginspodcast.com)

License: GPL (http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)
*/


/*
	Add the sitemap when shortcode is encountered
	@param $args - arguments or attributes specified in the shortcode tag.
	@param $content - not used
	@return the page sitemap or empty string if not applicable.
*/
function html_sitemap_shortcode_handler( $args, $content = null )
{
	if( is_feed() )
		return '';
		
	$args['echo'] = 0;
	$args['title_li'] = '';
	unset($args['link_before']);
	unset($args['link_after']);
	if( isset($args['child_of']) && $args['child_of'] == 'CURRENT' )
		$args['child_of'] = get_the_ID();
	else if( isset($args['child_of']) && $args['child_of'] == 'PARENT' )
	{
		$post = &get_post( get_the_ID() );
		if( $post->post_parent )
			$args['child_of'] = $post->post_parent;
		else
			unset( $args['child_of'] );
	}
	
	$html = wp_list_pages($args);

	// Remove the classes added by WordPress
	$html = preg_replace('/( class="[^"]+")/is', '', $html);
	return '<ul>'. $html .'</ul>';
}

add_shortcode('html-sitemap', 'html_sitemap_shortcode_handler');

?>