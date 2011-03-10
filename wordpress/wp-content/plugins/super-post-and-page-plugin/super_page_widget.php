<?php
/**
 * Plugin Name: Super Post and Page Widget
 * Plugin URI: http://www.thewebsiteaudit.com/super-post-and-page-widget
 * Description: A widget that can display any single post or page information in various ways inside a widget
 * Version: 0.4e
 * Author: Peter Knight
 * Author URI: http://www.thewebsiteaudit.com
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 */
 
/* Add our function to the widgets_init hook. */
add_action( 'widgets_init', 'custom_page_widget' );
add_theme_support( 'post-thumbnails' );
add_filter( 'post_thumbnail_html', 'my_post_image_html', 10, 3 );
add_action( 'edit_page_form', 'spw_add_box');


function spw_page_excerpt_meta_box($post) {
?>
<label class="hidden" for="excerpt"><?php _e('Excerpt') ?></label><textarea rows="1" cols="40" name="excerpt" tabindex="6" id="excerpt"><?php echo $post->post_excerpt ?></textarea>
<p><?php _e('Excerpts are optional hand-crafted summaries of your content. You can <a href="http://codex.wordpress.org/Template_Tags/the_excerpt" target="_blank">use them in your template</a>'); ?></p>
<?php
}

/* To make it easier to determine a post or page's id, I've added code found on Restore ID plugin (Contributors: nickohrn, gambit37
Donate link: http://nickohrn.com/wordpress-restore-id-plugin)
It makes it easy to identify the ID you need to insert inside the widget by looking at the columns in the manage posts & manage pages screen */
if(!class_exists('Super_Page_Post_Id_Display')) {

	class Super_Page_Post_Id_Display {
		
		/**
		 * Adds the Id column to the plugin.
		 */
		function custom_columns($defaults) {
			$other = array();
			$other['cb'] = $defaults['cb'];
			$other['id'] = __('Id');
			unset($defaults['cb']);
			return array_merge($other,$defaults);
		}
				/**
		 * Echoes the Id of the post/page that is being iterated over.
		 */
		function fill_column($column_name, $id) {
			if('id' == $column_name) {
				echo $id;
			}
		}
		
	} //end class

} // end if

/**
 * Insert action and filter hooks for posts and page id display here
 */
add_filter('manage_posts_columns', array('Super_Page_Post_Id_Display', 'custom_columns'));
add_action('manage_posts_custom_column', array('Super_Page_Post_Id_Display', 'fill_column'), 10, 2);
add_filter('manage_pages_columns', array('Super_Page_Post_Id_Display', 'custom_columns'));
add_action('manage_pages_custom_column', array('Super_Page_Post_Id_Display', 'fill_column'), 10, 2);

// personally added set column width for the id in the manage pages and manage posts screens
function style_id_column() {
echo '<style>
		.column-id { width: 30px; }
	</style>';
}
add_action('admin_head', 'style_id_column');

