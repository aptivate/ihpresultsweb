=== External markup ===
Contributors: Henrik Box
Tags: framework, external content
Requires at least: 2.7.1
Tested up to: 2.8.2
Stable tag: trunk

== Description ==
Retrieve markup from external websites based on html-comments.
The plugin creates htmlfiles that are inserted into the templates
where the function call is made. Uses CURL or fOPEN to retrive the
external content. Also checks the age of the htmlfile using filemtime
and compares it to the option "em_external_src_cache".
 
== Installation ==
The markup from external source must be tagged with specific html-comments.
Plugin retrives markup from start/end comments.
 
The htmlfile path is default set to /themes/TEMPLATENAME/em_cache/
Create folder /themes/TEMPLATENAME/em_cache/ and make it writeable (chmod 777)
 
The file external_markup_functions.php must be included in the template functions.php.
Copy the file external_markup_functions.php into your template folder.
 
Example: include_once (TEMPLATEPATH . '/external_markup_functions.php');

Example:
For retriving navigation markup from http://www.tv4.se;
Function call in template:  em_showContent("main-navigation start","main-navigation end",EM_EXAMPLE,FALSE)
 
Explanation of function call:
em_showContent(HTML-COMMENT-START,HTML-COMMENT-END,DEFINE HTMLFILENAME,COMPRESS)
 
- em_showContent is the function (found in external_markup_functions.php)
- HTML-COMMENT-START, the start html-comment
- HTML-COMMENT-END, the end html-comment
- DEFINE HTMLFILENAME, the name definition of the htmlfile (see documentation in external_markup_functions.php)
- COMPRESS, should the htmlfile be compressed (FALSE/TRUE) - use with caution!

== 

Websites that are using this plugin:
http://stylebykling.tv4.se/
http://lundh.fotbollskanalen.se/
http://sciencefictionbloggen.tv4.se/	