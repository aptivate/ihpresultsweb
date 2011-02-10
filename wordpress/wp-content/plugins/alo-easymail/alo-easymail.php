<?php
/*
Plugin Name: ALO EasyMail Newsletter
Plugin URI: http://www.eventualo.net/blog/wp-alo-easymail-newsletter/
Description: To send newsletters. Features: collect subcribers on registration or with an ajax widget, mailing lists, cron batch sending, multilanguage.
Version: 1.8.4
Author: Alessandro Massasso
Author URI: http://www.eventualo.net
*/

/*  Copyright 2010  Alessandro Massasso  (email : alo@eventualo.net)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/


/**
 * Settings
 */
define("ALO_EM_FOOTER","<p style='margin-top:25px'>&raquo; <em>Please visit plugin site for more info and feedback: <a href='http://www.eventualo.net/blog/wp-alo-easymail-newsletter/' target='_blank'>www.eventualo.net</a></em></p>
	<p>&raquo; <em>If you use this plugin consider the idea of donating and supporting its development:</em></p><form action='https://www.paypal.com/cgi-bin/webscr' method='post' style='display:inline'>
	<input name='cmd' value='_s-xclick' type='hidden'><input name='lc' value='EN' type='hidden'><input name='hosted_button_id' value='9E6BPXEZVQYHA' type='hidden'>
	<input src='https://www.paypal.com/en_US/i/btn/btn_donate_SM.gif' name='submit' alt='PayPal' border='0' type='image'>
	<img alt='' src='https://www.paypal.com/it_IT/i/scr/pixel.gif' border='0' height='1' width='1'><br>	</form>");
define("ALO_EM_INTERVAL_MIN", 10); 	// cron interval in minutes (default: 10) (NOTE: to apply the change you need to reactivate the plugin)

define("ALO_EM_PLUGIN_DIR", basename(dirname(__FILE__)) );
define("ALO_EM_PLUGIN_URL", WP_PLUGIN_URL ."/" . ALO_EM_PLUGIN_DIR );


/**
 * Required functions
 */
require_once( 'alo-easymail_functions.php');


/**
 * On plugin activation 
 */
function ALO_em_install() {
    global $wpdb, $wp_roles;
    
	if (!get_option('ALO_em_template')) add_option('ALO_em_template', 'Hi [USER-NAME],<br /><br />
	    I have published a new post <strong>[POST-TITLE]</strong>.<br />[POST-EXCERPT]<br />Please visit my site [SITE-LINK] to read it and leave your comment about it.<br />
        Hope to see you online!<br /><br />[SITE-LINK]');
	if (!get_option('ALO_em_list')) add_option('ALO_em_list', '');
    if (!get_option('ALO_em_lastposts')) add_option('ALO_em_lastposts', 10);
    if (!get_option('ALO_em_dayrate')) add_option('ALO_em_dayrate', 1500);
    if (!get_option('ALO_em_batchrate')) add_option('ALO_em_batchrate', 60);
	if (!get_option('ALO_em_sender_email')) {
		$admin_email = get_option('admin_email');
	    add_option('ALO_em_sender_email', $admin_email);
	}
	if (!get_option('ALO_em_sender_name')) {
		$sender_name = get_option('blogname');
	    add_option('ALO_em_sender_name', $sender_name );
	}
		
	/*if (!get_option('ALO_em_optin_msg')) add_option('ALO_em_optin_msg', '' );
	if (!get_option('ALO_em_optout_msg')) add_option('ALO_em_optout_msg', '');	
	if (!get_option('ALO_em_lists_msg')) add_option('ALO_em_lists_msg', '');*/
	update_option('ALO_em_import_alert', "show" );
	if (!get_option('ALO_em_delete_on_uninstall')) add_option('ALO_em_delete_on_uninstall', 'no');
	if (!get_option('ALO_em_show_subscripage')) add_option('ALO_em_show_subscripage', 'no');
	if (!get_option('ALO_em_embed_css')) add_option('ALO_em_embed_css', 'no');
	
	ALO_em_setup_predomain_texts( false );
		    	    
	require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
	
    //-------------------------------------------------------------------------
	// TO MODIFY IF UPDATE NEEDED
	$database_version = '1.27';
	
	// Db version
	$installed_db = get_option('ALO_em_db_version');

	//if ( $database_version != $installed_db ) {
    	
    	$table_name = $wpdb->prefix . "easymail_subscribers";
    	
        if($wpdb->get_var("show tables like '$table_name'") != $table_name || $database_version != $installed_db) {
		    
			if( defined( 'DB_COLLATE' ) && constant( 'DB_COLLATE' ) != '' ) {
				$collate = constant( 'DB_COLLATE' );
			} else {
				$collate = constant( 'DB_CHARSET' );
			}
			
		    // Create the table structure
		    $sql = "CREATE TABLE ".$table_name." (
					    ID int(11) unsigned NOT NULL auto_increment,
					    email varchar(100) NOT NULL,
					    name varchar(100) NOT NULL,
					    join_date datetime NOT NULL,
					    active INT( 1 ) NOT NULL DEFAULT '0',
					    unikey varchar(24) NOT NULL,
					    lists varchar(255) DEFAULT '_',
					    lang varchar(5) DEFAULT NULL,					    
					    PRIMARY KEY  (ID),
					    UNIQUE KEY  `email` (`email`)
					    ) DEFAULT CHARSET=".$collate.";
					    
					CREATE TABLE {$wpdb->prefix}easymail_sendings (
						ID int(11) unsigned NOT NULL auto_increment,
						start_at datetime DEFAULT NULL,
						last_at datetime DEFAULT NULL,
						user int(11) unsigned DEFAULT NULL,
						subject varchar(250) DEFAULT NULL,
						content text DEFAULT NULL,
						recipients longtext DEFAULT NULL,
					    tracking varchar(10) DEFAULT NULL,						
					    tag varchar(30) DEFAULT NULL,						    
						sent INT( 1 ) NOT NULL DEFAULT '0',
						PRIMARY KEY  (ID)
						) DEFAULT CHARSET=".$collate.";
						
					CREATE TABLE {$wpdb->prefix}easymail_trackings (
						ID int(11) unsigned NOT NULL auto_increment,
						newsletter int(11) unsigned DEFAULT NULL,
						email varchar(100) NOT NULL,
						type varchar(10) DEFAULT NULL,
						PRIMARY KEY  (ID)
						) DEFAULT CHARSET=".$collate.";
				    ";

		    dbDelta($sql);
		    update_option( "ALO_em_db_version", $database_version );
        }
	//}
	
	//-------------------------------------------------------------------------
	// Create/update the page with subscription
	
	// check if page already exists
	$my_page_id = get_option('ALO_em_subsc_page');
	
	$my_page = array();
    $my_page['post_title'] = 'Newsletter';
    $my_page['post_content'] = '[ALO-EASYMAIL-PAGE]';
    $my_page['post_status'] = 'publish';
    $my_page['post_author'] = 1;
    $my_page['comment_status'] = 'closed';
    $my_page['post_type'] = 'page';
    
    if ($my_page_id) {
        // if exists update
        $my_page['ID'] = $my_page_id;
        wp_update_post($my_page);
    } else {
        // insert the post into the database
        $my_page_id = wp_insert_post( $my_page );
        update_option('ALO_em_subsc_page', $my_page_id);
    }
    
    // add scheduled cleaner
    wp_schedule_event(time(), 'twicedaily', 'ALO_em_schedule');
    // add scheduled cron batch
    wp_schedule_event( time() +60, 'ALO_em_interval', 'ALO_em_batch' ); /* hourly */
    
    // default permission
	$wp_roles->add_cap( 'administrator', 'manage_easymail_options');
	$wp_roles->add_cap( 'administrator', 'manage_easymail_subscribers');		
	$wp_roles->add_cap( 'administrator', 'manage_easymail_newsletters');
	$wp_roles->add_cap( 'administrator', 'send_easymail_newsletters');
	$wp_roles->add_cap( 'editor', 'send_easymail_newsletters');
}
register_activation_hook(__FILE__,'ALO_em_install');


/**
 * For batch sending (every tot mins)
 */

function ALO_em_more_reccurences() {
	return array(
		'ALO_em_interval' => array('interval' => 59*(ALO_EM_INTERVAL_MIN), 'display' => 'EasyMail every ' .ALO_EM_INTERVAL_MIN. ' minutes' )
	);
}
add_filter('cron_schedules', 'ALO_em_more_reccurences');


/**
 * Clean the new subscription not yet activated after too much time
 */

function ALO_em_clean_no_actived() {
	global $wpdb;
	// delete subscribes not yet activated after 5 days
	$limitdate = date ("Y-m-d",mktime(0,0,0,date("m"),date("d")-5,date("Y")));
    $output = $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->prefix}easymail_subscribers WHERE join_date <= '%s' AND active = '0'", $limitdate ) );
    //return $output;.
}