/* truncate function credit goes to Gabi Solomon, code can be found here: http://www.gsdesign.ro/blog/cut-html-string-without-breaking-the-tags/ */
function super_truncate($content, $length = 100, $ending = '...', $exact = false, $considerHtml = true) {
        //$content = ob_get_clean();
		//$text = strip_tags($content,'<p><a><b><br /><li><ol><ul><table>');
		$text = $content;
		if ($considerHtml) {
            // if the plain text is shorter than the maximum length, return the whole text
            if (strlen(preg_replace('/<.*?>/', '', $text)) <= $length) {
                return $text;
            }
            // splits all html-tags to scanable lines
            preg_match_all('/(<.+?>)?([^<>]*)/s', $text, $lines, PREG_SET_ORDER);
            $total_length = strlen($ending);
            $open_tags = array();
            $truncate = '';
            $doingtag=0;
            foreach ($lines as $line_matchings) {
                // if there is any html-tag in this line, handle it and add it (uncounted) to the output
                if (!empty($line_matchings[1])) {
                    // if it's an "empty element" with or without xhtml-conform closing slash (f.e. <br/>)
                    if (preg_match('/^<(\s*.+?\/\s*|\s*(img|br|input|hr|area|base|basefont|col|frame|isindex|link|meta|param)(\s.+?)?)>$/is', $line_matchings[1])) {
                        // do nothing
                    // if tag is a closing tag (f.e. </b>)
                    } else if (preg_match('/^<\s*\/([^\s]+?)\s*>$/s', $line_matchings[1], $tag_matchings)) {
                        // delete tag from $open_tags list
                        $pos = array_search($tag_matchings[1], $open_tags);
                        $doingtag=0;
                        if ($pos !== false) {
                            unset($open_tags[$pos]);
                        }
                    // if tag is an opening tag (f.e. <b>)
                    } else if (preg_match('/^<\s*([^\s>!]+).*?>$/s', $line_matchings[1], $tag_matchings)) {
                        // add tag to the beginning of $open_tags list
                        array_unshift($open_tags, strtolower($tag_matchings[1]));
                        $doingtag=1;
                    }
                    // add html-tag to $truncate'd text
                    $truncate .= $line_matchings[1];
                }
                // calculate the length of the plain text part of the line; handle entities as one character
                $content_length = strlen(preg_replace('/&[0-9a-z]{2,8};|&#[0-9]{1,7};|[0-9a-f]{1,6};/i', ' ', $line_matchings[2]));
                if ($total_length+$content_length> $length) {
                    // the number of characters which are left
                    $left = $length - $total_length;
                    $entities_length = 0;
                    // search for html entities
                    if (preg_match_all('/&[0-9a-z]{2,8};|&#[0-9]{1,7};|[0-9a-f]{1,6};/i', $line_matchings[2], $entities, PREG_OFFSET_CAPTURE)) {
                        // calculate the real length of all entities in the legal range
                        foreach ($entities[0] as $entity) {
                            if ($entity[1]+1-$entities_length <= $left) {
                                $left--;
                                $entities_length += strlen($entity[0]);
                            } else {
                                // no more characters left
                                break;
                            }
                        }
                    }
                    $truncate .= substr($line_matchings[2], 0, $left+$entities_length);
                    // maximum lenght is reached, so get off the loop
                    break;
                } else {
                    $truncate .= $line_matchings[2];
                    $total_length += $content_length;
                }
                // if the maximum length is reached, get off the loop
                if($total_length>= $length) {
                    break;
                }
            }
        } else {
            if (strlen($text) <= $length) {
                return $text;
            } else {
                $truncate = substr($text, 0, $length - strlen($ending));
            }
        }
        // if the words shouldn't be cut in the middle...
        if (!$exact) {
            // ...search the last occurance of a space...
            if(!$doingtag) { $spacepos = strrpos($truncate, ' '); }
            else { $spacepos=strrpos($truncate,'>'); }
            if (isset($spacepos)) {
                // ...and cut the text in this position
                $truncate = substr($truncate, 0, $spacepos);
                if($doingtag){$truncate.=">";}
            }
        }
        // add the defined ending to the text
        $truncate .= $ending;
        if($considerHtml) {
            // close all unclosed html-tags
            foreach ($open_tags as $tag) {
                $truncate .= '</' . $tag . '>';
            }
        }
        return $truncate;
    }

function spw_add_box()
{
	add_meta_box('postexcerpt', __('Page Excerpt'), 'spw_page_excerpt_meta_box', 'page', 'advanced', 'core');
}

function my_post_image_html( $html, $post_id, $post_image_id ) {

	$html = '<a href="' . get_permalink( $post_id ) . '" title="' . esc_attr( get_post_field( 'post_title', $post_id ) ) . '">' . $html . '</a>';

	return $html;
}
/* Function that registers our widget. */
function custom_page_widget() {
	register_widget( 'mycustom_page_widget' );
}

