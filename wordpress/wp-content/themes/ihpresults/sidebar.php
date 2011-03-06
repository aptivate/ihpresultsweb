<hr />
<div id="sidebar">
		<?php if ( !function_exists('dynamic_sidebar') || !dynamic_sidebar('sidebar') ) : ?>

			<div id="search" class="widget widget_search">
				<h2>Search</h2>
				<?php get_search_form(); ?>
			</div><!-- end search -->

			<div id="pages" class="widget widget_pages">
				<h2>Pages</h2>
				<ul>
					<?php wp_list_pages('title_li='); ?>
				</ul>
			</div><!-- end pages -->

			<div id="tag_cloud" class="widget widget_tag_cloud">
				<h2>Popular Tags</h2>
				<?php // In a perfect world, we would wrap popular tags in more and more EMs, but this will do for now. ?>
				<?php wp_tag_cloud('smallest=.75&largest=1.75&unit=em&format=list&number=20'); ?>
			</div><!-- end tag_cloud -->

			<div id="meta" class="widget widget_meta">
				<h2>Meta</h2>
				<ul>
					<?php wp_register(); ?>
					<li><?php wp_loginout(); ?></li>
					<li><? echo "$numposts" ?> entries</li>
					<li><? echo "$numcomms" ?> comments</li>
					<?php wp_meta(); ?>
				</ul>
			</div><!-- end meta -->

		<?php endif; ?>

</div> <!-- end sidebar -->