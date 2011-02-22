<?php /*
Template Name: Archives Template
This is heavily based on the archives template from the K2 theme: http://getk2.com/
*/

// Count the posts, comments, and categories on your blog
$numposts = $wpdb->get_var("SELECT COUNT(1) FROM $wpdb->posts WHERE post_status = 'publish' AND post_type != 'page'");
if (0 < $numposts) $numposts = number_format($numposts); 

$numcomms = $wpdb->get_var("SELECT COUNT(1) FROM $wpdb->comments WHERE comment_approved = '1'");
if (0 < $numcomms) $numcomms = number_format($numcomms);

// Get custom theme options set in the admin area, or use the defaults
global $dojomenu_options;
foreach ($dojomenu_options as $value) {
	if (get_option( $value['id'] ) === FALSE) { $$value['id'] = $value['std']; } else { $$value['id'] = get_option( $value['id'] ); }
}

?>

<?php get_header(); ?>

<div class="entry" id="site-archives">

<div class="title">
	<h1><a href="<?php echo get_permalink() ?>"><?php the_title(); ?></a></h1>
</div>

<div class="content">

	<p>
		You are viewing the archives at <?php bloginfo('name'); ?>, 
		which contain <?php echo $numposts ?> posts and <?php echo $numcomms ?> comments. 
		You can flip through the tag cloud or browse the monthly archives below, 
		or you could try using the search form if you're looking for something in particular.
	</p>
	
	<div id="site-archives-search-form">
		<h2>Search the <?php bloginfo('name'); ?> Archives</h2>
		<?php include (TEMPLATEPATH . '/searchform.php'); ?>
	</div>

	<div id="site-archives-tag-cloud">
		<h3>Top 100 Tags</h3>
		<?php wp_tag_cloud('smallest=.75&largest=1.75&unit=em&format=list&number=100'); ?>
	</div><!-- end tag-cloud -->

	<div id="site-archives-monthly-archive" class="<?php echo ($dojo_disable_categories == 'true') ? "wide" : ""; ?>">
		<h3>Monthly Archive</h3>
		<?php
			// based on code from http://www.z-oc.com/blog/2008/02/a-powerful-archive-page-for-your-wordpress-blog/
			$prev_date = NULL;
			$date = NULL;
			query_posts("posts_per_page=-1&order=DESC");
			if (have_posts()) : while (have_posts()) : the_post();
				$date  = get_the_time('m.Y');
				$year  = get_the_time('Y');
				$month = get_the_time('m');
				$baseUrl = get_bloginfo('URL');
				if($date != $prev_date) {
					if ($prev_date) echo "</ul>\n";
					$prev_date = $date;
					echo "<h4><a href='" . get_month_link("$year", "$month") . "'>" . get_the_time('F Y') . "</a></h4>\n";
					echo "<ul>\n";
				}
		?>
		<li><a href="<?php the_permalink() ?>"><?php the_title() ?></a></li>
		<?php
			endwhile;
			echo "</ul>\n";
			endif;
		?>
	</div><!-- end monthly-archive -->

	<?php
		// Show or hide the category archive based on admin option.
		if ( $dojo_disable_categories != 'true' ) { ?>
			<div id="site-archives-category-archive">
				<h3>Category Archive</h3>
				<ul>
					<?php wp_list_cats('hierarchical=0&optioncount=1'); ?>
				</ul>
			</div><!-- end category-archive -->
		<?php }
	?>

</div><!-- end content -->

</div><!-- end entry -->
</div> <!-- end content -->

<?php get_sidebar(); ?>

<?php get_footer(); ?>