add_filter('editable_post_meta','htmlify');
function htmlify($data){
$data = apply_filters('the_content',$data).'test';
echo $data;
return apply_filters('editable_post_meta',$data);
}

class mycustom_page_widget extends WP_Widget {

	function mycustom_page_widget() {
		/* Widget settings. */
		$widget_ops = array( 'classname' => 'mycustom-page', 'description' => 'Displays content associated with a single post or page' );

		/* Widget control settings. */
		$control_ops = array( 'width' => 300, 'height' => 350, 'id_base' => 'mycustom-page-widget' );

		/* Create the widget. */
		$this->WP_Widget( 'mycustom-page-widget', 'Super Page Widget', $widget_ops, $control_ops );
	}
	
	function widget( $args, $instance ) {
		extract( $args );

		/* User-selected settings. */
		$title =  apply_filters('widget_title', $instance['title'] );
		$mypageid = $instance['mypageid'];
		$mycontentformat = $instance['mycontentformat'];
		$morelink = $instance['morelink'];
		$moretext = $instance['moretext'];
		$thumbnail = $instance['thumbnail'];
		$thumbposition = $instance['thumbposition'];
		$hidetitle = $instance['hidetitle'];
		$title_is_hyperlink = $instance['title_is_hyperlink'];
		$customtitlelink = $instance['customtitlelink'];
		$thumbposition = $instance['thumbposition'];
		$titlenametag = $instance['titlenametag'];
		$customfield = $instance['customfield'];
		$use_post_or_page_title = $instance['use_post_or_page_title'];
		$superexcerptlength = $instance['superexcerptlength'];
		$forcecustomfieldexcerpt = $instance['force_custom_field_excerpt'];
		/* Before widget (defined by themes). */
		
		echo $before_widget;
		
		// wrap content inside a div with individually identifiable class for custom styling
		echo '<div class="super-page-widget super-'.$mypageid.'">';

		// gets the content based on the id input
		$custom_page_content = get_post( $mypageid );
		the_post();
		setup_postdata($custom_page_content);
				
		// check what the permalink destination should be
		if ( !$customtitlelink ) { $permalink = get_permalink( $mypageid );} else { $permalink = $customtitlelink;} //checks to see if a custom title link was configured and uses that over the default permalink
		
		// checks what title to use, the widget title or page/post title
		if ( $use_post_or_page_title ) { 
		$title = apply_filters('the_title',$custom_page_content->post_title);
		}
		else {
		$title = get_post_meta($mypageid, 'customtitle', true);
		$title = apply_filters('post_meta',$title, $mypageid, 'customtitle', 'rich', true);
		}
		// checks to see if widget should place an image before the text
		if ( $thumbnail != "none" && $thumbposition == "before" ) { 
			?>
				<a href="<?php echo $permalink;?>"><?php echo get_the_post_thumbnail( $mypageid, $thumbnail );?></a><br />
			<?php }
		
		// checks if title should be visible, if hidden it will skip this section
		if ($hidetitle != 'hidden'){ 
			echo $before_title; 
				// checks to see if either/both name tag and hyperlinks were set to be activated
				if ($titlenametag || $title_is_hyperlink){
					?>
					<a <?php if ($titlenametag){ echo'name="'.$titlenametag.'"';} if ($title_is_hyperlink) {?> href="<?php echo $permalink;echo '"';}?>><?php echo $title;?></a><?php } 
					else { echo $title; }
			echo $after_title;
		} 
		// text section: checking content type
		// full content selected?
		if ( $mycontentformat == 'full') {
			$content = $custom_page_content->post_content;
			$content = apply_filters('the_content',$content);
			echo $content;// echoes out the content if full content was selected
		}
		// excerpt content selected?
		elseif ( $mycontentformat == 'excerpt' ) {
			$content = $custom_page_content->post_excerpt;
			if (strlen($content) > 5 && !$forcecfexcerpt){ 				
				$content = apply_filters('the_excerpt',$content);
				echo $content;} 
			else {
				echo apply_filters('the_excerpt',get_post_meta($mypageid, 'customexcerpt',true));
				}
				?>
		<a href="<?php if (!$morelink) { echo $permalink; } else { echo $morelink; }?>"><?php $more=get_post_meta($mypageid, 'custommoretext', true);echo apply_filters('post_meta',$more, $mypageid, 'custommoretext', 'rich', true);?></a><?php
		} 
		// custom field content selected?
		elseif ( $mycontentformat == 'customfield' ) 
		{ 
		$content = get_post_meta($mypageid, $customfield, true);
		$content = apply_filters('post_meta',$content);
		echo $content;?>
		<a href="<?php if (!isset ($morelink)) { echo $permalink; } else { ;  echo $morelink; }?>"><?php $more=get_post_meta($mypageid, 'custommoretext', true);echo apply_filters('post_meta',$more, $mypageid, 'custommoretext', 'rich', true);?></a><?php
		} 
		// checks if image position was set after text
		if ( $thumbnail != "none" && $thumbposition == "after" ) {?>
		<br /><a href="<?php echo $permalink;?>"><?php echo get_the_post_thumbnail( $mypageid, $thumbnail );?></a>
	<?php } 
		//endwhile;
		echo '</div>';
		
		/* After widget (defined by themes). */
		echo $after_widget;
				
	}

	function update( $new_instance, $old_instance ) {
		$instance = $old_instance;

		// Update manual excerpt if needed
		$tempcontent = get_post($new_instance['mypageid']);
		//$manualexcerptset = $tempcontent->post_excerpt;
		$manualcustomexcerptset = get_post_meta($new_instance['mypageid'],'customexcerpt');
		if (!$manualcustomexcerptset) { // checks if a custom field excerpt was already created and creates an excerpt based on character length if needed
			$content = $tempcontent->post_content;
			$content = apply_filters('the_post',$content);
			$content = strip_tags($content,'<em><strong><p><a><b><br /><li><ol><ul><table>');
			$content = super_truncate($content,$new_instance['superexcerptlength'],'',0,1);
			$content = apply_filters('the_content',$content);
			update_post_meta($new_instance['mypageid'],'customexcerpt',$content);
			}
		elseif($new_instance['superexcerptlength'] != $instance['superexcerptlength']){ //checks if user adjusted the character length and performs necessary update
				$content = $tempcontent->post_content;
				$content = apply_filters('the_post',$content);
				$content = strip_tags($content,'<em><strong><p><a><b><br /><li><ol><ul><table>');
				$content = super_truncate($content,$new_instance['superexcerptlength'],'',0,1);
				$content = apply_filters('the_content',$content);
				update_post_meta($new_instance['mypageid'],'customexcerpt',$content);
				/* the following was optional to update the regular excerpt fields wordpress defines as well
				$updated_manual_excerpt = array();
				$updated_manual_excerpt['ID']= $new_instance['mypageid'];
				$updated_manual_excerpt['post_excerpt']= $content;
				wp_update_post( $updated_manual_excerpt );*/
				}
		
		/* Strip tags (if needed) and update the widget settings. */
		$instance['title'] = strip_tags( $new_instance['title'] );
		$instance['mypageid'] = strip_tags( $new_instance['mypageid'] );
		$instance['mycontentformat'] = $new_instance['mycontentformat'];
		$instance['morelink'] = $new_instance['morelink'];
		$instance['moretext'] = $new_instance['moretext'];
		$instance['thumbnail'] = $new_instance['thumbnail'];
		$instance['thumbposition'] = $new_instance['thumbposition'];
		$instance['customtitlelink'] = $new_instance['customtitlelink'];
		$instance['hidetitle'] = $new_instance['hidetitle'];
		$instance['title_is_hyperlink'] = $new_instance['title_is_hyperlink'];
		$instance['titlenametag'] = $new_instance['titlenametag'];
		$instance['customfield'] = $new_instance['customfield'];
		$instance['superexcerptlength'] = $new_instance['superexcerptlength'];
		$instance['use_post_or_page_title'] = $new_instance['use_post_or_page_title'];
		$instance['force_custom_field_excerpt'] = $new_instance['force_custom_field_excerpt'];
		update_post_meta($new_instance['mypageid'],'custommoretext',$instance['moretext']);
		update_post_meta($new_instance['mypageid'],'customtitle',$instance['title']);
		
		
		return $instance;//($content, $length = 100, $ending = '...', $exact = false, $considerHtml = true)
	}	
	
	function form( $instance ) {

		/* Set up some default widget settings. */
		$defaults = array( 'title' => 'Example', 'mypageid' => '3', 'morelink' => '', 'mycontentformat' => 'excerpt' , 'thumbnail' => 'none' ,'moretext' => 'Read More', 'superexcerptlength'=> '360' );
		$instance = wp_parse_args( (array) $instance, $defaults ); ?>
		<p>
			<label for="<?php echo $this->get_field_id( 'title' ); ?>">Custom Title:</label>
			<input id="<?php echo $this->get_field_id( 'title' ); ?>" name="<?php echo $this->get_field_name( 'title' ); ?>" value='<?php echo get_post_meta($instance['mypageid'],'customtitle',true); ?>' style="width:100%;" />
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'customtitlelink' ); ?>">Custom Title Link:</label>
			<input id="<?php echo $this->get_field_id( 'customtitlelink' ); ?>" name="<?php echo $this->get_field_name( 'customtitlelink' ); ?>" value="<?php echo $instance['customtitlelink']; ?>" style="width:100%;" />
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'titlenametag' ); ?>">Title Name Tag:</label>
			<input id="<?php echo $this->get_field_id( 'titlenametag' ); ?>" name="<?php echo $this->get_field_name( 'titlenametag' ); ?>" value="<?php echo $instance['titlenametag']; ?>" style="width:100%;" />
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'mypageid' ); ?>">Page id:</label>
			<input id="<?php echo $this->get_field_id( 'mypageid' ); ?>" name="<?php echo $this->get_field_name( 'mypageid' ); ?>" value="<?php echo $instance['mypageid']; ?>" style="width:100%;" />
		</p>
		
