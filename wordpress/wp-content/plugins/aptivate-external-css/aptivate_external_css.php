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
	function wp_head()
	{
		em_showContent("starthead", "endhead",
			"http://localhost/django/public/scorecard/agency/UNICEF/",
			"", FALSE);
	}
}

add_action('wp_head', array('AptivateExternalCSS', 'wp_head'));