add_action('ALO_em_schedule', 'ALO_em_clean_no_actived');

add_action( 'ALO_em_batch' , 'ALO_em_batch_sending');


/**
 * On plugin adectivation 
 */
function ALO_em_uninstall() {
	global $wpdb, $wp_roles, $wp_version;
	
    // delete scheduled cleaner
    wp_clear_scheduled_hook('ALO_em_schedule');
    // delete cron batch sending
    wp_clear_scheduled_hook('ALO_em_batch');
    
    // if required delete all plugin data (options, db tables, page)
   	if ( get_option('ALO_em_delete_on_uninstall') == "yes" ) {
   		$tables = array ( "easymail_sendings", "easymail_subscribers", "easymail_trackings" );
   		foreach ( $tables as $tab ) {
   			$wpdb->query("DROP TABLE IF EXISTS {$wpdb->prefix}$tab");
   		}

		// delete option from db
		$wpdb->query( "DELETE FROM {$wpdb->prefix}options WHERE option_name LIKE '%ALO_em%'" );

	    // delete subscription page
		if ( version_compare ( $wp_version , '2.9', '>=' ) ) {
			wp_delete_post( get_option('ALO_em_subsc_page'), true ); // skip trash, from wp 2.9
		} else {
			wp_delete_post( get_option('ALO_em_subsc_page') );
		}
		// and the option with page id
		delete_option ('ALO_em_subsc_page');
	}
	
	// reset cap
	$roles = $wp_roles->get_names(); // get a list of values, containing pairs of: $role_name => $display_name
	foreach ( $roles as $rolename => $key) {
		$wp_roles->remove_cap( $rolename, 'manage_easymail_options');
		$wp_roles->remove_cap( $rolename, 'manage_easymail_subscribers');		
		$wp_roles->remove_cap( $rolename, 'manage_easymail_newsletters');
		$wp_roles->remove_cap( $rolename, 'send_easymail_newsletters');
	}
	
	// delete text pre-domain default
	delete_option ('ALO_em_txtpre_activationmail_mail_default');
	delete_option ('ALO_em_txtpre_activationmail_subj_default');
}
register_deactivation_hook( __FILE__, 'ALO_em_uninstall' );