		<p>
			<label for="<?php echo $this->get_field_id( 'moretext' ); ?>">More Text:</label>
			<input id="<?php echo $this->get_field_id( 'moretext' ); ?>" name="<?php echo $this->get_field_name( 'moretext' ); ?>" value='<?php $themore = get_post_meta($instance['mypageid'],'custommoretext',true); if($themore) { echo $themore; } else { echo $instance['moretext'];} ?>' style="width:100%;" />
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'morelink' ); ?>">More Link:</label>
			<input id="<?php echo $this->get_field_id( 'morelink' ); ?>" name="<?php echo $this->get_field_name( 'morelink' ); ?>" value="<?php echo $instance['morelink']; ?>" style="width:100%;" />
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'mycontentformat' ); ?>">Content format:</label>
			<select id="<?php echo $this->get_field_id( 'mycontentformat' ); ?>" name="<?php echo $this->get_field_name( 'mycontentformat' ); ?>" class="widefat" style="width:100%;">
				<option <?php if ( 'full' == $instance['mycontentformat'] ) echo 'selected="selected"'; ?>>full</option>
				<option <?php if ( 'excerpt' == $instance['mycontentformat'] ) echo 'selected="selected"'; ?>>excerpt</option>
				<option <?php if ( 'customfield' == $instance['mycontentformat'] ) echo 'selected="selected"'; ?>>customfield</option>
			</select>
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'customfield' ); ?>">Custom Field (optional):</label>
			<input id="<?php echo $this->get_field_id( 'customfield' ); ?>" name="<?php echo $this->get_field_name( 'customfield' ); ?>" value="<?php echo $instance['customfield']; ?>" style="width:100%;" />
		</p>
		<label for="<?php echo $this->get_field_id( 'superexcerptlength' ); ?>">Excerpt Character Length (if applicable):</label>
			<input id="<?php echo $this->get_field_id( 'superexcerptlength' ); ?>" name="<?php echo $this->get_field_name( 'superexcerptlength' ); ?>" value="<?php echo $instance['superexcerptlength']; ?>" style="width:100%;" />
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'hidetitle' ); ?>">Title Visibility:</label>
			<select id="<?php echo $this->get_field_id( 'hidetitle' ); ?>" name="<?php echo $this->get_field_name( 'hidetitle' ); ?>" class="widefat" style="width:100%;">
				<option <?php if ( 'visible' == $instance['hidetitle'] ) echo 'selected="selected"'; ?>>use custom title</option>
				<option <?php if ( 'hidden' == $instance['hidetitle'] ) echo 'selected="selected"'; ?>>hidden</option>
			</select>
		</p>
		<p>
			<input class="checkbox" type="checkbox" <?php checked( $instance['title_is_hyperlink'], 'on' ); ?> id="<?php echo $this->get_field_id( 'title_is_hyperlink' ); ?>" name="<?php echo $this->get_field_name( 'title_is_hyperlink' ); ?>" />
			<label for="<?php echo $this->get_field_id( 'title_is_hyperlink' ); ?>">Make The Title a Hyperlink?</label>
		</p>
		<p>
			<input class="checkbox" type="checkbox" <?php checked( $instance['use_post_or_page_title'], 'on' ); ?> id="<?php echo $this->get_field_id( 'use_post_or_page_title' ); ?>" name="<?php echo $this->get_field_name( 'use_post_or_page_title' ); ?>" />
			<label for="<?php echo $this->get_field_id( 'use_post_or_page_title' ); ?>">Use Post/Page Title Instead of Custom Title?</label>
		</p>
		<p>If checked, will ignore any manual excerpt set for the post/page and strictly used an excerpt created based on character length (length defined by this widget).
			<input class="checkbox" type="checkbox" <?php checked( $instance['force_custom_field_excerpt'], 'on' ); ?> id="<?php echo $this->get_field_id( 'force_custom_field_excerpt' ); ?>" name="<?php echo $this->get_field_name( 'force_custom_field_excerpt' ); ?>" />
			<label for="<?php echo $this->get_field_id( 'force_custom_field_excerpt' ); ?>">Force character-length based excerpt</label>
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'thumbposition' ); ?>">Thumb Position:</label>
			<select id="<?php echo $this->get_field_id( 'thumbposition' ); ?>" name="<?php echo $this->get_field_name( 'thumbposition' ); ?>" class="widefat" style="width:100%;">
				<option <?php if ( 'before' == $instance['thumbposition'] ) echo 'selected="selected"'; ?>>before</option>
				<option <?php if ( 'after' == $instance['thumbposition'] ) echo 'selected="selected"'; ?>>after</option>
			</select>
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'thumbnail' ); ?>">Thumbnail specs:</label>
			<select id="<?php echo $this->get_field_id( 'thumbnail' ); ?>" name="<?php echo $this->get_field_name( 'thumbnail' ); ?>" class="widefat" style="width:100%;">
				<option <?php if ( 'thumbnail' == $instance['thumbnail'] ) echo 'selected="selected"'; ?>>thumbnail</option>
				<option <?php if ( 'medium' == $instance['thumbnail'] ) echo 'selected="selected"'; ?>>medium</option>
				<option <?php if ( 'large' == $instance['thumbnail'] ) echo 'selected="selected"'; ?>>large</option>
				<option <?php if ( 'full' == $instance['thumbnail'] ) echo 'selected="selected"'; ?>>full</option>
				<option <?php if ( 'none' == $instance['thumbnail'] ) echo 'selected="selected"'; ?>>none</option>
			</select>
		</p>
	<?php 
	}
}
?>