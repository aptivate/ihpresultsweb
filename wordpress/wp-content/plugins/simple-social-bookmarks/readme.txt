=== Simple Social Bookmarks ===
Contributors: dartiss
Donate link: http://artiss.co.uk/donate
Tags: social, bookmark, bookmarking, simple, sexy, addtoany, shareaholic, addthis, twitter, facebook, myspace, mail, email, pdf, capture, screen, google, yahoo, gmail, print, printer, post,page, russia, japan, china, buzz, bebo, baidu, linkedin, hotmail, netlog, vybralisme, furl, diigo, multiply, hatena, livejournal, identica, favoriten, linkuj, digg, tumblr, livedoor, friendfeed, yandex, de.lirio.us, delirious, friendster, sonico, informazione, typepad, muti, reddit
Requires at least: 2.0.0
Tested up to: 3.0.3
Stable tag: 3.0

Simple Social Bookmarks adds icons to your posts and/or pages that allow your visitors to easily submit them on social bookmarking and network sites. 

== Description ==

**Please note, if upgrading from a version previous to 3.0:**
**Version 3 has changed some of the existing service names and icon filenames - please check the version history for further details. In addition, the standard icon set has changed.**

Simple Social Bookmarks is an easy but powerful way to implement Social Bookmarking on your WordPress blog. It has links to over 200 Social Bookmarking networks - more than any other plugin - and is fully XHTML standards compliant.

Many non-English bookmarking sites are included - particularly Russian, Chinese and Japanese. Because of the use of icons and a lack of an administration screen, Simple Social Bookmarks does not require translation to other languages.

It will display a row of social bookmarking icons wherever you add its code - for an individual post and page or in a sidebar. They are split between bookmarking services and tools (e.g. printing, converting to PDF, etc).