/**
 * Add menu pages 
 */
function ALO_em_add_admin_menu() {
    add_options_page( __("Newsletter", "alo-easymail") , __("Newsletter", "alo-easymail"), 'manage_easymail_options', 'alo-easymail/alo-easymail_options.php');
	add_management_page ( __("Send newsletter", "alo-easymail"), __("Send newsletter", "alo-easymail"), 'send_easymail_newsletters', 'alo-easymail/alo-easymail_main.php');
	add_submenu_page('users.php', __("Newsletter subscribers", "alo-easymail"), __("Newsletter subscribers", "alo-easymail"), 'manage_easymail_subscribers', 'alo-easymail/alo-easymail_subscribers.php');
}

add_action('admin_menu', 'ALO_em_add_admin_menu');


require_once('alo-easymail-widget.php');

add_action( 'show_user_profile', 'ALO_em_user_profile_optin' );
add_action( 'edit_user_profile', 'ALO_em_user_profile_optin' );

function ALO_em_user_profile_optin($user) { 

    // get the current setting
    //if (ALO_easymail_get_optin($user->ID)=='yes'){    // deleted ALO
    if (ALO_em_is_subscriber($user->user_email)){       // added ALO
        $optin_selected = 'selected';            
        $optout_selected = '';            
    }
    else{
        $optin_selected = '';            
        $optout_selected = 'selected';            
    }        
    
    $html = "<h3>". __("Newsletter", "alo-easymail") ."</h3>\n";
    $html .= "<table class='form-table'>\n";
    $html .= "  <tr>\n";
    $optin_txt = ( ALO_em_translate_option ( ALO_em_get_language (), 'ALO_em_custom_optin_msg', false) !="") ? ALO_em_translate_option ( ALO_em_get_language (), 'ALO_em_custom_optin_msg', false) : __("Yes, I would like to receive the Newsletter", "alo-easymail"); 
    $html .= "    <th><label for='alo_em_option'>". $optin_txt ."</label></th>\n";
    $html .= "    <td>\n";
    $html .= "		<select name='alo_easymail_option' id='alo_easymail_option'>\n";
    $html .= "        <option value='yes' $optin_selected>". __("Yes", "alo-easymail")."</option>\n";
    $html .= "        <option value='no' $optout_selected>". __("No", "alo-easymail")."</option>\n";
    $html .= "      </select>\n";
    $html .= "    </td>\n";
    $html .= "  </tr>\n";
    $html .= "</table>\n";
 
	// add mailing lists html table
	$html .= ALO_em_html_mailinglists_table_to_edit ( $user->user_email, "form-table" );
 	
    echo $html;
}

