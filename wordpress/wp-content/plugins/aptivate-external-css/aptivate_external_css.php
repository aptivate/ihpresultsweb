<?php
/*
Plugin Name: Aptivate External CSS
Description: Retrieve parts of external content and include in HTML HEAD
Author: Aptivate
Version: 1.0
Author URI: http://aptivate.org
*/

class AptivateExternalCSS
{
	function head()
	{
		em_showContent("starthead", "endhead",
			"http://localhost/django/public/scorecard/agency/UNICEF/",
			"", FALSE);
	}
	function enqueue_scripts()
	{
		wp_enqueue_script("jquery");
	}
}

add_action('wp_head', array('AptivateExternalCSS', 'head'));
add_action('wp_enqueue_scripts', array('AptivateExternalCSS', 'enqueue_scripts'));
