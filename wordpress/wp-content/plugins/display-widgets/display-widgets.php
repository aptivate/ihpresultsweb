<?php
/*
Plugin Name: Display widgets
Plugin URI: http://blog.strategy11.com/display-widgets/
Description: Adds checkboxes to each widget to show or hide on site pages.
Author: Stephanie Wells
Author URI: http://blog.strategy11.com
Version: 1.14
*/

//TODO: Add text field that accepts full urls that will be checked under 'else'
load_plugin_textdomain( 'display-widgets', false, dirname( plugin_basename( __FILE__ ) ) . '/languages/' );

function show_dw_widget($instance){
    if (is_home())
        $show = isset($instance['page-home']) ? ($instance['page-home']) : false;
    else if (is_front_page())
        $show = isset($instance['page-front']) ? ($instance['page-front']) : false;
    else if (is_category())
        $show = isset($instance['cat-'.get_query_var('cat')]) ? ($instance['cat-'.get_query_var('cat')]) : false;
    else if (is_archive())
        $show = isset($instance['page-archive']) ? ($instance['page-archive']) : false;
    else if (is_single()){
        $show = isset($instance['page-single']) ? ($instance['page-single']) : false;
        if (!$show){
            foreach(get_the_category() as $cat){ 
                if ($show) continue;
                if (isset($instance['cat-'.$cat->cat_ID]))
                    $show = $instance['cat-'.$cat->cat_ID];
            } 
        }
    }else if (is_404()) 
        $show = isset($instance['page-404']) ? ($instance['page-404']) : false;
    else if (is_search())
        $show = isset($instance['page-search']) ? ($instance['page-search']) : false;
    else{
        global $wp_query;
        $post_id = $wp_query->get_queried_object_id();
        $show = isset($instance['page-'.$post_id]) ? ($instance['page-'.$post_id]) : false;
        
        if (!$show and isset($instance['other_ids']) and !empty($instance['other_ids'])){
            $other_ids = explode(',', $instance['other_ids']);
            foreach($other_ids as $other_id){
                if($post_id == (int)$other_id)
                    $show = true;
            }
        }
    }
    
    if (isset($instance['include']) && (($instance['include'] and $show == false) or ($instance['include'] == 0 and $show)))
        return false;
    else{
        global $user_ID;
        if( (isset($instance['logout']) and $instance['logout'] and $user_ID) or 
            (isset($instance['login']) and $instance['login'] and !$user_ID)) 
            return false;
            
    }
	return $instance;
}