add_action( 'personal_options_update', 'ALO_em_save_profile_optin' );
add_action( 'edit_user_profile_update', 'ALO_em_save_profile_optin' );

function ALO_em_save_profile_optin($user_id) {
     
	if ( !current_user_can( 'edit_user', $user_id ) )
		return false;
    
    $user_info = get_userdata( $user_id );
    $user_email = $user_info->user_email;
    
    if (isset($_POST['alo_easymail_option'])) {
        if ( $_POST['alo_easymail_option'] == "yes") {
            ALO_em_add_subscriber( $user_email, $user_info->first_name ." ".$user_info->first_name, 1, ALO_em_get_language() );
            
            // if subscribing, save also lists
        	$mailinglists = ALO_em_get_mailinglists( 'public' );
			if ($mailinglists) {
				$subscriber_id = ALO_em_is_subscriber( $user_email );
				foreach ( $mailinglists as $mailinglist => $val) {					
					if ( isset ($_POST['alo_em_profile_lists']) && is_array ($_POST['alo_em_profile_lists']) && in_array ( $mailinglist, $_POST['alo_em_profile_lists'] ) ) {
						ALO_em_add_subscriber_to_list ( $subscriber_id, $mailinglist );	  // add to list
					} else {
						ALO_em_delete_subscriber_from_list ( $subscriber_id, $mailinglist ); // remove from list
					}
				}
			}				
        } else {
            ALO_em_delete_subscriber_by_id( ALO_em_is_subscriber($user_email) );
        }
    }
}

// Widget activation

add_action( 'widgets_init', 'ALO_em_load_widgets' );

function ALO_em_load_widgets() {
	register_widget( 'ALO_Easymail_Widget' );
}


/**
 * Add javascript on admin side
 */
function ALO_add_admin_js() {
	if (isset($_GET['page']) && $_GET['page'] == "alo-easymail/alo-easymail_options.php") {
		wp_enqueue_script('jquery-ui-tabs');
		echo '<link rel="stylesheet" href="'.ALO_EM_PLUGIN_URL.'/inc/jquery.ui.tabs.css" type="text/css" media="print, projection, screen" />'."\n";
	}
}
add_action('admin_print_scripts', 'ALO_add_admin_js' );


/**
 * Add TinyMCE on admin side
 * http://blog.zen-dreams.com/en/2009/06/30/integrate-tinymce-into-your-wordpress-plugins/
 */
