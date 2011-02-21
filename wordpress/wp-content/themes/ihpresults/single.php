<?php get_header(); ?>

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
	<h1><?php the_title(); ?></h1>
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



<?php endwhile; else: ?>



<?php endif; ?>


<?php get_sidebar(); ?>

<?php get_footer(); ?>
