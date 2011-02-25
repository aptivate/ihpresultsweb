<?php
/*
Plugin Name: Basic-SEO
Plugin URI: http://jonathanbullock.com/projects/basic-seo
Description: Applies basic search engine optimisations to your WordPress powered site.
Version: 0.3
Author: Jonathan Bullock
Author URI: http://jonathanbullock.com
License: GPL2
*/

/*  Copyright 2010  Jonathan Bullock  (email : jonbullock@gmail.com)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License, version 2, as 
    published by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

/*

TODO:
- Allow customisation of output via control panel page
- Customisation to be made via template code (%n = name etc,)
- Allow additional content (i.e. google verify header) to be output
- Add support for using custom fields in output for "pages"

*/

function basic_seo_title($text) {
	$name = get_bloginfo('name');
	
	if (is_feed()) {
		// leave feed title along
	} else {
		if (is_single()) {
			while (have_posts()) : the_post();
				$text = single_post_title('', false) . " | " . $name;
			endwhile;
			rewind_posts();
		} elseif (is_page()) {
			while (have_posts()) : the_post();
				$text = the_title('', false) . " | " . $name;
			endwhile;
			rewind_posts();
		} elseif (is_category()) {
			$text = "Category: " . single_cat_title('', false) . " | " . $name;
		} elseif (is_tag()) {
			$text = "Tag: " . single_tag_title(' ', false) . " | " . $name;
		} elseif (is_date()) {
			$text = "Archive: " . single_month_title(' ', false) . " | " . $name;
		} else {
			$text = $name;
		}
	}
	
	return $text;
}

add_filter( 'wp_title', 'basic_seo_title' );

function basic_seo_head() {
	echo "<!-- Basic-SEO start -->\n";
	
	$name = get_bloginfo('name');
	$desc = get_bloginfo('description');
	
	if (is_single()) {
		while (have_posts()) : the_post();
			$desc = strip_tags(get_the_excerpt());
			echo "<meta name=\"description\" content=\"$desc\" />\n";
			$tag_text = "";
			$post_tags = get_the_tags();
			if ($post_tags) {
				foreach($post_tags as $tag) {
					$tag_text .= $tag->name . ', ';
				}
				$tag_text = substr($tag_text, 0, (strlen($tag_text)-2));
			}
			echo "<meta name=\"keywords\" content=\"$tag_text\" />\n";
		endwhile;
		rewind_posts();
	} elseif (is_category()) {
		$cat = single_cat_title('', false);
		echo "<meta name=\"description\" content=\"Posts assigned to the category: $cat\" />\n";
		echo "<meta name=\"keywords\" content=\"$cat\" />\n";
	} elseif (is_tag()) {
		$tag = single_tag_title('', false);
		echo "<meta name=\"description\" content=\"Posts marked with the tag: $tag\" />\n";
		echo "<meta name=\"keywords\" content=\"$tag\" />\n";		
	} elseif (is_date()) {
		$date = single_month_title(' ', false);
		echo "<meta name=\"description\" content=\"Posts for the date: $date\" />\n";
		echo "<meta name=\"keywords\" content=\"$date\" />\n";
	} else {
		echo "<meta name=\"description\" content=\"$name : $desc\" />\n";
	}
	
	echo "<!-- Basic-SEO end -->\n";
}

add_action( 'wp_head', 'basic_seo_head' );

?>