function ALO_em_show_tinymce () {
	if (isset($_GET['page']) ) {
		switch ( $_GET['page'] ) {
			case "alo-easymail/alo-easymail_main.php":
			//case "alo-easymail/alo-easymail_options.php":
				wp_enqueue_script( 'common' );
				wp_enqueue_script( 'jquery-color' );
				wp_print_scripts('editor');
				if (function_exists('add_thickbox')) add_thickbox();
				wp_print_scripts('media-upload');
				if (function_exists('wp_tiny_mce')) wp_tiny_mce();
				wp_admin_css();
				wp_enqueue_script('utils');
				do_action("admin_print_styles-post-php");
				do_action('admin_print_styles');
				wp_enqueue_script( 'jquery-form' ); // extra
				wp_enqueue_script( 'jquery-ui-core' ); // extra
		}
	}
}
add_filter('admin_head','ALO_em_show_tinymce');


/**
 * Load scripts & styles
 */
function ALO_em_load_scripts() {
	if ( get_option('ALO_em_embed_css') == "yes" ) {
		if ( @file_exists ( TEMPLATEPATH.'/alo-easymail.css' ) ) {
		  	wp_enqueue_style ('alo-easymail', get_bloginfo('template_directory') .'/alo-easymail.css' );
		} else {
		  	wp_enqueue_style ('alo-easymail', ALO_EM_PLUGIN_URL.'/alo-easymail.css' );
		}
	} 
}
add_action('wp_enqueue_scripts', 'ALO_em_load_scripts');


/**
 * On plugin init
 */
 
function ALO_em_init_method() {
	// if required, exclude the easymail page from pages' list
	if ( get_option('ALO_em_show_subscripage') == "no" ) add_filter('get_pages','ALO_exclude_page');
	// load localization files
	load_plugin_textdomain ("alo-easymail", false, "alo-easymail/languages");
}
add_action( 'init', 'ALO_em_init_method' );


function ALO_exclude_page( $pages ) {
    for ( $i=0; $i<count($pages); $i++ ) {
		$page = & $pages[$i];
        if ($page->ID == get_option('ALO_em_subsc_page')) unset ($pages[$i]);
    }
    return $pages;
}

/**
 * Manage the newsletter subscription page
 */
function ALO_em_subscr_page ($atts, $content = null) {
	ob_start();
	include(ABSPATH . 'wp-content/plugins/alo-easymail/easymail-subscr-page.php');
	$contents = ob_get_contents();
	ob_end_clean();
	return $contents;
}
add_shortcode('ALO-EASYMAIL-PAGE', 'ALO_em_subscr_page');


/**
 * Add to favorites top menu
 */
function ALO_em_add_favorite ($actions) {
	if ( current_user_can( "send_easymail_newsletters") ) {
		$actions['edit.php?page=alo-easymail/alo-easymail_main.php'] = array( __("Newsletters", "alo-easymail") , 'send_easymail_newsletters' );
	}
	return $actions;
}
add_filter('favorite_actions', 'ALO_em_add_favorite', 10000); // inspired by http://wordpress.org/extend/plugins/favorites-menu-manager/



/**
 * Add a dashboard widget
 */
function ALO_em_dashboard_widget_function() {
	global $wpdb;
	echo "<h4>". __("Newsletters scheduled for sending", "alo-easymail")."</h4>";
	$news_on_queue =  $wpdb->get_results("SELECT * FROM {$wpdb->prefix}easymail_sendings WHERE sent = 0 ORDER BY ID ASC LIMIT 4");
	if (count($news_on_queue)) {
		echo "<ul>";
		$row_count = 1;
		foreach ($news_on_queue as $q) {
			echo "<li style='margin:10px auto'>";
			if ($row_count == 1) { // the 1st, now on sending
				echo '<img src="'.get_option ('home').'/wp-content/plugins/alo-easymail/images/16-email-forward.png" title="'.__("now sending", "alo-easymail").'" alt="" style="vertical-align:text-bottom" />';
			} else {
				echo "#".($row_count - 1);
			}
			echo " <strong>" . stripslashes ( ALO_em___( $q->subject ) ) ."</strong><br />";
			if ($row_count == 1) { 
				$q_recipients = unserialize( $q->recipients );
				$q_tot = count($q_recipients);
				$n_sent = 0;
				foreach ($q_recipients as $qr) {
			   		if ( isset($qr['result']) ) $n_sent ++;
			   	}
				echo __("Progress", "alo-easymail") .": " . round($n_sent*100/ $q_tot ) . " %<br />" ;			
			}
			echo "<em>".__("Added on", "alo-easymail") . " ". date("d/m/Y", strtotime($q->start_at))." h.".date("H:i", strtotime($q->start_at)) . " - "; 
			echo __("Scheduled by", "alo-easymail") . " ". get_user_meta($q->user, 'nickname',true). "</em>";
		    echo "</li>";
			$row_count++;
		}
		echo "</ul>";
	} else {
		echo "<p>". __("There are no newsletters in queue", "alo-easymail") . ".</p>";
	}
	echo "<br /><h4>". __("Subscribers", "alo-easymail") ."</h4>";
	list ( $total, $active, $noactive ) = ALO_em_count_subscribers ();
	if ($total) {
		echo "<p>". sprintf( __("There are %d subscribers: %d activated, %d not activated", "alo-easymail"), $total, $active, $noactive ) . ".</p>";
	} else {
		echo "<p>". __("No subscribers", "alo-easymail") . ".</p>";
	}
} 

