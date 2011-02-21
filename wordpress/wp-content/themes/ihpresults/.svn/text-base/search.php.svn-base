<?php get_header(); ?>

<?php
	// Get custom theme options set in the admin area, or use the defaults
	global $dojomenu_options;
	foreach ($dojomenu_options as $value) {
		if (get_option( $value['id'] ) === FALSE) { $$value['id'] = $value['std']; } else { $$value['id'] = get_option( $value['id'] ); }
	}
?>

<?php if (have_posts()) : ?>

<h1 class="archive">Search Results for &#8220;<?php the_search_query(); ?>&#8221;</h1>

<?php $posts=query_posts($query_string . '&showposts=25'); ?>
<?php while (have_posts()) : the_post(); ?>

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
	<h2><a href="<?php echo get_permalink() ?>"><?php the_title(); ?></a></h2>
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
	<p><?php the_excerpt_rss(); /* just like the_excerpt, but really strips all the HTML, including BR tags */ ?></p>
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

<hr />

<?php endwhile; ?>

<div class="navigation">
	<div class="prev"><?php next_posts_link('Older Entries') ?></div>
	<div class="next"><?php previous_posts_link('Newer Entries') ?></div>
</div>

<?php else: ?>

<div class="error">
	<h1>Not Found</h1>
	<p>Sorry, we couldn't find the content you were looking for. Perhaps you'd like try a different search?</p>
	<?php include (TEMPLATEPATH . '/searchform.php'); ?>
</div>

<?php endif; ?>
</div> <!-- end content -->


<?php get_footer(); ?>