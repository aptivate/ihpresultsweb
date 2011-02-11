=== HTML Page Sitemap ===
Contributors: Angelo Mandato of the PluginsPodcast.com
Donate link: http://www.pluginspodcast.com/contact/
Tags: sitemap, page, pages, shortcode, cms, static, short code, map, pagemap, site, html
Requires at least: 2.7.0
Tested up to: 3.0
Stable tag: 1.1.1

Adds an HTML (Not XML) sitemap of your blog pages (not posts) by entering the shortcode [html-sitemap], perfect for those who use WordPress as a CMS.

== Description ==
This simple plugin adds an HTML (Not XML) sitemap of your blog pages (not posts) by entering the shortcode [html-sitemap] in the page content. This simple plugin is configured from the shortcode. Settings include the `sort_column`, `sort_order`, `exclude`, `include`, `depth`, `child_of`, `meta_key`, `meta_value`, `authors`, `number`, and `offset`. You can set essentially everything you can set in the wp_list_pages function.

This plugins is perfect for those who use WordPress as a CMS.

First example shows how to add the sitemap in its simplest form.

`[html-sitemap]`

Example shortcode will add a sitemap to a page displaying a depth limit of 3 and exclude page ID 708.

`[html-sitemap depth=3 exclude=708]`

Example shortcode will add a sitemap to a page displaying only children and grandchildren of the current page.

`[html-sitemap depth=2 child_of=CURRENT]`

Last example shortcode will add a sitemap displaying the page modified date with the pages sorted by the menu order number.

`[html-sitemap show_date=modified sort_column=menu_order]`


Please see the [Template Documentation for the `wp_list_pages` function](http://codex.wordpress.org/Template_Tags/wp_list_pages) for detailed documentation of the available attributes and their values.

For the latest information visit the website.

[http://www.pluginspodcast.com/plugins/html-page-sitemap/](http://www.pluginspodcast.com/plugins/html-page-sitemap/)

== Frequently Asked Questions ==

 = Why is there no settings page for the plugin? =
 I put together this plugin in less than 2 hours, this readme.txt actually took longer to create. This plugin is meant to be simple and easy to use. To keep it simple, it doesn't add settings to your database or clutter to your admin screens.
 
== Installation ==
1. Copy the entire directory from the downloaded zip file into the /wp-content/plugins/ folder.
2. Activate the "HTML Page Sitemap" plugin in the Plugin Management page.
3. Add the shortcode [html-sitemap] to the page(s) of your choice.
		
== Screenshots ==
1. HTML Page Sitemap in the Default WordPress theme.

== Changelog ==

= 1.1.1 =
* Released 6/27/2010
* HTML Sitemap compatiable with latest versions of WordPress 2.9 and 3.0.

= 1.1.0 =
* Released on 11/24/2009
* Fixed typos in readme
* Added child_of options
** child_of=CURRENT (starts list of pages that are children of the current page)
** child_of=PARENT (starts list of pages that are of the same level as current page)

= 1.0.0 =
* Released on 09/05/2009
* Initial release of HTML Page Sitemap plugin.


== Contributors ==
Angelo Mandato, CIO [RawVoice](http://www.rawvoice.com) and host of the [Plugins Podcast](http://www.pluginspodcast.com) - Plugin author

== Follow us on Twitter == 
[http://twitter.com/pluginspodcast](http://twitter.com/pluginspodcast)