function ALO_em_add_dashboard_widgets() {
	if ( current_user_can ( 'manage_easymail_subscribers' ) && current_user_can ( 'manage_easymail_newsletters' ) ) {
		wp_add_dashboard_widget('alo-easymail-widget', 'EasyMail Newsletter', 'ALO_em_dashboard_widget_function');	
	}
} 
add_action('wp_dashboard_setup', 'ALO_em_add_dashboard_widgets' );


/**
 * SHOW the optin/optout on registration form
 */
function ALO_em_show_registration_optin () {
    $optin_txt = ( ALO_em_translate_option ( ALO_em_get_language (), 'ALO_em_custom_optin_msg', false) !="") ? ALO_em_translate_option ( ALO_em_get_language (), 'ALO_em_custom_optin_msg', false) : __("Yes, I would like to receive the Newsletter", "alo-easymail"); 
	echo '<p class="alo_easymail_reg_optin"><input type="checkbox" id="alo_em_opt" name="alo_em_opt" value="yes" class="input" checked="checked" /> ';
	echo '<label for="alo_em_opt" >' . $optin_txt .'</label></p>';
	 
    $mailinglists = ALO_em_get_mailinglists( 'public' );
    if ( $mailinglists ) {
    	$lists_msg 	= ( ALO_em_translate_option ( ALO_em_get_language (), 'ALO_em_custom_lists_msg',false) !="") ? ALO_em_translate_option ( ALO_em_get_language (), 'ALO_em_custom_lists_msg',false) :  __("You can also sign up for specific lists", "alo-easymail"); 
		echo "<p class='alo_easymail_reg_list_msg'>". $lists_msg .":</p>\n";
		foreach ( $mailinglists as $list => $val ) {
			echo "<p class='alo_easymail_reg_list'><input type='checkbox' name='alo_em_register_lists[]' id='alo_em_register_list_$list' value='$list' /> <label for='alo_em_register_list_$list'>" . ALO_em_translate_multilangs_array ( ALO_em_get_language(), $val['name'], true ) ."</label></p>\n";
		}
	} 

	echo '<input type="hidden" id="alo_em_lang" name="alo_em_lang" value="' . esc_attr(ALO_em_get_language()).'" /> ';
}
add_action('register_form','ALO_em_show_registration_optin');


/**
 * SAVE the optin/optout on registration form
 */
function ALO_em_save_registration_optin ($user_id, $password="", $meta=array())  {
	$user = get_userdata($user_id);
	if (!empty($user->first_name) && !empty($user->last_name)) {
		$name = $user->first_name.' '.$user->last_name;	
	} else {
		$name = $user->display_name;
	}
	if ( isset ($_POST['alo_em_opt']) && $_POST['alo_em_opt'] == "yes" ) {
		$lang = ( isset($_POST['alo_em_lang']) && in_array ( $_POST['alo_em_lang'], ALO_em_get_all_languages( false )) ) ? $_POST['alo_em_lang'] : "" ;
		ALO_em_add_subscriber( $user->user_email, $name , 1, $lang );
		
		 // if subscribing, save also lists
    	$mailinglists = ALO_em_get_mailinglists( 'public' );
		if ($mailinglists) {
			$subscriber_id = ALO_em_is_subscriber( $user->user_email );
			foreach ( $mailinglists as $mailinglist => $val) {					
				if ( isset ($_POST['alo_em_register_lists']) && is_array ($_POST['alo_em_register_lists']) && in_array ( $mailinglist, $_POST['alo_em_register_lists'] ) ) {
					ALO_em_add_subscriber_to_list ( $subscriber_id, $mailinglist );	  // add to list
				} 
			}
		}				
	}
}
add_action( 'user_register', 'ALO_em_save_registration_optin' );