function dw_show_hide_widget_options($widget, $return, $instance){
    $last_saved = get_option('dw_check_new_pages'); //Check to see when pages and categories were last saved

    //if more than 1 minute ago, we can check again
    if(!$last_saved or ((time() - $last_saved) >= 60)){
        $pages = get_posts( array('post_type' => 'page', 'post_status' => 'publish', 'numberposts' => 999, 'orderby' => 'title', 'order' => 'ASC'));
        $cats = get_categories();
        update_option('dw_saved_page_list', $pages);
        update_option('dw_saved_cat_list', $cats);
        update_option('dw_check_new_pages', time());
    }else{
        $pages = get_option('dw_saved_page_list');
        $cats = get_option('dw_saved_cat_list');
    }
       
    $wp_page_types = array('front' => __('Front', 'display-widgets'), 'home' => __('Blog', 'display-widgets'),'archive' => __('Archives', 'display-widgets'),'single' => __('Single Post', 'display-widgets'),'404' => '404', 'search' => __('Search', 'display-widgets'));
    
    $instance['include'] = isset($instance['include']) ? $instance['include'] : 0;
    $instance['logout'] = isset($instance['logout']) ? $instance['logout'] : 0;
    $instance['login'] = isset($instance['login']) ? $instance['login'] : 0;
    $instance['other_ids'] = isset($instance['other_ids']) ? $instance['other_ids'] : '';
?>   
     <p>
    	<label for="<?php echo $widget->get_field_id('include'); ?>"><?php _e('Show/Hide Widget', 'display-widgets') ?></label>
    	<select name="<?php echo $widget->get_field_name('include'); ?>" id="<?php echo $widget->get_field_id('include'); ?>" class="widefat">
            <option value="0" <?php echo selected( $instance['include'], 0 ) ?>><?php _e('Hide on checked', 'display-widgets') ?></option> 
            <option value="1" <?php echo selected( $instance['include'], 1 ) ?>><?php _e('Show on checked', 'display-widgets') ?></option>
        </select>
    </p>    

<div style="height:150px; overflow:auto; border:1px solid #dfdfdf;">
    <p><input class="checkbox" type="checkbox" <?php checked($instance['logout'], true) ?> id="<?php echo $widget->get_field_id('logout'); ?>" name="<?php echo $widget->get_field_name('logout'); ?>" value="1" />
    <label for="<?php echo $widget->get_field_id('logout'); ?>"><?php _e('Show only for Logged-out users', 'display-widgets') ?></label></p>
    <p><input class="checkbox" type="checkbox" <?php checked($instance['login'], true) ?> id="<?php echo $widget->get_field_id('login'); ?>" name="<?php echo $widget->get_field_name('login'); ?>" value="1" />
    <label for="<?php echo $widget->get_field_id('login'); ?>"><?php _e('Show only for Logged-in users', 'display-widgets') ?></label></p>
    
    <p><b><?php _e('Pages', 'display-widgets') ?> <a href="javascript:dw_toggle_pages()">+/-</a></b></p>
    <div id="<?php echo $widget->get_field_id('dw_pages'); ?>">
    <?php foreach ($pages as $page){ 
        $instance['page-'.$page->ID] = isset($instance['page-'.$page->ID]) ? $instance['page-'.$page->ID] : false;   
    ?>
        <p><input class="checkbox" type="checkbox" <?php checked($instance['page-'.$page->ID], true) ?> id="<?php echo $widget->get_field_id('page-'.$page->ID); ?>" name="<?php echo $widget->get_field_name('page-'.$page->ID); ?>" />
        <label for="<?php echo $widget->get_field_id('page-'.$page->ID); ?>"><?php echo $page->post_title ?></label></p>
    <?php	}  ?>
    </div>
    
    <p><b><?php _e('Categories', 'display-widgets') ?> <a href="javascript:dw_toggle_cats()">+/-</a></b></p>
    <div id="<?php echo $widget->get_field_id('dw_cats'); ?>">
    <?php foreach ($cats as $cat){ 
        $instance['cat-'.$cat->cat_ID] = isset($instance['cat-'.$cat->cat_ID]) ? $instance['cat-'.$cat->cat_ID] : false;   
    ?>
        <p><input class="checkbox" type="checkbox" <?php checked($instance['cat-'.$cat->cat_ID], true) ?> id="<?php echo $widget->get_field_id('cat-'.$cat->cat_ID); ?>" name="<?php echo $widget->get_field_name('cat-'.$cat->cat_ID); ?>" />
        <label for="<?php echo $widget->get_field_id('cat-'.$cat->cat_ID); ?>"><?php echo $cat->cat_name ?></label></p>
    <?php } ?>
    </div>
    <p><b><?php _e('Miscellaneous', 'display-widgets') ?></b></p>
    <?php foreach ($wp_page_types as $key => $label){ 
        $instance['page-'. $key] = isset($instance['page-'. $key]) ? $instance['page-'. $key] : false;
    ?>
        <p><input class="checkbox" type="checkbox" <?php checked($instance['page-'. $key], true) ?> id="<?php echo $widget->get_field_id('page-'. $key); ?>" name="<?php echo $widget->get_field_name('page-'. $key); ?>" />
        <label for="<?php echo $widget->get_field_id('page-'. $key); ?>"><?php echo $label .' '. __('Page', 'display-widgets') ?></label></p>
    <?php } ?>
    <p><label for="<?php echo $widget->get_field_id('other_ids'); ?>"><?php _e('Comma Separated list of IDs of posts not listed above', 'display-widgets') ?>:</label>
    <input type="text" value="<?php echo $instance['other_ids'] ?>" name="<?php echo $widget->get_field_name('other_ids'); ?>" id="<?php echo $widget->get_field_id('other_ids'); ?>" />
    </p>
    </div>
    <script type="text/javascript">
    function dw_toggle_cats(){jQuery('#<?php echo $widget->get_field_id("dw_cats"); ?>').toggle();}
    function dw_toggle_pages(){jQuery('#<?php echo $widget->get_field_id("dw_pages"); ?>').toggle();}
    </script>
<?php        
}

function dw_update_widget_options($instance, $new_instance, $old_instance){
    $pages = get_posts( array('post_type' => 'page', 'post_status' => 'publish', 'numberposts' => 999, 'order_by' => 'post_title', 'order' => 'ASC'));
    foreach ($pages as $page)
        $instance['page-'.$page->ID] = isset($new_instance['page-'.$page->ID]) ? 1 : 0;
    foreach (get_categories() as $cat)
        $instance['cat-'.$cat->cat_ID] = isset($new_instance['cat-'.$cat->cat_ID]) ? 1 : 0;
    $instance['include'] = $new_instance['include'] ? 1 : 0;
    $instance['logout'] = $new_instance['logout'] ? 1 : 0;
    $instance['login'] = $new_instance['login'] ? 1 : 0;
    $instance['other_ids'] = $new_instance['other_ids'] ? $new_instance['other_ids'] : '';
    $instance['page-front'] = isset($new_instance['page-front']) ? 1 : 0;
    $instance['page-home'] = isset($new_instance['page-home']) ? 1 : 0;
    $instance['page-archive'] = isset($new_instance['page-archive']) ? 1 : 0;
    $instance['page-single'] = isset($new_instance['page-single']) ? 1 : 0;
    $instance['page-404'] = isset($new_instance['page-404']) ? 1 : 0;
    $instance['page-search'] = isset($new_instance['page-search']) ? 1 : 0;
    return $instance;
}


add_filter('widget_display_callback', 'show_dw_widget');
add_action('in_widget_form', 'dw_show_hide_widget_options', 10, 3);
add_filter('widget_update_callback', 'dw_update_widget_options', 10, 3);
?>