**For help with this plugin, or simply to comment or get in touch, please read the appropriate section in "Other Notes" for details. This plugin, and all support, is supplied for free, but [donations](http://artiss.co.uk/donate "Donate") are always welcome.**

The code for Simple Social Bookmarks should be added to your theme's code where required. In the case of posts this should be within "the loop".

Here is an example on use...

`<?php echo simple_social_bookmarks('','','padding-left: 5px; padding-right: 5px','iconfolder=24x24'); ?>`

There are 4 parameters in total that can be specified, but all are optional.

The first parameter is the URL that you wish the social sites to bookmark. If left blank (and this is probably the default for most people) it will use the URL of the current post or page.

The second parameter is where you can specify a shortened URL to bookmark (if you have one available). To maintain backward compatibility with previous version of this plugin, the URL must begin with "http" to be accepted. At the moment Twitter, Identica and Blip will be passed shortened URLs. If you think any other services should be included, please [let me know](http://www.artiss.co.uk/contact "Contact Me").

The third parameter is a style definition which applies to the bookmark icons. This should, where possible, not be used in preference to using CSS definitions. Instead each element generated has a `class` of `ssb` so that it can be defined via your own stylesheet. The separator `class` is `ssb_sep`.

Finally, the fourth parameter can contain a number of options, all of which are separated by an ampersand. These options are as follows...

**default=**
This should be `on`, `off` or `basic` and defines which social bookmarks should display by default. `on` means all should display, `off` means none should be displayed and `basic` shows a basic few. Not specifying this sub-parameter will cause the basic set to be displayed.

**iconfolder=**
If not specified, a default set of 16x16 pixel icons will be used. If, however, you'd like to use your own icons then you will need to add a sub-folder in your theme folder and then use this parameter to specify the sub-folders name. In the above example, I am specifying a sub-folder named `24x24`.
Icons should all have a `.PNG` extension and the file names must match the bookmarking service name, as specified below. Bookmarking services are shown first and tools afterwards.

**priority=**
Allows you to specify whether a bookmark link should be via AddThis (1), Shareaholic (2) or AddtoAny (3) (if a link via more than one is available). This is defined by providing a series of numbers representing the order of the services. So, a priority of 231 would be Shareaholic first, followed by AddToAny and then AddThis. The default priority is 123.

**nofollow=**
By default, `REL=NOFOLLOW` will be added to all links. However, if this is specified as `NO` then this will be deactivated.

**target=**
Allows you to specify a `TARGET`. By default this is not used.

**separator=**
If you wish to display a separator image between the bookmark and icon lists then you must specify `separator=Yes`. An image named `separator.png` will then be displayed. If using your own folder for images then this image will be required as well.

**id=**
If using the animation option (see the later section) then a unique ID must be specified for each set of social bookmarks on the screen. If there is only one set of bookmarks per post and page, then the best option is to pass the post ID via `get_the_ID()`. By default, no ID is specified so animation is turned off.

There are also options for EACH of the social bookmarking services allowing you to specify whether they should be turned on or off. So, for example, to turn Digg off, you would specify `digg=off`.

So, as a further example, if you ONLY wanted the Delicious and Digg bookmarks to appear, it would be best to specify the `default` as `off` and then turn Delicious and Digg on individually, like so...

`<?php echo simple_social_bookmarks('','','','default=off&delicious=on&digg=on'); ?>`

The full list of social bookmark services are listed separately.

If an alternative name is specified in brackets, this is the one that should be used in the aforementioned options.

The basic set of services are as follows...

Delicious, Digg, Email, Facebook, LinkedIn, Print Friendly (Print), reddit, StumbleUpon and Twitter.

Here is a further version of the original example, but this time with a check to confirm that the plugin is active...

`<?php if (function_exists('simple_social_bookmarks')) : ?>
<?php echo simple_social_bookmarks('','','padding-left: 5px; padding-right: 5px','iconfolder=24x24'); ?>
<?php endif; ?>`

**Adding To Your Feed**

It's possible to add the Social Bookmarks to your WordPress feed. Open up your `functions.php` file within your theme folder and add the following code...

`<?php
function insertRss($content) {
    if ((is_feed())&&(function_exists('simple_social_bookmarks'))) {
        $content = $content."<p>".simple_social_bookmarks('','','padding-left: 2px; padding-right: 2px','iconfolder=16x16')."</p>";
    }
    return $content;
}
add_filter('the_content', 'insertRss');
?>`

Obviously, you will need to modify the parameters that are passed to the Simple Social Bookmarks plugin, to make it appropriate for yourself. In the above example you may notice that I'm using an alternative set of icons with a small padded space between them.

**Animation**

A basic animation option is available and is switched on by providing a unique ID parameter (see earlier details).

Once specified, hovering over a bookmark option will switch it from the standard icon to another with `_hov` on the end.

For instance, hovering over `twitter.png` will switch the image to `twitter_hov.png`. When you move away, it will return to the original image. This extra image will need to exist in the same folder as the first.

However, although basic, it can be used for all sorts of effects, such as black & white icons becoming coloured when hovered over or icons that expand in size.

Here is an example where I'm switching on the animation option by specifying a unique ID...

`<?php echo simple_social_bookmarks('','','padding-left: 2px; padding-right: 2px','separator=Yes&id='.get_the_ID()); ?>`

Animation can also be performed by modifying the stylesheet. The following example will cause the images to move up by 5 pixels whenever they are hovered over, in a similar way  to the SexyBookmarks or Simple Social plugins.

`.ssb img, .ssb_sep {
    padding-top: 5px;
    padding-bottom: 0;
    padding-left: 5px;
    padding-right: 5px
}
.ssb img:hover {
    padding-top: 0;
    padding-bottom: 5px;
}`

== Installation ==

1. Upload the entire `simple-social-bookmarks` folder to your `wp-content/plugins/` directory.
2. Activate the plugin through the 'Plugins' menu in WordPress.
3. There is no options screen - configuration is done in your code.

== Available Bookmarking Services ==

Any of the following bookmarking services can be used...

100zakladok, a1webmarks, addthis, addtoany, allvoices, amazon_ca, amazon_de, amazon_fr, amazon_jp, amazon_uk, amazon_us, aollifestream, aolmail, baang, baidu, balatarin, barrapunto, bebo, bibsonomy, biggerpockets, bitacoras, blinklist, blip, blogger, bloggy, bloglines, blogmarks, blogpoint, blogtercimlap, blurpalicious, bobrdobr, bonzobox, bookmark_it, bookmarks_fr, bookmarky_cz, boxdotnet, bryderi, businessweek, buzzfeed, buzzurl, care2, choix, citeulike, clply, comments, connotea, corank, cosmiq, current, dailyme, dealsplus, delicious, digg, diggita, diggitsport, dihitt, diigo, dipdive, dotnetkicks, douban, dzone, edelight, ekudos, evernote, facebook, fark, faves, favoriten_de, fc2bookmark, flaker, fnews, folkd, forceindya, friendfeed, friendster, funp, ghidoo, globalgrind, googlebookmarks, googlebuzz, googlenotebook, grono, grumper, gwar, habergentr, hackernews, hadashhot, hatena, hazarkor, healthimize, hedgehogs, hotklix, icio, identica, igoogle, informazione, jamespot, jumptags, kaboodle, kledy, laaikit, ladenzeile, linkarena, linkedin, linkninja, linkter, linkuj, livedoor, livejournal, mawindo, mekusharim, memori, meneame, messenger, misterwong, misterwong_de, mixx, moemesto, mototagz, msdn, msnreporter, multiply, muti, myaol, mylinkvault, myshare, myspace, n4g, netlog, netvibes, newsing, newsvine, niftyclip, ning, nowpublic, nujij, oknotizie, orkut, pfbuzz, pingfm, plaxo, plurk, pochvalcz, posterous, pratiba, preferate, pusha, quantcast, reader, readitlater, readwriteweb, reddit, rediff, redkum, scoopat, scoopeo, sekoman, shaveh, sinaweibo, slashdot, smiru, socialbookmarkingnet, socialdotcom, socialdust, sodahead, sonico, soupio, spurl, squidoo, startlap, studivz, stumbleupon, stylehive, supr, svejo, swik, tagvn, technet, technorati, thefreedictionary, thisnext, tuenti, tulinq, tumblr, tweetmeme, twitter, typepad, upnews, urlaubswerkde, viadeo, virb, visitezmonsite, vk, vodpod, vybralisme, webnews, webnews_de, wikio, wikio_fr, wikio_it, windycitizen, wink, winlivespaces, wists, wordpress, wovre, wykop, xanga, xing, yahoobookmarks, yahoobookmarks_jp, yahoobuzz, yahoobuzz_fr, yahoomessenger, yandex, yardbarker, yigg and zakladoknet.

In addition, the following tools can be used....

2tag, aviarycapture, bitly, domaintoolswhois, email, gmail, googletranslate, hootsuite, hotmail, instapaper, isgd, jmp, joliprint, osxdashboard, page2rss, pdfmyurl, pdfonline, printfriendly, qrf_in, tinyurl, w3validator, windowsgadgets and yahoomail.

== Licence ==

This WordPRess plugin is [GPLv2 compatible](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html "GNU General Public License, version 2").

== Support ==

All of my plugins are supported via [my website](http://www.artiss.co.uk "Artiss.co.uk").

Please feel free to visit the site for plugin updates and development news - either visit the site regularly, follow [my news feed](http://www.artiss.co.uk/feed "RSS News Feed") or [follow me on Twitter](http://www.twitter.com/artiss_tech "Artiss.co.uk on Twitter") (@artiss_tech).

For problems, suggestions or enhancements for this plugin, there is [a dedicated page](http://www.artiss.co.uk/simple-social-bookmarks "Simple Social Bookmarks") where you can leave comments. 

Alternatively, please [contact me directly](http://www.artiss.co.uk/contact "Contact Me"). 

**This plugin, and all support, is supplied for free, but [donations](http://artiss.co.uk/donate "Donate") are always welcome.**

== Frequently Asked Questions ==

= The Social Bookmarking site is not appearing =

If you've not specified `default=on` then new sites will not appear - you will need to specifically switch it on.

Here's an example of switching on Google Buzz...

`<?php echo simple_social_bookmarks('','','padding-left: 5px; padding-right: 5px','googlebuzz=on'); ?>`

= Where can I find some alternative icons? =

The icons provided with the plugin are the standard icons for each of the sites (usually the site's favicon). There are many good, free collections available. However, none have the full set that this plugin uses, which is why I use this generic group.

None-the-less, most people will probably only want to display a few, popular, sites and therefore various icon collections will be ideal.

My favourites include [Vector Social Media Icons](http://icondock.com/free/vector-social-media-icons "Vector Social Media Icons") by IconDock and [Social Network Icon Pack](http://www.komodomedia.com/download/ "Social Network Icon Pack") by Komodo Media.

Alternatively, read [75 Beautiful Free Social Bookmarking Icon Sets](http://www.bloggodown.com/2009/07/75-beautiful-free-social-bookmarking.html "75 Beautiful Free Social Bookmarking Icon Sets") from Blog Godown or [21 Sets of Free Social Bookmarking Icons for Your Blog](http://www.wpzoom.com/design/21-sets-of-free-social-bookmarking-icons-for-your-blog/ "21 Sets of Free Social Bookmarking Icons for Your Blog") from wpzoom.

= You haven't included my favourite Social Bookmarking service =

I keep a huge database of over 500 bookmarking services. However, I only use those that appear to be the most popular, based on Google search results. If you think I have missed one of great importance, please [get in contact with me](http://www.artiss.co.uk/contact "Contact Me") and plead your case!

= Now that this plugin doesn't have it's own URL shortening, how can I do this? =

There are many shortening plugins available to do this, including my own [Simple URL Shortener](http://www.artiss.co.uk/simple-url-shortener "Simple URL Shortener"). Simply call one of these first and get the shortened URL - you can then pass this as the second parameter into Simple Social Bookmarks.

Here is an example of how to get a bit.ly short URL with Simple URL Shortener...

`if (function_exists('simple_url_shortener')) {$shorturl=simple_url_shortener('','bit.ly');}`

== Screenshots ==

1. An example of the plugin in use, showing colour and movement animation
2. A full list of the default icons

== Changelog ==  
  
= 1.0 =  
* Initial release

= 1.1 =
* Now XHTML compliant

= 1.2 =
* Fixed issue with ampersands (and probably other characters) in the blog title causing linking issues
* Added su.pr as another URL shortening service

= 1.3 =
* Updated default icons to a set kindly provided by komodomedia.com (With the exception of the AddToAny and Ping.FM icons)
* Added AddToAny, Ping.fm, Google Bookmarks, Google Reader and email to the list of providers. By default these will be turned off so as to not to suddenly appear on existing installs and cause problems!
* Further improvement to blog title issues
* Removed URL shortening on all services with the exception of Twitter, as it was not required and may have even have caused some issues (such as some services not being able to get hold of thumbnails and general page content).
* Now using [Simple URL Shortener](http://wordpress.org/extend/plugins/simple-url-shortener/ "Simple URL Shortener") plugin to provide URL shortening
* Caching of short URLs now takes place providing large performance improvements
* NOFOLLOW and TARGET parameters added
* Compressed default icons

= 1.4 =
* Removed caching, as this is now handled by [Simple URL Shortener](http://wordpress.org/extend/plugins/simple-url-shortener/ "Simple URL Shortener"). Please ensure you update to the latest version of this plugin to ensure that caching continues to work - once you know it does, the cache folder for this plugin can be removed.
* Added additional parameter - cache=
* Tidied code and updated shared functions

= 1.5 =
* Use different encoding for email links
* Added Technorati to the list of providers. By default this will be turned off (including using the default=on option) so as to not to suddenly appear on existing installs.

= 1.6 =
* Added Yahoo! Bookmarks, Yahoo! Buzz and Google Buzz to the list of providers. By default these will be turned off (including using the default=on option) so as to not to suddenly appear on existing installs.

= 1.7 =
* Icon folders are now stored in the theme directory, to prevent them from being deleted whenever the plugin is updated
* API key and user details can now be passed to shortening services
* Added new 'default' parameter setting - this should not impact existing installation unless you've explicitly requested 'default=on'.

= 1.8 =
* Added new, official, link for Google Buzz

= 2.0 =
* Re-written base code
* Added LOTS of new social services
* Help file re-written

= 3.0 =
* Another re-write of the base code
* There are now 218 bookmarking services and 23 tools available
* Now uses AddToAny, AddThis and Shareaholic for the majority of links
* Removed use of Simple URL Shortener plugin - you now pass the shortened URL yourself, allowing any shortening plugin to be used
* Split bookmark service definition function to a separate file
* Output HTML comments containing plugin information
* Added new parameter - priority - to allow user to give priority to one sharing service
* New default icons
* Existing icon filenames changed  (ffeed is now friendfeed, ybuzz is now yahoobuzz, gbuzz is now googlebuzz and print is now printfriendly)
* The bookmark service previously named ping.fm is now named pingfm
* Removed Twitter text parameter (no longer used) and replaced with the ability to pass a shortened URL
* Propeller has been removed as it is no longer available
* Separated bookmarks and tools - added optional new separator icon
* Used smush.it to compress images (23% average reduction)
* The default is now for `REL=NOFOLLOW` to be on for all links generated to ensure maximum SEO optimisation.
* The default for the `target` is now for it not to be specified (and therefore be XHTML valid)
* Added a default CLASS to all elements plus an ID to the images
* Added basic animation effect, allowing you to switch between two images
* Improved the instructions and spell checked them for once!

== Upgrade Notice ==

= 1.5 =
* Upgrade if you use the email option, as this will fix a problem with the text encoding
* Also added Technorati as a social bookmarking service

= 1.6 =
* Upgrade if you want to use the Yahoo! Bookmarks, Yahoo! Buzz or Google Buzz social bookmarking services

= 1.7 =
* Upgrade if you want to use a shortening service that requires an API key or logon

= 1.8 =
* Upgrade is you use the Google Buzz service

= 2.0 =
* Upgrade for new services and to benefit from improved coding

= 3.0 =
* Major update adding dozens of new bookmarks, an animation options and removal of URL shortening