/** EXPERIMENTAL
 * Return the localised login url
 */
 /*
function ALO_em_login_url( $url ) {
	// qTranslate
	if( ALO_em_multilang_enabled_plugin() == "qTrans") $url = add_query_arg( 'lang', ALO_em_get_language(), $url );
	return $url;
}
add_filter( 'login_url', 'ALO_em_login_url', 10);
*/

/** EXPERIMENTAL
 * Return the localised register url
 */
 /*
function ALO_em_register_url( $url ) {
	// qTranslate
	//if( ALO_em_multilang_enabled_plugin() == "qTrans") $url = add_query_arg( 'lang', ALO_em_get_language(), $url );
   	return $url;
}
add_filter( 'register', 'ALO_em_register_url', 10 );
*/


/**
 * Edit the e-mail message
 */
 
function ALO_em_handle_email ( $args ) {
	// $args['to'], $args['subject'], $args['message'], $args['headers'], $args['attachments']
	
	// Check based on $args['subject']; more attrs in $args['message']
	global $_config;
	/*
	 * 1) Activation e-mail
	 */
	if ( strpos ( "#_EASYMAIL_ACTIVATION_#", $args['subject'] ) !== false) {
		
		// Get the parameters stored as a query in $args['message'] 
		$defaults = array( 'lang' => '', 'email' => '',	'name' => '', 'unikey' => '' );
		$customs = wp_parse_args( $args['message'], $defaults );
		extract( $customs, EXTR_SKIP );
		
		// Subject
	   	if ( ALO_em_translate_option ( $lang, 'ALO_em_txtpre_activationmail_subj', false ) ) {
			$subject = ALO_em_translate_option ( $lang, 'ALO_em_txtpre_activationmail_subj', false );
		} else {
		   	$subject = ALO_em___( __("Confirm your subscription to %BLOGNAME% Newsletter", "alo-easymail" ) );
		}
		$blogname = html_entity_decode ( wp_kses_decode_entities ( get_option('blogname') ) );
		$subject = str_replace ( "%BLOGNAME%", $blogname, $subject );
		$args['subject'] = $subject;
				
		// Content
	   	if ( ALO_em_translate_option ( $lang, 'ALO_em_txtpre_activationmail_mail', false ) ) {
			$content = ALO_em_translate_option ( $lang, 'ALO_em_txtpre_activationmail_mail', false );
		} else {
		   	$content = __("Hi %NAME%\nto complete your subscription to %BLOGNAME% newsletter you need to click on the following link (or paste it in the address bar of your browser):\n", "alo-easymail");
		   	$content .= "%ACTIVATIONLINK%\n\n";
		   	$content .= __("If you did not ask for this subscription ignore this message.", "alo-easymail"). "\n";
		    $content .= __("Thank you", "alo-easymail")."\n". $blogname ."\n";
		}

	 	$div_email = explode("@", $email);
		$arr_params = array ('ac' => 'activate', 'em1' => $div_email[0], 'em2' => $div_email[1], 'uk' => $unikey );
		$sub_link = add_query_arg( $arr_params, get_page_link (get_option('ALO_em_subsc_page')) );
		$sub_link = ALO_em_translate_url ( $sub_link, $lang );		
		
	  	$content = str_replace ( "%BLOGNAME%", $blogname, $content );
	   	$content = str_replace ( "%NAME%", $name, $content );
	   	$content = str_replace ( "%ACTIVATIONLINK%", $sub_link, $content );
	   	
		$args['message'] = $content;
	}
	
	return $args;
}

add_filter('wp_mail', 'ALO_em_handle_email');


?>
