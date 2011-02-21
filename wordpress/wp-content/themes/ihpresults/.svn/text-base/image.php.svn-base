<?php get_header(); 
/*

	This is lifted directly from the version of the default theme that ships
	with WP 2.5.1. I've cleaned it up a bit, but it doesn't seem to work quite
	right. Perhaps once the documentation has been updated, I'll come back and
	tweak this to work better. - SV

*/
?>

<?php
	// Get custom theme options set in the admin area, or use the defaults
	global $dojomenu_options;
	foreach ($dojomenu_options as $value) {
		if (get_option( $value['id'] ) === FALSE) { $$value['id'] = $value['std']; } else { $$value['id'] = get_option( $value['id'] ); }
	}
?>

<?php if (have_posts()) : while (have_posts()) : the_post(); ?>

<?
	// set the post date to variables for use in link functions below
	$arc_year = get_the_time('Y');
	$arc_month = get_the_time('m');
	$arc_day = get_the_time('d');
?>

<?php
	// use the new post_class() function if it's available
	if (function_exists('post_class')) {
?>
	<div <?php post_class('entry'); ?> id="post-<?php the_ID(); ?>">
<?php } else { ?>
	<div class="entry" id="post-<?php the_ID(); ?>">
<?php } ?>

<div class="title">
	<h1><a href="<?php echo get_permalink() ?>"><?php the_title(); ?></a></h1>
	<?php
		// Prepare the byline, which will be output either here or in the footer
		ob_start(); 
	?>
		<p class="byline"><small>
			<?php if ( $dojo_byline_in_title != 'true' ) { comments_popup_link('<strong>0</strong> Comments.', '<strong>1</strong> Comment.', '<strong>%</strong> Comments.', 'commentlink', 'Comments are off.'); } ?>
			Posted 
			by <?php the_author_posts_link(); ?>
			on <?php the_time('l'); ?>,
			<a href="<?php echo get_month_link("$arc_year", "$arc_month"); ?>"><?php the_time('F j'); ?></a>,
			<a href="<?php echo get_year_link("$arc_year"); ?>"><?php the_time('Y'); ?></a>
			at <?php the_time(); ?>.
			<?php if ( $dojo_byline_in_title == 'true' ) { comments_popup_link('<strong>0</strong> Comments.', '<strong>1</strong> Comment.', '<strong>%</strong> Comments.', 'commentlink', 'Comments are off.'); } ?>
			<?php edit_post_link('Edit this entry.'); ?>
		</small></p>
	<?
		$dojo_byline = ob_get_contents();
		ob_end_clean();	
		// Show or hide the byline based on admin option.
		if ( $dojo_byline_in_title == 'true' ) { echo $dojo_byline; }
	?>
</div>

<div class="content">
	<p class="attachment"><a href="<?php echo wp_get_attachment_url($post->ID); ?>"><?php echo wp_get_attachment_image( $post->ID, 'medium' ); ?></a></p>
	<div class="caption"><?php if ( !empty($post->post_excerpt) ) the_excerpt(); // this is the "caption" ?></div><!-- end caption -->
	<?php the_content(); ?>
	<?php wp_link_pages(array('before' => '<p><strong>Pages:</strong> ', 'after' => '</p>', 'next_or_number' => 'number')); ?>
</div>

<div class="metadata">
	<?php
		// Show or hide the byline based on admin option.
		if ( $dojo_byline_in_title != 'true' ) { echo $dojo_byline; } 
		// Show or hide the categories based on admin option.
		if ( $dojo_disable_categories != 'true' ) {
			echo "<p class=\"folksonomy\"><small>Filed under ";
			the_category(', ');
			if (get_the_tags()) the_tags(', ',', ');
			echo ".</small></p>";
		} else {
			if (get_the_tags()) the_tags('<p class="folksonomy"><small>Filed under ',', ','.</small></p>');
		}
	?>
</div>

</div><!-- end entry -->

<?php comments_template(); ?>

<hr />

<ul class="navigation">
	<?php /*
		I'm not sure if this is correct usage of previous_image_link, there's 
		no documentation for it yet. I'm assuming it works like previous_post_link.
	*/ ?>
	<?php previous_image_link('<li class="prev"><small>Previously:</small> %link</li>') ?>
	<?php next_image_link('<li class="next"><small>Next Up:</small> %link</li>') ?>
</ul>

<?php endwhile; else: ?>

<div class="error">
	<h1>Not Found</h1>
	<p>Sorry, we couldn't find the image you were looking for. Perhaps you'd like to search for it?</p>
	<?php include (TEMPLATEPATH . '/searchform.php'); ?>
</div>

<?php endif; ?>
</div> <!-- end content -->

<?php get_sidebar(); ?>

<?php get_footer(); ?>