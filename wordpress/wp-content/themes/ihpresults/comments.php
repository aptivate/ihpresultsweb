<?php // Do not delete these lines
	if (!empty($_SERVER['SCRIPT_FILENAME']) && 'comments.php' == basename($_SERVER['SCRIPT_FILENAME']))
		die ('Please do not load this page directly. Thanks!');
	if ( post_password_required() ) {
		echo '<p class="nocomments">This post is password protected. Enter the password to view comments.</p>';
		return;
	}
/* You can start editing here. */ ?>

<hr />

<div class="comments">

	

	<?php if ('open' == $post->comment_status) : /* If comments are open */ ?>
	
		<p class="syndicate"><small><em>You can track this conversation through its <a href="<?php bloginfo('url'); ?>/index.php?feed=atom&amp;p=<?php the_ID(); ?>">atom feed</a>.</em></small></p>
	<?php endif; ?>

	<?php if ( have_comments() ) : /* If there are comments */ ?>
		<?php if ( function_exists('wp_list_comments') ) : /* use new threaded comments */ ?>
			<ol class="commentlist">
				<?php wp_list_comments('style=ol&callback=dojo_comments'); ?>
			</ol>
			<?php if ( get_option('page_comments') ) : ?>
				<div class="navigation">
					<div class="prev"><?php previous_comments_link("Older Comments") ?></div>
					<div class="next"><?php next_comments_link("Newer Comments") ?></div>
				</div>
			<?php endif; ?>
		<?php else : /* use old unthreaded comments */ ?>
			<ol class="commentlist">
				<?php foreach ($comments as $comment) : ?>
					<?php
						/* Check if comment email is the same as the post author's, and add the 'authorcomment' class if so */
						$authorcomment = '';
						if ( $comment->comment_author_email == get_the_author_email() )
							$authorcomment = ' authorcomment';
					?>
					<li <?php echo "class=\"comment$oddcomment$authorcomment\""; ?> id="comment-<?php comment_ID() ?>">
						<p class="title">
							<?php echo get_avatar( $comment, 48 ); ?>
							<cite><?php comment_author_link() ?></cite> says:
						</p>
						<?php if ($comment->comment_approved == '0') : // If comment is not approved ?>
							<p class="alert"><em>Your comment is awaiting moderation.</em></p>
						<?php endif; ?>
						<div class="content">
							<?php comment_text() ?>
						</div>
						<p class="metadata"><small>
							Posted on <a href="#comment-<?php comment_ID() ?>"><?php comment_date('F jS, Y') ?> at <?php comment_time() ?></a>.
							<?php edit_comment_link('(edit)','&nbsp;&nbsp;'); ?>
						</small></p>
					</li>
					<?php
						/* Change every other comment to a different class */
						$oddcomment = ( empty($oddcomment) ? ' alt' : '' );
					?>
				<?php endforeach; /* end for each comment */ ?>
			</ol>
		<?php endif; ?>
	<?php else : /* If there are no comments */ ?>
		<?php if ('open' == $post->comment_status) : /* If comments are open */ ?>
			<p class="nocomments">No one has commented on this entry yet.</p>
		 <?php else : /* If comments are closed. */ ?>
			<p class="nocomments"> </p>
		<?php endif; ?>
	<?php endif; ?>

	<?php if ('open' == $post->comment_status) : /* If comments are open */ ?>
		<div class="commentform" id="respond">
			<h3><?php comment_form_title(); ?></h3>
			<?php if ( get_option('comment_registration') && !$user_ID ) : /* If registration is required, and the user is not logged in */ ?>
				<p>You must be <a href="<?php echo get_option('siteurl'); ?>/wp-login.php?redirect_to=<?php echo urlencode(get_permalink()); ?>">logged in</a> to post a comment.</p>
			<?php else : /* If registration is not required */ ?>
				<form action="<?php echo get_option('siteurl'); ?>/wp-comments-post.php" method="post" id="commentform">
					<?php if ( $user_ID ) : /* If the user is logged in */ ?>
						<p>Logged in as <a href="<?php echo get_option('siteurl'); ?>/wp-admin/profile.php"><?php echo $user_identity; ?></a>. <a href="<?php echo get_option('siteurl'); ?>/wp-login.php?action=logout">Log out &raquo;</a></p>
					<?php else : /* If the user is not logged in */ ?>
						<p>
							<input type="text" name="author" id="author" value="<?php echo $comment_author; ?>" size="25" tabindex="1" />
							<label for="author">Name <?php if ($req) echo "<em class=\"required\">(required)</em>"; ?></label>
						</p>
						<p>
							<input type="text" name="email" id="email" value="<?php echo $comment_author_email; ?>" size="25" tabindex="2" />
							<label for="email">Mail <small>(will not be published)</small> <?php if ($req) echo "<em class=\"required\">(required)</em>"; ?></label>
						</p>
						<p>
							<input type="text" name="url" id="url" value="<?php echo $comment_author_url; ?>" size="25" tabindex="3" />
							<label for="url">Website</label>
						</p>
					<?php endif; ?>
					<p><textarea name="comment" id="comment" cols="60" rows="10" tabindex="4"></textarea></p>
					<p class="buttons">
						<input name="submit" type="submit" id="submit" tabindex="5" value="Submit Comment" />
						<?php cancel_comment_reply_link("Nevermind, I don't want to reply to this person") ?>
						<?php comment_id_fields(); ?>
					</p>
					<?php do_action('comment_form', $post->ID); ?>
					<p class="instructions"><small><strong>XHTML:</strong> You can use these tags: <kbd><?php echo allowed_tags(); ?></kbd></small></p>
				</form>
			<?php endif; ?>
		</div><!-- end commentform -->
	<?php endif; ?>
	</div> <!-- end content -->



</div><!-- end comments -->