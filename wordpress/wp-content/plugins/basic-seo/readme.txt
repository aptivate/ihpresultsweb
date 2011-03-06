=== Basic-SEO ===
Contributors: jonbullock
Donate link: http://jonathanbullock.com/about/donate/
Tags: seo, search engine optimization, headers, title, meta, meta keywords, meta description
Requires at least: 3.0
Tested up to: 3.0.1
Stable tag: trunk

Applies basic search engine optimisations to your WordPress powered site.

== Description ==

Applies the following simple search engine optimisations to your blog:

* Shows "Site Title" in page title always no matter what content your viewing
* Shows any content descriptor (page/post title etc.) first in page title
* Uses post excerpt as value of "description" meta tag
* Uses post tags as value of "keywords" meta tag
* Uses tag name as value of "keywords" meta tag when viewing posts for a tag
* Uses category name as value of "keywords" meta tag when viewing posts for a category
* Uses date as value of "keywords" meta tag when viewing posts for a date

That's it really, pretty simple stuff.

== Installation ==

1. Upload basic-seo.php to the "/wp-content/plugins/" directory
2. Activate the plugin through the 'Plugins' menu in WordPress
3. Place `<?php wp_title(); ?>` inside the <title></title> tags in header.php for your template if not already there (should be the only content)
4. Place `<?php wp_head(); ?>` somewhere inside the <head></head> tags in header.php for your template if not already there

== Changelog ==
= 0.3 (19/09/10) =
* Fixed output of description meta tag when it contains html
= 0.2 (15/08/10) =
* Fixed title output for feeds.
= 0.1 (10/08/10) =
* Plugin released.
