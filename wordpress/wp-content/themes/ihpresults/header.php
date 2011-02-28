<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="<?php bloginfo('html_type'); ?>; charset=<?php bloginfo('charset'); ?>" />
<meta name="google-site-verification" content="gYQQirkNB_vFxoawYVk9T07_33ILZmObRGT37w8RVaI" />
<title><?php
	if ( is_search() ) { echo "Search for $s"; }
	if ( is_404() ) { echo "404: Page Not Found"; }
	wp_title('');
	if ( is_archive() ) { echo " archive "; }
	if ( !is_home() ) { echo " at "; }
	bloginfo('name');
?></title>
<?php
	// Get custom theme options set in the admin area, or use the defaults
	global $dojomenu_options;
	foreach ($dojomenu_options as $value) {
		if (get_option( $value['id'] ) === FALSE) { $$value['id'] = $value['std']; } else { $$value['id'] = get_option( $value['id'] ); }
	}
?>
<link rel="stylesheet" href="<?php bloginfo('stylesheet_url'); ?>" type="text/css" media="screen" />
<?php if ( $dojo_use_custom_styles == 'true' ) { ?>
	<link rel="stylesheet" href="<?php bloginfo('template_url'); ?>/custom.css" type="text/css" media="screen" />
<?php }; ?>
<link rel="stylesheet" href="<?php bloginfo('template_url'); ?>/print.css" type="text/css" media="print" />
<!--[if lte IE 6 ]>
	<link rel="stylesheet" href="<?php bloginfo('template_url'); ?>/ie6bugs.css" type="text/css" media="screen" />
	<?php if ( $dojo_use_custom_styles == 'true' ) { ?>
		<link rel="stylesheet" href="<?php bloginfo('template_url'); ?>/customie6bugs.css" type="text/css" media="screen" />
	<?php }; ?>
<![endif]-->
<!--[if IE 7 ]>
	<link rel="stylesheet" href="<?php bloginfo('template_url'); ?>/ie7bugs.css" type="text/css" media="screen" />
	<?php if ( $dojo_use_custom_styles == 'true' ) { ?>
		<link rel="stylesheet" href="<?php bloginfo('template_url'); ?>/customie7bugs.css" type="text/css" media="screen" />
	<?php }; ?>
<![endif]-->
<link rel="alternate" type="application/atom+xml" title="<?php bloginfo('name'); ?> Full Posts" href="<?php bloginfo('atom_url'); ?>" />
<link rel="alternate" type="application/atom+xml" title="<?php bloginfo('name'); ?> Comments" href="<?php bloginfo('comments_atom_url'); ?>" />
<?php
	// add comments feed on single-post pages
	if (is_single()) {
		while (have_posts()) : the_post();
			if ('open' == $post->comment_status) : /* If comments are open */
?>
<link rel="alternate" type="application/atom+xml" title="Comments on <?php the_title(); ?>" href="<?php bloginfo('url'); ?>/index.php?feed=atom&amp;p=<?php the_ID(); ?>" />
<?php
			endif;
		endwhile;
		rewind_posts();
	// add category feed on category archives
	} else if (is_category()) {
		$category = get_the_category(); 
?>
<link rel="alternate" type="application/atom+xml" title="Posts in the <?php echo $category[0]->cat_name; ?> category" href="<?php echo get_category_feed_link( $category[0]->cat_ID, 'atom' ); ?>" />
<?php
	// add tag feed on tag archives
	} else if (is_tag()) {
?>
<link rel="alternate" type="application/atom+xml" title="Posts tagged with <?php single_tag_title(); ?>" href="<?php echo get_tag_feed_link( get_query_var('tag_id'), 'atom' ); ?>" />
<?php
	// add author feed on author pages
	} else if (is_author()) {
		if(isset($_GET['author_name'])) :
		$curauth = get_userdatabylogin($author_name);
		else :
		$curauth = get_userdata(intval($author));
		endif;
		$authorfeedlink = get_author_feed_link( $curauth->ID, 'atom' );
	?>
<link rel="alternate" type="application/atom+xml" title="Posts by <?php echo $curauth->display_name; ?>" href="<?php echo $authorfeedlink; ?>" />
<?php
	}
?>
<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />
<?php
	if ( is_singular() ) wp_enqueue_script( 'comment-reply' );
	wp_head();
?>
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-20361977-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</head>
<body <?php if(function_exists('body_class')) { body_class(); } ?>>

<div id="header">
<div id="branding">
	<?php if ( is_home() ) { /* use an h1 on the homepage */ ?>
	<h1 id="blogname"><a href="<?php bloginfo('url'); ?>"><?php bloginfo('name'); ?></a></h1>
	<?php } else { /* and a p tag everywhere else */ ?>
	<p id="blogname"><strong><a href="<?php bloginfo('url'); ?>"><?php bloginfo('name'); ?></a></strong></p>
	<?php } ?>
	<p id="tagline"><em><?php bloginfo('description'); ?></em></p>
</div>
<div id="access">
	<div id="access-inner">
  <?php /*  Allow screen readers / text browsers to skip the navigation menu and get right to the good stuff */ ?>
	<div class="skip-link screen-reader-text"><a href="#content" title="<?php esc_attr_e( 'Skip to content', 'ihpresults' ); ?>">
                 <?php _e( 'Skip to content', 'twentyten' ); ?></a></div>
	<?php /* Our navigation menu.  If one isn't filled out, wp_nav_menu falls back to wp_page_menu.  The menu assiged to the primary position is 
                 the one used.  If none is assigned, the menu with the lowest ID is used.  */ ?>
	<?php wp_nav_menu( array( 'container_class' => 'menu-header', 'theme_location' => 'primary' ) ); ?>
	<div id="results">
    	<div class="results-inner">
    		 <h2>Find results by:</h2>
    		 <?php wp_nav_menu( array( 'container_class' => 'menu-header', 'theme_location' => 'secondary' ) ); ?>
				<?php get_search_form(); ?>
    	</div>
	</div><!-- #results -->
	</div><!-- #access-inner -->

</div><!-- #access -->
</div> <!-- end header -->



<div id="wrapper">

<div id="wrapper-inner">
	<div id="content">