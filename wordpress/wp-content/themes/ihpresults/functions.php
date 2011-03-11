<?php
if ( function_exists('register_sidebar') ) {
	// have to register the sidebars separately so I can name them uniquely - SV
	register_sidebar( array(
		'name' => 'header',
		'before_widget' => '<div id="%1$s" class="widget %2$s">',
		'after_widget' => '</div><!-- end widget -->',
		'before_title' => '<h2>',
		'after_title' => '</h2>',
	));
	register_sidebar( array(
		'name' => 'home bottom',
		'before_widget' => '<div id="%1$s" class="widget %2$s">',
		'after_widget' => '</div><!-- end widget -->',
		'before_title' => '<h2>',
		'after_title' => '</h2>',
	));
	register_sidebar( array(
		'name' => 'sidebar',
		'before_widget' => '<div id="%1$s" class="widget %2$s">',
		'after_widget' => '</div><!-- end widget -->',
		'before_title' => '<h2>',
		'after_title' => '</h2>',
	));
	
}

// This theme uses wp_nav_menu() in three location.
	register_nav_menus( array(
		'primary' => __( 'Primary Navigation', 'ihp' ),
));

	register_nav_menus( array(
		'secondary' => __( 'Secondary Navigation', 'ihp' ),
));

	register_nav_menus( array(
		'tertiary' => __( 'Tertiary Navigation', 'ihp' ),
));

		

	// This theme uses post thumbnails
	add_theme_support( 'post-thumbnails' );
	
	if ( function_exists( 'add_image_size' ) )
	add_theme_support( 'post-thumbnails' );



// Display the links to the extra feeds such as category feeds
remove_action( 'wp_head', 'feed_links_extra', 3 );

// Display the links to the general feeds: Post and Comment Feed
remove_action( 'wp_head', 'feed_links', 2 );

/*
	Custom Threaded Comments code to be used with wp_list_comments
*/
function dojo_comments($comment, $args, $depth) {
	$GLOBALS['comment'] = $comment; ?>
	<li <?php comment_class(); ?> id="li-comment-<?php comment_ID() ?>">
		<div id="comment-<?php comment_ID(); ?>">
			<p class="title comment-author vcard">
				<?php echo get_avatar($comment,$size='48' ); ?>
				<?php printf(__('<cite class="fn">%s</cite> <span class="says">says:</span>'), get_comment_author_link()) ?>
			</p>
			<?php if ($comment->comment_approved == '0') : // If comment is not approved ?>
				<p class="alert"><em><?php _e('Your comment is awaiting moderation.') ?></em></p>
			<?php endif; ?>
			<div class="content">
				<?php comment_text() ?>
			</div>
			<p class="metadata comment-meta commentmetadata"><small>
				Posted on <a href="<?php echo htmlspecialchars( get_comment_link( $comment->comment_ID ) ) ?>"><?php printf(__('%1$s at %2$s'), get_comment_date(),  get_comment_time()) ?></a>.
				<?php comment_reply_link(array_merge( $args, array('reply_text' => '(Reply)', 'depth' => $depth, 'max_depth' => $args['max_depth']))) ?>
				<?php edit_comment_link(__('(Edit)'),'  ','') ?>
			</small></p>
		</div>
	<?php
}

/*
	Subscribe Widget
	Uses atom feeds - to use RSS2, just change 'atom' to 'rss2'.
*/
function widget_dojo_subscribe( $args ) {
	global $post;
	extract( $args );
	echo "\n$before_widget\n";
	echo $before_title . "Subscribe" . $after_title . "\n"; ?>
		<p>Grab an Atom feed:</p>
		<ul class="rss">
			<li><a href="<?php bloginfo('atom_url'); ?>">Full Entries</a></li>
			<li><a href="<?php bloginfo('comments_atom_url'); ?>">All Comments</a></li>
			<?php
				// add comments feed on single-post pages
				if (is_single()) {
					while (have_posts()) : the_post();
						if ('open' == $post->comment_status) : /* If comments are open */
			?>
			<li><a href="<?php bloginfo('url'); ?>/index.php?feed=atom&amp;p=<?php the_ID(); ?>">Comments on &ldquo;<?php the_title(); ?>&rdquo;</a></li>
			<?php
						endif;
					endwhile;
					rewind_posts();
				// add category feed on category archives
				} else if (is_category()) {
					$category = get_the_category(); 
			?>
			<li><a href="<?php echo get_category_feed_link( $category[0]->cat_ID, 'atom' ); ?>">Posts in the &ldquo;<?php echo $category[0]->cat_name; ?>&rdquo; category</a></li>
			<?php
				// add tag feed on tag archives
				} else if (is_tag()) {
			?>
			<li><a href="<?php echo get_tag_feed_link( get_query_var('tag_id'), 'atom' ); ?>">Posts tagged with &ldquo;<?php single_tag_title(); ?>&rdquo;</a></li>
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
			<li><a href="<?php echo $authorfeedlink; ?>">Posts by <?php echo $curauth->display_name; ?></a></li>
			<?php
				}
			?>
		</ul>
	<?php echo "$after_widget\n";
}
if ( function_exists('register_sidebar_widget') )
	register_sidebar_widget('Subscribe (dojo)', 'widget_dojo_subscribe');



?>