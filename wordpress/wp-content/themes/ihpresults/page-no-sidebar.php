<?php
/**
 * Template Name: No sidebar
 */
 ?>


<?php get_header(); ?>

<?php if (have_posts()) : while (have_posts()) : the_post(); ?>

<?php
	// use the new post_class() function if it's available
	if (function_exists('post_class')) {
?>
	<div <?php post_class('entry'); ?> id="post-<?php the_ID(); ?>">
<?php } else { ?>
	<div class="entry" id="post-<?php the_ID(); ?>">
<?php } ?>

	<h1><?php the_title(); ?></h1>

<div class="content">
	<?php the_content(); ?>
	<?php wp_link_pages(array('before' => '<p><strong>Pages:</strong> ', 'after' => '</p>', 'next_or_number' => 'number')); ?>
</div>

<?php edit_post_link('Edit this page.', '<div class="metadata"><p class="byline"><small>', '</small></p></div>'); ?>

</div><!-- end entry -->

<?php endwhile; else: ?>

<div class="error">
	<h1>Not Found</h1>
	<p>Sorry, we couldn't find the page you were looking for. Perhaps you'd like to search for it?</p>
	<?php include (TEMPLATEPATH . '/searchform.php'); ?>
</div>

<?php endif; ?>
</div> <!-- end content -->

<?php get_footer(); ?>