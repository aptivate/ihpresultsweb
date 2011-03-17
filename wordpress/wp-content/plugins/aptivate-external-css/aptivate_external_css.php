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
		if (preg_match('#^/scorecard/(partner|country)/([-\w %0-9]+)(/)?$#',
			$_SERVER['REQUEST_URI']))
		{
			em_showContent("starthead", "endhead",
				"http://localhost/django/public".$_SERVER["REQUEST_URI"]."/",
				"", FALSE);
		}
	}
	function enqueue_scripts()
	{
		if (preg_match('#^/scorecard/(partner|country)/([-\w %0-9]+)(/)?$#',
			$_SERVER['REQUEST_URI']))
		{
			wp_enqueue_script("jquery");
		}
	}
}

add_action('wp_head', array('AptivateExternalCSS', 'head'));
add_action('wp_enqueue_scripts', array('AptivateExternalCSS', 'enqueue_scripts'));
