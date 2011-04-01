<?php
/**
 * Template Name: Homepage
 */
 ?>
<?php get_header(); ?>
<?php if (have_posts()) : while (have_posts()) : the_post(); ?>
<?php
	// use the new post_class() function if it's available
	if (function_exists('post_class')) {
?>
<div class="section top">
	<div <?php post_class('entry'); ?> id="intro">
	  <?php } else { ?>
	  <div class="entry" id="post-<?php the_ID(); ?>">
		<?php } ?>
		<h2>
		  <?php the_title(); ?>
		</h2>
		<div class="content">
		  <?php the_content(); ?>
		  <?php wp_link_pages(array('before' => '<p><strong>Pages:</strong> ', 'after' => '</p>', 'next_or_number' => 'number')); ?>
		</div>
	  </div>
	  <!-- end entry -->
	  <?php endwhile; else: ?>
	  <div class="error">
		<h1>Not Found</h1>
		<p>Sorry, we couldn't find the page you were looking for. Perhaps you'd like to search for it?</p>
		<?php include (TEMPLATEPATH . '/searchform.php'); ?>
	  </div>
	  <?php endif; ?>
	  <div class="featured-content"><img class="image-1" src="<?php bloginfo('template_url'); ?>/images/scorecards.png" alt="scorecards" /></div>
	  <div class="icons"></div>
	  </div><!--end top section-->

</div><!--end #content-->

	  <div class="section bottom">
	  	<div id="home-bottom">

		  <?php if ( function_exists('dynamic_sidebar') && dynamic_sidebar('home bottom') ) : else : ?>insert widgets into home bottom here<?php endif; ?>

<?php if (function_exists('simple_social_bookmarks')) : ?>
<div id="social-bookmarks">
Share this page with:
<?php echo simple_social_bookmarks('','','',
	'iconfolder=../../plugins/simple-social-bookmarks/default'); ?>
</div>
<?php endif; ?>

		</div>
		  <?php get_sidebar(); ?>
	  </div><!--end #home-bottom-->
	  

<?php get_footer(); ?>
