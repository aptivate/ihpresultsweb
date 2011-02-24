=== Display Widgets ===
Contributors: sswells
Donate link: http://blog.strategy11.com/donate/
Tags: widget, widgets, admin, show, hide, page, Thesis, sidebar, content, wpmu, wordpress, plugin, post, posts, content
Requires at least: 2.8
Tested up to: 3.0.1
Stable tag: 1.14

Simply hide widgets on specified pages. Adds checkboxes to each widget to either show or hide it on every site page.

== Description ==

Change your sidebar content with different pages. Avoid creating multiple sidebars and duplicating widgets by adding check boxes to each widget in the admin (as long as it is written in the WordPress version 2.8 format) which will either show or hide the widgets on every site page. Great for use with the [Thesis WordPress Theme](http://blog.strategy11.com/thesis "Thesis WordPress Theme") (aff link), or just to avoid extra coding. 

By default, 'Hide on Checked' is selected with no boxes checked, so all current widgets will continue to display on all pages. 

== Installation ==

1. Upload `display-widgets.php` to the `/wp-content/plugins/` directory
2. Activate the plugin through the 'Plugins' menu in WordPress
3. Go to the 'Widgets' menu and show the options panel for the widget you would like to hide.
4. Select either 'Show on Checked' or 'Hide on Checked' from the drop-down and check the boxes.


== Frequently Asked Questions ==

= Why aren't the options showing up on my widget? =

This is a known limitation. Widgets written in the pre-2.8 format don't work the same way, and don't have the hooks. Sorry.


== Screenshots ==

1. The extra widget options added.

== Changelog ==
= 1.14 =
* Added Japanese translation

= 1.13 = 
* Added a PO file for translators

= 1.12 =
* Show only published pages, and increase the displayed page limit
* Toggle sections
* Added check boxes to hide/show for logged-in users
* Added text field to list post ids for posts not displayed

= 1.11 =
* WordPress 3.0 compatibility
* Fixed PHP notices

= 1.10 =
* Improved admin widget page efficiency and load time
* Fixed bug preventing widgets from being hidden/shown correctly on some subpages

= 1.9 =
* Add check box for front page
* Change category checkbox to apply not only to the category page, but also to posts in that category

= 1.8 =
* Added check box for search page under "Miscellaneous"

= 1.7 =
* Update for 2.9 compatibility

= 1.6 =
* Added category checkboxes

= 1.5 =
* Added "404 Page" checkbox

= 1.4 =
* Changed "Home Page" check box to "Blog Page"

= 1.3 =
* Added check box for Home page if it is the blog page
* Added check boxes for single post and archive pages
* Save hide/show option correctly for more widgets

= 1.2 =
* Save page check boxes for more widgets

= 1.1 =
* Fixed bug that prevented other widget options to be displayed

