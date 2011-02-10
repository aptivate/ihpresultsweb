<?php

/*************************************************************************
 * MISC UTILITIES FUNCTIONS
 *************************************************************************/ 

/**
 * Add help image with tooltip
 */
function ALO_em_help_tooltip ( $text ) {
	$text = str_replace( array("'", '"'), "", $text );
	$html = "<img src='".ALO_EM_PLUGIN_URL."/images/12-help.png' title='". esc_attr($text) ."' style='cursor:help;vertical-align:middle;margin-left:3px' alt='(?)' />";
	return $html;
}


/**
 * Compatibility with older WP version
 * get_usermeta (deprecated from 3.0)
 */
if ( !function_exists('get_user_meta') ) {
	function get_user_meta ( $user, $key, $single=false ) {
		return get_usermeta ( $user, $key );
	}
}



/**
 * Sort a multidimensional array on a array kay (found on http://php.net/manual/en/function.sort.php)
 * @array		array	the array
 * @key			str		the field to use as key to sort
 * @order		str		sort method: "ASC", "DESC"
 */

function ALO_em_msort  ($array, $key, $order = "ASC") {
	$tmp = array();
	foreach($array as $akey => $array2)  {
		$tmp[$akey] = $array2[$key];
	}
    if ($order == "DESC") {
    	arsort($tmp , SORT_NUMERIC );
    } else {
    	asort($tmp , SORT_NUMERIC );
    }
	$tmp2 = array();       
 	foreach($tmp as $key => $value) {
		$tmp2[$key] = $array[$key];
	}       
	return $tmp2; 
}
        

/**
 * Remove HTML tags, including invisible text such as style and
 * script code, and embedded objects.  Add line breaks around
 * block-level tags to prevent word joining after tag removal.
 * (based on http://nadeausoftware.com/articles/2007/09/php_tip_how_strip_html_tags_web_page )
 */
function ALO_em_html2plain ( $text ) {
	// transform in utf-8 if not yet
	if ( mb_detect_encoding($text, "UTF-8") != "UTF-8" ) $text = utf8_encode($text);
    $text = preg_replace(
        array(
          // Remove invisible content
            '@<head[^>]*?>.*?</head>@siu',
            '@<style[^>]*?>.*?</style>@siu',
            '@<script[^>]*?.*?</script>@siu',
            '@<object[^>]*?.*?</object>@siu',
            '@<embed[^>]*?.*?</embed>@siu',
            '@<applet[^>]*?.*?</applet>@siu',
            '@<noframes[^>]*?.*?</noframes>@siu',
            '@<noscript[^>]*?.*?</noscript>@siu',
            '@<noembed[^>]*?.*?</noembed>@siu',
          // Add line breaks before and after blocks
            '@</?((address)|(blockquote)|(center)|(del))@iu',
            '@</?((div)|(h[1-9])|(ins)|(isindex)|(p)|(pre))@iu',
            '@</?((dir)|(dl)|(dt)|(dd)|(li)|(menu)|(ol)|(ul))@iu',
            '@</?((table)|(th)|(td)|(caption))@iu',
            '@</?((form)|(button)|(fieldset)|(legend)|(input))@iu',
            '@</?((label)|(select)|(optgroup)|(option)|(textarea))@iu',
            '@</?((frameset)|(frame)|(iframe))@iu',
        ),
        array(
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            "\n\$0", "\n\$0", "\n\$0", "\n\$0", "\n\$0", "\n\$0",
            "\n\$0" 
        ),
        $text );
    // from <br> to \n
   	$text = preg_replace('/<br(\s+)?\/?>/i', "\n", $text );
	// reduce 2 or more consecutive <br> to one
	$text = preg_replace ("|(\\n\s*){2,}|s","\n", $text);
 	
    return strip_tags( $text );
}



/*************************************************************************
 * SUBSCRIPTION FUNCTIONS
 *************************************************************************/ 


/**
 * Count the n° of subscribers
 * return a array: total (active + not active), active, not active
 */
function ALO_em_count_subscribers () {
    global $wpdb;
    $search = $wpdb->get_results( "SELECT active, COUNT(active) AS count FROM {$wpdb->prefix}easymail_subscribers GROUP BY active ORDER BY active ASC" );
    $total = $noactive = $active = false;
    if ($search) {
		foreach ($search as $s) {
			switch ($s->active) {
				case 0: 	$noactive = $s->count; break;
				case 1: 	$active = $s->count; break;
			}
		}
		$total = $noactive + $active;
	} 
    return array ( $total, $active, $noactive );
} 


/**
 * Check is there is already a subscriber with that email and return ID subscriber
 */
function ALO_em_is_subscriber($email) {
    global $wpdb;
    $is_subscriber = $wpdb->get_var( $wpdb->prepare("SELECT ID FROM {$wpdb->prefix}easymail_subscribers WHERE email='%s' LIMIT 1", $email) );
    return (($is_subscriber)? $is_subscriber : 0); // ID in db tab subscribers
} 


/**
 * Check is there is a subscriber with this ID and return true/false
 */
function ALO_em_is_subscriber_by_id ( $id ) {
    global $wpdb;
    $is_subscriber = $wpdb->get_var( $wpdb->prepare("SELECT ID FROM {$wpdb->prefix}easymail_subscribers WHERE ID=%d LIMIT 1", $id) );
    return $is_subscriber;
} 


/**
 * Check the state of a subscriber (active/not-active)
 */
function ALO_em_check_subscriber_state($email) {
    global $wpdb;
    $is_activated = $wpdb->get_var( $wpdb->prepare("SELECT active FROM {$wpdb->prefix}easymail_subscribers WHERE email='%s' LIMIT 1", $email) );
    return $is_activated;
} 


/**
 * Modify the state of a subscriber (active/not-active) (BY ADMIN)
 */
function ALO_em_edit_subscriber_state_by_id($id, $newstate) {
    global $wpdb;
    $output = $wpdb->update(    "{$wpdb->prefix}easymail_subscribers",
                                array ( 'active' => $newstate ),
                                array ( 'ID' => $id)
                            );
    return $output;
} 


/**
 * Modify the state of a subscriber (active/not-active) (BY SUBSCRIBER)
 */
function ALO_em_edit_subscriber_state_by_email($email, $newstate="1", $unikey) {
    global $wpdb;
    $output = $wpdb->update(    "{$wpdb->prefix}easymail_subscribers",
                                array ( 'active' => $newstate ),
                                array ( 'email' => $email, 'unikey' => $unikey )
                            );
    return $output;
} 


/**
 * Add a new subscriber 
 * return bol/str:
 *		false					= generic error
 *		"OK"					= success
 *		"NO-ALREADYACTIVATED"	= not added because: email is already added and activated
 *		"NO-ALREADYADDED"		= not added because: email is already added but not activated; so send activation msg again
 */
function ALO_em_add_subscriber($email, $name, $newstate=0, $lang="" ) {
    global $wpdb;
 	$output = true;
    // if there is NOT a subscriber with this email address: add new subscriber and send activation email
    if (ALO_em_is_subscriber($email) == false){
        $unikey = substr(md5(uniqid(rand(), true)), 0,24);    // a personal key to manage the subscription
           
        // try to send activation mail, otherwise will not add subscriber
        if ($newstate == 0) {
            if ( !ALO_em_send_activation_email($email, $name, $unikey, $lang) ) $output = false; // DEBUG ON LOCALHOST: comment this line to avoid error on sending mail
        }
        
        if ( $output ) {	
			$wpdb->insert ( "{$wpdb->prefix}easymail_subscribers",
           					array( 'email' => $email, 'name' => $name, 'join_date' => get_date_from_gmt( date("Y-m-d H:i:s") ), 'active' => $newstate, 'unikey' => $unikey, 'lists' => "_", 'lang' => $lang )
			);
        	$output = "OK"; //return true;
        }
        
    } else {
        // if there is ALREADY a subscriber with this email address, and if is NOT confirmed yet: re-send an activation email
        if ( ALO_em_check_subscriber_state($email) == 0) {
            // retrieve existing unique key 
            $exist_unikey = $wpdb->get_var( $wpdb->prepare("SELECT unikey FROM {$wpdb->prefix}easymail_subscribers WHERE ID='%d' LIMIT 1", ALO_em_is_subscriber($email) ) );
            
            if ( ALO_em_send_activation_email($email, $name, $exist_unikey, $lang) ) {
                // update join date to today
                $output = $wpdb->update(    "{$wpdb->prefix}easymail_subscribers",
                                            array ( 'join_date' => get_date_from_gmt( date("Y-m-d H:i:s") ), 'lang' => $lang ),
                                            array ( 'ID' => ALO_em_is_subscriber($email) )
                                        );
             	// tell that there is already added but not active: so it has sent another activation mail.......
                $output = "NO-ALREADYADDED";
            } else {
                $output = false;
                //$output = "NO-ALREADYADDED"; // DEBUG ON LOCALHOST: comment the previous line and uncomment this one to avoid error on sending mail
            }
        } else {
	        // tell that there is already an activated subscriber.....
            $output = "NO-ALREADYACTIVATED"; 
        }
    }
    return $output;
} 


/**
 * Delete a subscriber (BY ADMIN/REGISTERED-USER)
 */
function ALO_em_delete_subscriber_by_id($id) {
    global $wpdb;
    $output = $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->prefix}easymail_subscribers WHERE ID=%d LIMIT 1", $id ) );
    return $output;
} 


/**
 * Delete a subscriber (BY SUBSCRIBER)
 */
function ALO_em_delete_subscriber_by_email($email, $unikey) {
    global $wpdb;
    $output = $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->prefix}easymail_subscribers WHERE email='%s' AND unikey='%s' LIMIT 1", $email, $unikey ) );
    return $output;
} 


/**
 * Check if can access subscription page (BY SUBSCRIBER)
 */
function ALO_em_can_access_subscrpage ($email, $unikey) {
    global $wpdb;
    // check if email and unikey match
    $check = ALO_em_check_subscriber_email_and_unikey ( $email, $unikey );
    return $check;
} 


/**
 * Check if subscriber email and unikey match (BY SUBSCRIBER) (check EMAIL<->UNIKEY)
 */
function ALO_em_check_subscriber_email_and_unikey ( $email, $unikey ) {
    global $wpdb;
    $check = $wpdb->get_var( $wpdb->prepare("SELECT ID FROM {$wpdb->prefix}easymail_subscribers WHERE email='%s' AND unikey='%s' LIMIT 1", $email, $unikey) );
    return $check;
} 


/**
 * Send email with activation link
 */
function ALO_em_send_activation_email($email, $name, $unikey, $lang) {
	$blogname = html_entity_decode ( wp_kses_decode_entities ( get_option('blogname') ) );
    // Headers
    $mail_sender = "noreply@". str_replace("www.","", $_SERVER['HTTP_HOST']);
    $headers =  "";//"MIME-Version: 1.0\n";
    $headers .= "From: ". $blogname ." <".$mail_sender.">\n";
    $headers .= "Content-Type: text/plain; charset=\"". get_bloginfo('charset') . "\"\n";
    
    /*
    // Subject
    // $subject = sprintf(__("Confirm your subscription to %s Newsletter", "alo-easymail"), $blogname );
   	$subject = ALO_em_translate_option ( $lang, 'ALO_em_txtpre_activationmail_subj', true ); 
   	$subject = str_replace ( "%BLOGNAME%", $blogname, $subject );
    */
       	
    // Main content    
    /*
 	$div_email = explode("@", $email); // for link
    $arr_params = array ('ac' => 'activate', 'em1' => $div_email[0], 'em2' => $div_email[1], 'uk' => $unikey, 'lang' => $lang);
	$sub_link = add_query_arg( $arr_params, get_page_link (get_option('ALO_em_subsc_page')) );
	//$sub_link = ALO_em_translate_url ( $sub_link, $lang );
    */
    /*   
   	$content = ALO_em_translate_option ( $lang, 'ALO_em_txtpre_activationmail_mail', true ); 
   	$content = str_replace ( "%BLOGNAME%", $blogname, $content );
   	$content = str_replace ( "%NAME%", $name, $content );
   	$content = str_replace ( "%ACTIVATIONLINK%", $sub_link, $content );
   	*/
   	
   	$content = "lang=$lang&email=$email&name=$name&unikey=$unikey";
   
    //echo "<br />".$headers."<br />".$subscriber->email."<br />". $subject."<br />".  $content ."<hr />" ; // DEBUG
    $sending = wp_mail( $email, /*$subject*/ "#_EASYMAIL_ACTIVATION_#", $content, $headers);  
    return $sending;
} 


/**
 * Print table with tags summay
 */
function ALO_em_tags_table () { ?>
	<table class="widefat" style="margin-top:10px">
	<thead><tr><th scope="col" style="width:20%"><?php _e("Post tags", "alo-easymail") ?></th><th scope="col"></th></tr></thead>
	<tbody>
	<tr><td>[POST-TITLE]</td><td style='font-size:80%'><span class="description"><?php _e("The link to the title of the selected post.", "alo-easymail") ?>. <?php _e("This tag works also in the <strong>subject</strong>", "alo-easymail") ?>.</span></td></tr>
	<tr><td>[POST-EXCERPT]</td><td style='font-size:80%'><span class="description"><?php _e("The excerpt (if any) of the post.", "alo-easymail") ?></span></td></tr>
	<tr><td>[POST-CONTENT]</td><td style='font-size:80%'><span class="description"><?php _e("The main content of the post.", "alo-easymail") ?> <?php _e("Warning: this tag inserts the test as it is, including shortcodes from other plugins.", "alo-easymail") ?></span></td></tr>
	</tbody></table>

	<table class="widefat" style="margin-top:10px">
	<thead><tr><th scope="col" style="width:20%"><?php _e("Subscriber tags", "alo-easymail") ?></th><th scope="col"></th></tr></thead>
	<tbody>
	<tr><td>[USER-NAME]</td><td style='font-size:80%'><span class="description"><?php _e("Name and surname of registered user.", "alo-easymail") ?> (<?php _e("For subscribers: the name used for registration", "alo-easymail") ?>)</span></td></tr>
	<!-- Following [USER-FIRST-NAME] added GAL -->
	<tr><td>[USER-FIRST-NAME]</td><td style='font-size:80%'><span class="description"><?php _e("First name of registered user.", "alo-easymail") ?> (<?php _e("For subscribers: the name used for registration", "alo-easymail") ?>).</span></td></tr>
	</tbody></table>

	<table class="widefat" style="margin-top:10px">
	<thead><tr><th scope="col" style="width:20%"><?php _e("Other tags", "alo-easymail") ?></th><th scope="col"></th></tr></thead>
	<tbody>
	<tr><td>[SITE-LINK]</td><td style='font-size:80%'><span class="description"><?php _e("The link to the site", "alo-easymail") ?>: <?php echo "<a href='".get_option ('siteurl')."'>".get_option('blogname')."</a>" ?></span></td></tr>
	</tbody></table>
<?php 
}
 


/*************************************************************************
 * AJAX 'SACK' FUNCTION
 *************************************************************************/ 

add_action('wp_head', 'ALO_em_ajax_js' );


function ALO_em_ajax_js()
{
  // use JavaScript SACK library for Ajax
  wp_print_scripts( array( 'sack' ));

?>
<script type="text/javascript">
//<![CDATA[
<?php if ( is_user_logged_in() ) { // if logged in ?>
function alo_em_user_form ( opt )
{
  // updating...
  document.getElementById('alo_easymail_widget_feedback').innerHTML = '';
  document.getElementById('alo_easymail_widget_feedback').className = 'alo_easymail_widget_error';
  document.getElementById('alo_em_widget_loading').style.display = "inline";  
  
   var mysack = new sack( 
       "<?php echo admin_url() ?>admin-ajax.php" );       

  mysack.execute = 1;
  mysack.method = 'POST';
  mysack.setVar( "action", "alo_em_user_form_check" );
  mysack.setVar( "alo_easymail_option", opt );
  <?php 
  $txt_ok 		= esc_attr( ALO_em___(__("Successfully updated", "alo-easymail")) );	
  $lang_code 	= ALO_em_get_language();
  ?>
  mysack.setVar( "alo_easymail_txt_success", '<?php echo $txt_ok ?>' );
  mysack.setVar( "alo_easymail_lang_code", '<?php echo $lang_code ?>' );
  
  var cbs = document.getElementById('alo_easymail_widget_form').getElementsByTagName('input');
  var length = cbs.length;
  var lists = "";
  for (var i=0; i < length; i++) {
  	if (cbs[i].name == 'alo_em_form_lists' +'[]' && cbs[i].type == 'checkbox') {
  		if ( cbs[i].checked ) lists += cbs[i].value + ",";
  	}
  }
  mysack.setVar( "alo_em_form_lists", lists );
  mysack.onError = function() { alert('Ajax error' )};
  mysack.runAJAX();

  return true;

} 
<?php } else {  // if not is_user_logged_in() ?>
function alo_em_pubblic_form ()
{
  <?php
  $error_email_incorrect 	= esc_attr( ALO_em___(__("The e-email address is not correct", "alo-easymail")) );
  $error_name_empty 		= esc_attr( ALO_em___(__("The name field is empty", "alo-easymail")) );
  $error_email_added		= esc_attr( ALO_em___(__("Warning: this email address has already been subscribed, but not activated. We are now sending another activation email", "alo-easymail")) );
  $error_email_activated	= esc_attr( ALO_em___(__("Warning: this email address has already been subscribed", "alo-easymail")) );  
  $error_on_sending			= esc_attr( ALO_em___(__("Error during sending: please try again", "alo-easymail")) );
  $txt_ok					= esc_attr( ALO_em___(__("Subscription successful. You will receive an e-mail with a link. You have to click on the link to activate your subscription.", "alo-easymail")) ); 
  $txt_subscribe			= esc_attr( ALO_em___(__("Subscribe", "alo-easymail")) );
  $txt_sending				= esc_attr( ALO_em___(__("sending...", "alo-easymail")) );
  $lang_code				= ALO_em_get_language();
  ?>
  document.alo_easymail_widget_form.submit.value="<?php echo $txt_sending ?>";
  document.alo_easymail_widget_form.submit.disabled = true;
  document.getElementById('alo_em_widget_loading').style.display = "inline";
  document.getElementById('alo_easymail_widget_feedback').innerHTML = "";
  
   var mysack = new sack( 
       "<?php echo admin_url() ?>admin-ajax.php" );    

  mysack.execute = 1;
  mysack.method = 'POST';
  mysack.setVar( "action", "alo_em_pubblic_form_check" );
  mysack.setVar( "alo_em_opt_name", document.alo_easymail_widget_form.alo_em_opt_name.value );
  mysack.setVar( "alo_em_opt_email", document.alo_easymail_widget_form.alo_em_opt_email.value );
  
  mysack.setVar( "alo_em_error_email_incorrect", "<?php echo $error_email_incorrect ?>");
  mysack.setVar( "alo_em_error_name_empty", "<?php echo $error_name_empty ?>");
  mysack.setVar( "alo_em_error_email_added", "<?php echo $error_email_added ?>");
  mysack.setVar( "alo_em_error_email_activated", "<?php echo $error_email_activated ?>");
  mysack.setVar( "alo_em_error_on_sending", "<?php echo $error_on_sending ?>");
  mysack.setVar( "alo_em_txt_ok", "<?php echo $txt_ok ?>");
  mysack.setVar( "alo_em_txt_subscribe", "<?php echo $txt_subscribe ?>");
  mysack.setVar( "alo_em_lang_code", "<?php echo $lang_code ?>");  
  
  var cbs = document.getElementById('alo_easymail_widget_form').getElementsByTagName('input');
  var length = cbs.length;
  var lists = "";
  for (var i=0; i < length; i++) {
  	if (cbs[i].name == 'alo_em_form_lists' +'[]' && cbs[i].type == 'checkbox') {
  		if ( cbs[i].checked ) lists += cbs[i].value + ",";
  	}
  }
  mysack.setVar( "alo_em_form_lists", lists );
  mysack.onError = function() { alert('Ajax error' )};
  mysack.runAJAX();

  return true;

} 
//]]>
<?php } // end if is_user_logged_in() ?>
</script>
<?php
} // end ALO_em_ajax_js

add_action('wp_ajax_alo_em_user_form_check', 'ALO_em_user_form_callback');				// logged in
add_action('wp_ajax_nopriv_alo_em_pubblic_form_check', 'ALO_em_pubblic_form_callback'); // pubblic, no logged in

// For logged-in users
function ALO_em_user_form_callback() {
	global $wpdb, $user_ID, $user_email, $current_user;
	get_currentuserinfo();
	//die ("alert(\"".$_POST['alo_easymail_option']."\")");
   	if ( $user_ID && isset($_POST['alo_easymail_option'])) {
   		switch ( $_POST['alo_easymail_option'] ) {
   			case "yes":
   				$lang = ( isset($_POST['alo_easymail_lang_code']) && in_array ( $_POST['alo_easymail_lang_code'], ALO_em_get_all_languages( false )) ) ? $_POST['alo_easymail_lang_code'] : "" ;
   				if ( get_user_meta($user_ID, 'first_name', true) != "" || get_user_meta($user_ID, 'last_name', true) != "" ) {
	    	 	   	$reg_name = ucfirst(get_user_meta($user_ID, 'first_name',true))." " .ucfirst(get_user_meta($user_ID,'last_name',true));
	    	 	} else {
	    	 		$reg_name = get_user_meta($user_ID, 'nickname', true);
	    	 	}	    	
	            ALO_em_add_subscriber($user_email, $reg_name, 1, $lang );
	            break;
			case "no":		
				ALO_em_delete_subscriber_by_id( ALO_em_is_subscriber($user_email) );
				break;
        	case "lists":
				$subscriber_id = ALO_em_is_subscriber ( $user_email );
				$mailinglists = ALO_em_get_mailinglists( 'public' );
				$lists = ( isset($_POST['alo_em_form_lists'])) ? explode ( ",", trim ( $_POST['alo_em_form_lists'] , "," ) ) : array();
				if ($mailinglists) {
					foreach ( $mailinglists as $mailinglist => $val) {					
						if ( in_array ( $mailinglist, $lists ) ) {
							ALO_em_add_subscriber_to_list ( $subscriber_id, $mailinglist );	  // add to list
						} else {
							ALO_em_delete_subscriber_from_list ( $subscriber_id, $mailinglist ); // remove from list
						}
					}
				}
				break;
		}
		// Compose JavaScript for return
		$feedback = "";
		$feedback .= "document.getElementById('alo_easymail_widget_feedback').innerHTML = '". $_POST['alo_easymail_txt_success'] .".';";
		$feedback .= "document.getElementById('alo_easymail_widget_feedback').className = 'alo_easymail_widget_ok';";
		$feedback .= "document.getElementById('alo_em_widget_loading').style.display = 'none';";
		// if unsubscribe deselect all lists
		if ( isset($_POST['alo_easymail_option']) && $_POST['alo_easymail_option']=="no" ) {
			$feedback .= "var cbs = document.getElementById('alo_easymail_widget_form').getElementsByTagName('input');";
			$feedback .= "var length = cbs.length;";
			$feedback .= "for (var i=0; i < length; i++) {";
			$feedback .= 	"if (cbs[i].name == 'alo_em_form_lists' +'[]' && cbs[i].type == 'checkbox') { cbs[i].checked = false; }";
			$feedback .= "}";
		}
		// END!	
		die($feedback);
    }
}

// For NOT-logged-in pubblic visitors
function ALO_em_pubblic_form_callback() {
	global $wpdb, $user_ID;
    if (isset($_POST['alo_em_opt_name']) && isset($_POST['alo_em_opt_email'])){
        $error_on_adding = "";
        $just_added = false;
		$name 	= stripslashes(trim($_POST['alo_em_opt_name']));
		$email	= stripslashes(trim($_POST['alo_em_opt_email']));
        if ( !is_email($email) ) {
            $error_on_adding .= stripslashes(trim($_POST['alo_em_error_email_incorrect'])). "<br />";
        }
        if ( $name == "") {
            $error_on_adding .= stripslashes(trim($_POST['alo_em_error_name_empty'])) . ".<br />";
        }
        if ($error_on_adding == "") { // if no error
            // try to add new subscriber (and send mail if necessary) and return TRUE if success
            $try_to_add = ALO_em_add_subscriber( $email, $name, 0, stripslashes(trim($_POST['alo_em_lang_code'])) ); 
            switch ($try_to_add) {
            	case "OK":
            		$just_added = true;
            		break;
            	case "NO-ALREADYADDED":
            		$error_on_adding = stripslashes(trim($_POST['alo_em_error_email_added'])). ".<br />";
	            	break;
               	case "NO-ALREADYACTIVATED":
               		$error_on_adding = stripslashes(trim($_POST['alo_em_error_email_activated'])). ".<br />";
	            	break;
	            default: // false
	            	$error_on_adding = stripslashes(trim($_POST['alo_em_error_on_sending'])) . ".<br />";
            }
            
            // if requested, add to lists
            if ( isset($_POST['alo_em_form_lists']) && count($_POST['alo_em_form_lists']) ) {
	            $lists = explode ( ",", trim ( $_POST['alo_em_form_lists'] , "," ) );
	            $subscriber = ALO_em_is_subscriber ( $email );
	            foreach ( $lists as $list ) {
					ALO_em_add_subscriber_to_list ( $subscriber, $list );
				}
	      	}
        } 
        if ($just_added == true) {
			$output = $_POST['alo_em_txt_ok'];   
       		$classfeedback = "alo_easymail_widget_ok";
        } else {
			$output = $error_on_adding;
        	$classfeedback = "alo_easymail_widget_error";
       	}

		// Compose JavaScript for return
		$feedback = "";
		$feedback .= "document.alo_easymail_widget_form.submit.disabled = false;";
		$feedback .= "document.alo_easymail_widget_form.submit.value = '". stripslashes(trim($_POST['alo_em_txt_subscribe'])). "';";
		$feedback .= "document.getElementById('alo_easymail_widget_feedback').innerHTML = '$output';";
		$feedback .= "document.getElementById('alo_easymail_widget_feedback').className = '$classfeedback';";
		$feedback .= "document.getElementById('alo_em_widget_loading').style.display = 'none';";
		// END!	
		die($feedback);
    }
}

/*************************************************************************
 * BATCH SENDING
 *************************************************************************/ 

/**
 * Add a new newsletter to batch sending
 */
function ALO_em_add_new_batch ( $user_ID, $subject, $content, $recipients, $tracking, $tag ) {
	global $wpdb;
	$add_newsletter = $wpdb->insert(
                "{$wpdb->prefix}easymail_sendings", 
                array( 'start_at' => get_date_from_gmt( date("Y-m-d H:i:s") ), 'last_at' => get_date_from_gmt( date("Y-m-d H:i:s") ), 'user' => $user_ID, 'subject' => $subject, 
                'content' => $content, 'sent' => '0', 'recipients' => $recipients, 'tracking' => $tracking, 'tag' => $tag )
            );
    return $add_newsletter;
}
	

/**
 * Delete a sent newsletter 
 */
function ALO_em_delete_newsletter ( $newsletter ) {
	global $wpdb;
	// delete newsletter
	$delete = $wpdb->query($wpdb->prepare( "DELETE FROM {$wpdb->prefix}easymail_sendings WHERE ID = %d", $newsletter ));
	// delete trackings
	$wpdb->query($wpdb->prepare( "DELETE FROM {$wpdb->prefix}easymail_trackings WHERE newsletter = %d", $newsletter ));
    return $delete;
}


/**
 * Create alt text content before sending newsletter 
 */
function ALO_em_alt_mail_body( $phpmailer ) {
	if( $phpmailer->ContentType == 'text/html' && $phpmailer->AltBody == '') {
		$plain_text = ALO_em_html2plain ( $phpmailer->Body );
		$phpmailer->AltBody = $plain_text;
	}
}
add_action( 'phpmailer_init', 'ALO_em_alt_mail_body' );


/**
 * Send the newsletter to a fraction of recipients every X minutes
 */
function ALO_em_batch_sending () {
	global $wpdb;
	
	// retrieve info of oldest newsletter to send
	$sending_info =  $wpdb->get_row("SELECT * FROM {$wpdb->prefix}easymail_sendings WHERE sent = 0 ORDER BY ID ASC LIMIT 1");
	
	// if no sending there is nothing to send: batch has finished
	if ($sending_info == false) return;
	
	// the recipient of sending
	$recipients = unserialize( $sending_info->recipients );
	
	// search the interval between now and previous sending
	$diff_time = strtotime( get_date_from_gmt( date("Y-m-d H:i:s") ) ) - strtotime($sending_info->last_at);
	// so... how much recipients for this interval? // (86400 = seconds in a day)
	$day_rate = get_option('ALO_em_dayrate');
	$tot_recs = max ( floor(($day_rate * $diff_time / 86400)) , 1); 
		
	// for each sent mail add 1 to recs
	$n_recs = 0;
 
    for ($r=0; $r < count($recipients); $r++) {  
    
    	// if already sent to this recipient skip it
    	if ($recipients[$r]['result'] != "") {
    	   	continue; // go to next rec
    	}
    	
    	$rec_lang = ( !empty($recipients[$r]['lang']) ) ? $recipients[$r]['lang'] : ALO_em_get_language ();
		
		$subject = stripslashes ( ALO_em_translate_text ( $rec_lang, $sending_info->subject ) );    	
        
        // For each recipient delete TAGs update
        $updated_content = ALO_em_translate_text ( $rec_lang, $sending_info->content );

		// Retrieve post info for TAG
		$pID = ( isset($sending_info->tag) && (int)$sending_info->tag ) ? $sending_info->tag: false;
		if ($pID) $obj_post = get_post( $pID );
    		
		// TAG: [POST-TITLE]
		if ($pID) {
			$post_title = stripslashes ( ALO_em_translate_text ( $rec_lang, $obj_post->post_title ) );
		    $updated_content = str_replace("[POST-TITLE]", "<a href='". esc_url ( ALO_em_translate_url( get_permalink($obj_post->ID), $rec_lang )). "'>". $post_title ."</a>", $updated_content);      
		    $subject = str_replace('[POST-TITLE]', $post_title, $subject);
		} else {
		    $updated_content = str_replace("[POST-TITLE]", "", $updated_content);
		}

		// TAG: [POST-CONTENT]
		if ($pID) {
			$postcontent =  stripslashes ( ALO_em_translate_text ( $rec_lang, $obj_post->post_content ) );
			$postcontent = str_replace("\n", "<br />", $postcontent);
			// trim <br> added when rendering html tables (thanks to gunu)
			$postcontent = str_replace( array("<br /><t", "<br/><t", "<br><t"), "<t", $postcontent);
			$postcontent = str_replace( array("<br /></t", "<br/></t", "<br></t"), "</t", $postcontent);

		    $updated_content = str_replace("[POST-CONTENT]", $postcontent, $updated_content);
		} else {
		    $updated_content = str_replace("[POST-CONTENT]", "", $updated_content);
		}
		
		// TAG: [POST-EXCERPT] - if any
		if ($pID && !empty($obj_post->post_excerpt)) {
			$post_excerpt = stripslashes ( ALO_em_translate_text ( $rec_lang, $obj_post->post_excerpt ) );
		    $updated_content = str_replace("[POST-EXCERPT]", $post_excerpt, $updated_content);       
		} else {
		    $updated_content = str_replace("[POST-EXCERPT]", "", $updated_content);
		}
		
		// TAG: [SITE-LINK]
		$updated_content = str_replace("[SITE-LINK]", "<a href='".get_option ('siteurl')."'>".get_option('blogname')."</a>", $updated_content);       
		       
        // TAG: [USER-NAME]
        if ($recipients[$r]['name']) {
            $updated_content = str_replace("[USER-NAME]", stripslashes ( $recipients[$r]['name'] ), $updated_content);     
        } else {
            $updated_content = str_replace("[USER-NAME]", "", $updated_content);
        }            
        
        // TAG: [USER-FIRST-NAME]
        if ($recipients[$r]['firstname']) {
            $updated_content = str_replace("[USER-FIRST-NAME]", stripslashes ($recipients[$r]['firstname'] ), $updated_content);       
        } else {
            $updated_content = str_replace("[USER-FIRST-NAME]", "", $updated_content);
        }            

	    // Unsubscribe link, only if subscriber
		if ($recipients[$r]['unikey']) {
			$div_email = explode("@", $recipients[$r]['email']); // for link
		             
		   	$arr_params = array ('ac' => 'unsubscribe', 'em1' => $div_email[0], 'em2' => $div_email[1], 'uk' => $recipients[$r]['unikey'] );
			$uns_link = add_query_arg( $arr_params, get_page_link (get_option('ALO_em_subsc_page')) );
			$uns_link = ALO_em_translate_url ($uns_link, $rec_lang);

		   	if ( ALO_em_translate_option ( $rec_lang, 'ALO_em_custom_unsub_footer', false ) ) {
				$updated_content .= ALO_em_translate_option ( $rec_lang, 'ALO_em_custom_unsub_footer', false );
			} else {
				$updated_content .= "<p><em>". __("You have received this message because you subscribed to our newsletter. If you want to unsubscribe: ", "alo-easymail")." ";
				$updated_content .=	__("visit this link", "alo-easymail") ."<br /> %UNSUBSCRIBELINK%";//." <a href='" . $uns_link ."'>". $uns_link ."</a>.";
				$updated_content .= "</em></p>";
			}
			$updated_content = str_replace ( "%UNSUBSCRIBELINK%", " <a href='".$uns_link."'>". $uns_link ."</a>", $updated_content );
		    
		 	// TRACKING, if requested
			if ( $sending_info->tracking ) {
				switch ( $sending_info->tracking ) {
					case "ALO_EM": 	// default tracking: add a png image through a link to a php tracking page
						$updated_content .= "<img src='". ALO_EM_PLUGIN_URL ."/tr.php?n=".$sending_info->ID."&amp;e1=".$div_email[0]."&amp;e2=".$div_email[1]."&amp;k=".$recipients[$r]['unikey']."' width='1' height='1' border='0' >";
						break;
				}
			}
	    }

		$mail_sender = (get_option('ALO_em_sender_email')) ? get_option('ALO_em_sender_email') : "noreply@". str_replace("www.","", $_SERVER['HTTP_HOST']);
		$from_name = html_entity_decode ( wp_kses_decode_entities ( get_option('ALO_em_sender_name') ) );
		
		$headers =  "";//"MIME-Version: 1.0\n";
		$headers .= "From: ". $from_name ." <".$mail_sender.">\n";
		$headers .= "Content-Type: text/html; charset=\"" . strtolower( get_option('blog_charset') ) . "\"\n";		
		
        // ---- Send MAIL ----
        $mail_engine = @wp_mail($recipients[$r]['email'], $subject, $updated_content, $headers );  
        
        if( $mail_engine && is_email($recipients[$r]['email']) ) {
            $recipients[$r]['result'] = 1;
        } else {
            $recipients[$r]['result'] = -1;
        }
        
        // add as sent
  		$n_recs ++;
  		
        // sent to all of this sending? or too much sending stop sending!
        if ( $n_recs == $tot_recs || $n_recs >= get_option('ALO_em_batchrate') ) break;
        
        // after each email it sleep a little: (x')/n°recipients 
        //$timesleep = max (floor ( ALO_EM_INTERVAL_MIN *60 / $tot_recs ), 1);
		//sleep($timesleep);
		//sleep(1);
    }
		
   	// check if batch completed
   	$has_finished = 1;
   	foreach ($recipients as $recipient) {
   		if ( !isset($recipient['result']) ) {
   			$has_finished = 0;
   			break;
   		}
   	}
   		
	// update sending info
	$wpdb->update("{$wpdb->prefix}easymail_sendings",
                  array( 'last_at' => get_date_from_gmt( date("Y-m-d H:i:s") ), 'recipients' => serialize ($recipients), 'sent' => $has_finished ),
                  array( 'ID' => $sending_info->ID )
                 );
   	   	
}


/*************************************************************************
 * MAILING LISTS & RECIPIENTS FUNCTIONS
 *************************************************************************/ 


/**
 * Get all registered users of the blog 
 * return object with info as in table column
 */
function ALO_em_get_recipients_registered () {
	global $wpdb, $blog_id;
	if ( function_exists('is_multisite') ) { // compatibility with WP pre-3.x
      	$is_multisite = is_multisite();
   	} else {
   		$is_multisite = false;
   	}
	$where_ms_blog = ( $is_multisite ) ? " JOIN {$wpdb->usermeta} AS um ON um.user_id = u.ID WHERE um.meta_key = 'primary_blog' AND um.meta_value = '$blog_id'" : "";
	return $wpdb->get_results( "SELECT u.ID AS UID, user_email, s.lang AS lang FROM {$wpdb->users} AS u LEFT JOIN {$wpdb->prefix}easymail_subscribers AS s ON u.user_email = s.email ".$where_ms_blog );
	// to allow a right importation in multisite (thanks to RavanH !)
	/*
	$wp_user_search = new WP_User_Search();
	$wp_user_search->users_per_page = 3000;//PHP_INT_MAX;
	$reg_users = $wp_user_search->get_results();
	foreach ( $reg_users as $reg_user ) {
		//$reg_users[] = (object) array_merge( array('UID' => $reg_user), (array) get_userdata($reg_user) );
		$user = get_userdata($reg_user);
		$lang = $wpdb->get_var( "SELECT lang FROM {$wpdb->prefix}easymail_subscribers WHERE email='{$user->user_email}'" );
		$reg_users[] = (object) array( 'UID' => $reg_user, 'user_email' => $user->user_email, 'lang' => $lang );
	}
	return $reg_users;
	*/
}


/**
 * Get ALL subscribers OR only by SELECTED lists
 * @lists	array	only by selected lists 		
 * return object with info as in table column 
 */
function ALO_em_get_recipients_subscribers ( $lists=false ) {
	global $wpdb;
	$where_lists = "";
	if ( $lists && !is_array($lists) ) $lists = array ( $lists );
	if ( $lists ) {
		$where_lists .= " AND (";
		foreach ( $lists as $list ) {
			$where_lists .= "lists LIKE '%_".$list."_%' OR ";
		}
		$where_lists = substr( $where_lists , 0, -3); // cut last "OR"
		$where_lists .= ")";
	}
	return $wpdb->get_results( "SELECT * FROM {$wpdb->prefix}easymail_subscribers WHERE active='1' $where_lists" );
}


/**
 * Count subscribers reading the selected language
 * param	lang		if false return no langs or no longer available langs
 * param	active		if only activated subscribers or all subscribers
 * return int
 */
function ALO_em_count_subscribers_by_lang ( $lang=false, $only_activated=false ) {
	global $wpdb;
	if ( $lang ) {
		$str_lang = "lang='$lang'";
	} else {
		// search with no selected langs or old langs now not requested
		$langs = ALO_em_get_all_languages();
		$str_lang = "lang IS NULL OR lang NOT IN (";
		if ( is_array($langs) ) { 
			foreach ( $langs as $k => $l ) {
				$str_lang .= "'$l',";
			}
		}
		$str_lang = rtrim ($str_lang, ",");
		$str_lang .= ")" ;
	}
	$str_activated = ( $only_activated ) ? " AND active = '1'" : "";
	return $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}easymail_subscribers WHERE $str_lang $str_activated" );
}


/**
 * Get the mailing lists (as array)
 * @types  str		list types requested (a string with comma: eg. 'hidden,admin,public')
 */
function ALO_em_get_mailinglists ( $types = false ) {
	$get = get_option('ALO_em_mailinglists');
	if ( $types == false ) {
		$types = array ( 'hidden', 'admin', 'public' ); // default types	
	} else {
		$types = explode (",", $types);
	}
 	if ( empty($get) ) {
		return false;
	} else {
		$mailinglists = maybe_unserialize($get);
		$mailinglists = ALO_em_msort ($mailinglists,'order', 'ASC');//($mailinglists,'order', false);
		foreach ( $mailinglists as $list => $val) { // don't return unrequested types
			if ( !in_array( $val['available'], $types ) ) unset ($mailinglists[$list]);
		}
		return (array)$mailinglists;
	}
}


/**
 * Save the mailing lists
 * @lists  array
 */
function ALO_em_save_mailinglists ( $lists ) {
	if ( !is_array ($lists) ) return false;
	$arraylists = $lists; // maybe_serialize( $lists );
	update_option ( 'ALO_em_mailinglists', $arraylists );
	return true;
}


/**
 * Add a mailing list subscription to a subscriber (and save in db the new list)
 * @subscriber		
 * @list			
 */
function ALO_em_add_subscriber_to_list ( $subscriber, $list ) {
	global $wpdb;
	$user_lists = ALO_em_get_user_mailinglists ( $subscriber );
	if ( $user_lists && in_array($list, $user_lists) ) return; // if already, exit
	$user_lists[] = $list; // add the list
	asort ( $user_lists ); // order id from min to max, 1->9
	$updated_lists = implode ( "_", $user_lists );
	$updated_lists = "_".$updated_lists."_";
    return $wpdb->update( "{$wpdb->prefix}easymail_subscribers", array ( 'lists' => $updated_lists ), array ( 'ID' => $subscriber ) );
}


/**
 * Delete subscriber from mailing list
 * @subscriber		
 * @list		
 */
function ALO_em_delete_subscriber_from_list ( $subscriber, $list ) {
	global $wpdb;
	return $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->prefix}easymail_subscribers SET lists = REPLACE(lists, '_%d_', '_') WHERE ID=%d", $list, $subscriber ) );
}


/**
 * Delete ALL subscribers from mailing list(s)
 * @lists	array of lists ID
 */
function ALO_em_delete_all_subscribers_from_lists ( $lists ) {
	global $wpdb;
	if ( !is_array($lists) ) $lists = array ( $lists );
	foreach ( $lists as $list ) {
		$wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->prefix}easymail_subscribers SET lists = REPLACE(lists, '_%d_', '_')", $list ) );
	}
	return true;
}


/**
 * Get the user mailing lists
 * @array_lists		array of lists ID
 */
function ALO_em_get_user_mailinglists ( $subscr_id ) {
	global $wpdb;
	$lists = $wpdb->get_var ( $wpdb->prepare( "SELECT lists FROM {$wpdb->prefix}easymail_subscribers WHERE ID = %d", $subscr_id ) );
	if ( $lists	) {
		$array_lists = explode ( "_", trim ($lists, "_" ) );
		if ( is_array($array_lists) && $array_lists[0] != false  ) {
			asort ( $array_lists ); // order id from min to max, 1->9
			return (array)$array_lists;
		} else {
			return false;
		}		
	} else {
		return false;
	}
}


/**
 * Creates a html table with checkbox lists to edit own subscription
 * @user_email		str		subscriber email
 * @cssclass		str		the class css for the html table
 */
function ALO_em_html_mailinglists_table_to_edit ( $user_email, $cssclass="" ) {
	$html = "";
	$lists_msg 	= ( ALO_em_translate_option ( ALO_em_get_language (), 'ALO_em_custom_lists_msg',false) !="") ? ALO_em_translate_option ( ALO_em_get_language (), 'ALO_em_custom_lists_msg',false) :  __("You can also sign up for specific lists", "alo-easymail");  
    $mailinglists = ALO_em_get_mailinglists( 'public' );
    if ( $mailinglists ) {
	    $subscriber_id = ALO_em_is_subscriber( $user_email );
	    $user_lists = ALO_em_get_user_mailinglists ( $subscriber_id );
		$html .= "<table ". (($cssclass!="")? " class='$cssclass' " : "") ."><tbody>\n"; 
		$html .= "<tr><th ". (($cssclass=="")? " style='width:50%' ":"") .">". $lists_msg	.":</th>\n";
		$html .= "<td>\n";
		foreach ( $mailinglists as $list => $val ) {
			$checked = ( $user_lists && in_array ( $list, $user_lists )) ? "checked='checked'" : "";
			$html .= "<input type='checkbox' name='alo_em_profile_lists[]' id='alo_em_profile_list_$list' value='$list' $checked /> " . ALO_em_translate_multilangs_array ( ALO_em_get_language(), $val['name'], true ) ."<br />\n";
		}
		$html .= "</td></tr>\n";
		$html .= "</tbody></table>\n";
	} 
	return $html;
}



/*************************************************************************
 * TRACKING FUNCTIONS
 *************************************************************************/ 

/**
 * If recipient view has already tracked (eg. if he has opened the newsletter)
 * @type	str 	the type of tracking, now available: 'V' = when newsletter is openend and viewed
 * return ID tracking, otherwise false
 */
function ALO_em_recipient_is_tracked ( $email, $newsletter, $type='V' ) {
	global $wpdb;
	$check = $wpdb->get_var( $wpdb->prepare("SELECT ID FROM {$wpdb->prefix}easymail_trackings WHERE email='%s' AND newsletter=%d AND type=%s LIMIT 1", $email, $newsletter, $type ) );
	return $check;
}


/**
 * insert a new tracking in db
 */
function ALO_em_add_tracking ( $email, $newsletter, $type='V' ) {
	global $wpdb;
	$wpdb->query( $wpdb->prepare( "INSERT INTO {$wpdb->prefix}easymail_trackings ( newsletter, email, type ) VALUES ( %d, %s, %s )", array( $newsletter, $email, $type ) ) );
}



/*************************************************************************
 * TEMPLATES
 *************************************************************************/ 

/**
 * Add a new template
 */
function ALO_em_add_new_template ( $user_ID, $subject, $content ) {
	global $wpdb;
	$add_newsletter = $wpdb->insert(
                "{$wpdb->prefix}easymail_sendings", 
                array( 'start_at' => get_date_from_gmt( date("Y-m-d H:i:s") ), 'last_at' => get_date_from_gmt( date("Y-m-d H:i:s") ), 'user' => $user_ID, 'subject' => $subject, 
                'content' => $content, 'sent' => '9', 'recipients' => '', 'tracking' => '' )
            );
    return $add_newsletter;
}


/**
 * Update an existing template
 */
function ALO_em_update_template ( $tpl_id, $user_ID, $subject, $content ) {
	global $wpdb;
    $update = $wpdb->update(    "{$wpdb->prefix}easymail_sendings",
                            array ( 'last_at' => get_date_from_gmt( date("Y-m-d H:i:s") ), 'subject' => $subject, 'content' => $content ),
                            array ( 'ID' => $tpl_id )
                        );
    return $update;
}


/**
 * Count how many templates of an user
 */
function ALO_em_how_user_templates ( $user_ID ) {
	global $wpdb;
	$tpls = $wpdb->get_var( $wpdb->prepare("SELECT COUNT(ID) FROM {$wpdb->prefix}easymail_sendings WHERE sent='9' AND user='%d'", $user_ID ) );
    return (int) $tpls;
}



/*************************************************************************
 * MULTILANGUAGE
 *************************************************************************/ 


/**
 * Check if there is a multiplanguage enabled plugin 
 * return the name of plugin, or false
 */
function ALO_em_multilang_enabled_plugin () {
	// 1st choice: qTranslate
	global $q_config;
	if( function_exists( 'qtrans_init') && isset($q_config) ) {
		return "qTrans";
	}
	
	// TODO other choices...
	
	// no plugin: return false
	return false;
}


/**
 * Return a text after applying a multilanguage filter 
 */
function ALO_em___ ( $text ) {
	// 1st choice: using qTranslate
	if( ALO_em_multilang_enabled_plugin() == "qTrans" && function_exists( 'qtrans_useCurrentLanguageIfNotFoundUseDefaultLanguage') ) {
		return qtrans_useCurrentLanguageIfNotFoundUseDefaultLanguage ( $text );
	}
	// TODO other choices...

	// last case: return without translating
	return $text ;
}

/**
 * Echo a text after applying a multilanguage filter (based on 'ALO_em___')
 */
function ALO_em__e ( $text ) {
	echo ALO_em___ ( $text );
}



/**
 * Return a text after applying a multilanguage filter 
 */
function ALO_em_translate_text ( $lang, $text ) {
	if ( empty($lang) ) $lang = ALO_em_short_langcode ( get_locale() ); // default lang
	
	// 1st choice: using qTranslate
	if( ALO_em_multilang_enabled_plugin() == "qTrans" && function_exists( 'qtrans_use') ) {
		return qtrans_use ( $lang, $text, false);
	}
	// TODO other choices...

	// last case: return as is
	return $text ;
}


/**
 * Return a text of the requested lang from a saved option or default option
 * param	fallback	if requested lang not exists and fallback true returns a lang default
 */
function ALO_em_translate_option ( $lang, $key , $fallback=true ) {
	$default_lang = ALO_em_short_langcode ( get_locale() ); // default lang
	$fallback_lang = "en"; // latest default...
	$text_1 = $text_2 = $text_3 = false;

	// from default option if exists
	if ( get_option( $key."_default" ) ) {
		$get = get_option( $key."_default" );
		if ( is_array($get) ) {
			foreach ( $get as $k => $v ) {
				if ( $k == $lang )			$text_1 = $v;	// the requested lang
				if ( $k == $default_lang )	$text_2 = $v;	// the default lang
				if ( $k == $fallback_lang ) $text_3 = $v;	// the fallback lang
			}
		}
	}
		
	// from option
	if ( get_option( $key ) ) {
		$get = get_option( $key );
		if ( is_array($get) ) {
			foreach ( $get as $k => $v ) {
				if ( !empty($v) ) { // if not empty
					if ( $k == $lang )			$text_1 = $v;	// the requested lang
					if ( $k == $default_lang )	$text_2 = $v;	// the default lang
					if ( $k == $fallback_lang ) $text_3 = $v;	// the fallback lang
				}
			}
		}
	}
	
	if ( $text_1 ) return $text_1;
	if ( $text_2 && $fallback ) return $text_2;	
	if ( $text_3 && $fallback ) return $text_3;
	return false;
}


/**
 * Return a text of the requested lang from an array with same text in several langs ( "en" => "hi", "es" => "hola"...)
 * param	fallback	if requested lang not exists and fallback true returns a lang default
 */
function ALO_em_translate_multilangs_array ( $lang, $array, $fallback=true ) {
	if ( !is_array($array) ) return $array; // if not array, return the text
	
	$default_lang = ALO_em_short_langcode ( get_locale() ); // default lang
	$fallback_lang = "en"; // latest default...
	$text_1 = $text_2 = $text_3 = false;
	
	foreach ( $array as $k => $v ) {
		if ( $k == $lang ) 			$text_1 = $v;	// the requested lang
		if ( $k == $default_lang ) 	$text_2 = $v;	// the default lang
		if ( $k == $fallback_lang ) $text_3 = $v;	// the fallback lang
	}
	
	if ( $text_1 ) return $text_1;
	if ( $text_2 && $fallback ) return $text_2;	
	if ( $text_3 && $fallback ) return $text_3;
	return false;
}


/** 
 * Return the url localised for the requested lang 
 */
function ALO_em_translate_url ( $url, $lang ) {

	// 1st choice: using qTranslate
	if( ALO_em_multilang_enabled_plugin() == "qTrans" && function_exists( 'qtrans_convertURL') ) {
		//return qtrans_convertURL( $url, $lang ); // TODO
		return add_query_arg( "lang", $lang, $url );
	}
	
	// TODO other choices...
	
	// last case: return th url with a "lang" var... maybe it could be useful...
	return add_query_arg( "lang", $lang, $url );
}


/**
 * Return the current language
 */
function ALO_em_get_language () {
	// 1st choice: using qTranslate
	if( ALO_em_multilang_enabled_plugin() == "qTrans" && function_exists( 'qtrans_getLanguage') ) {
		return strtolower( qtrans_getLanguage() );
	}
	
	// TODO other choices...
	
	// default: get from browser, only if the lang .mo is available on blog
	$lang = ALO_em_short_langcode ( $_SERVER['HTTP_ACCEPT_LANGUAGE'] );
	if ( !empty($lang) && in_array($lang, ALO_em_get_all_languages(false)) ) {
		return $lang;
	}
	
	// last case... return empty
	return "";
}

/**
 * Return 2 chars lowercase lang code (eg. from "it_IT" to "it")
 */
function ALO_em_short_langcode ( $lang ) {
	return strtolower ( substr( $lang, 0, 2) );
}

/**
 * Return the long name of language
 */
function ALO_em_get_lang_name ( $lang_code ) {
	global $q_config;
	$lang_code = ALO_em_short_langcode( $lang_code );
	if ( ALO_em_multilang_enabled_plugin() == "qTrans" && isset($q_config) ) { // qTranslate
		$name = $q_config['language_name'][$lang_code];
	} else { // default
		$longname = ALO_em_format_code_lang ( $lang_code );
		$splitname = explode ( ";", $longname );
		$name = $splitname[0];
	}
	return $name;
}


/**
 * Return the lang flag
 * param 	fallback	if there is not the image, return the lang code ('code') or lang name ('name') or nothing
 */
function ALO_em_get_lang_flag ( $lang_code, $fallback=false ) {
	global $q_config;
	if ( empty($lang_code) ) return; 
	$flag = false;
	$lang_code =  ALO_em_short_langcode ( $lang_code );
	if ( ALO_em_multilang_enabled_plugin() == "qTrans" && isset($q_config) ) { // qTranslate
		if ( $lang_code == "en" && !file_exists ( trailingslashit(WP_CONTENT_DIR).$q_config['flag_location']. $lang_code .".png" ) ) {
			$img_code = "gb";
		} else {
			$img_code = $lang_code;
		}
		$flag = "<img src='". trailingslashit(WP_CONTENT_URL).$q_config['flag_location']. $img_code .".png' alt='".$q_config['language_name'][$lang_code]."' title='".$q_config['language_name'][$lang_code]."' />" ;
	} else { // default
		if ( $fallback == "code" ) $flag = $lang_code;
		if ( $fallback == "name" ) $flag = ALO_em_get_lang_name ( $lang_code );
	}
	return $flag;
}


/**
 * Return an array with availables languages
 * param 	by_users	if true and no other translation plugins get all langs chosen by users, if not only langs installed on blog
 */
function ALO_em_get_all_languages ( $fallback_by_users=false ) {
	global $wp_version;
	
	// 1st choice: using qTranslate
	if( ALO_em_multilang_enabled_plugin() == "qTrans" && function_exists( 'qtrans_getSortedLanguages') ) {
		return qtrans_getSortedLanguages();
	}
		
	// 2nd choise: wp default detection
	$languages = array();
	foreach( (array)glob( WP_LANG_DIR  . '/*.mo' ) as $lang_file ) {
		$lang_file = basename($lang_file, '.mo');
		if ( 0 !== strpos( $lang_file, 'continents-cities' ) && 0 !== strpos( $lang_file, 'ms-' ) )
			$languages[] = ALO_em_short_langcode( $lang_file );
	}
	if ( !empty ($languages[0]) ) return $languages;
	
	
	// last case: return all langs chosen by users or default
	if ( $fallback_by_users ) {
		return ALO_em_get_all_languages_by_users();
	} else {
		return array( ALO_em_short_langcode ( get_locale() ) );
	}	
}


/**
 * Return an array with all languages chosen by users
 */
function ALO_em_get_all_languages_by_users () {
	global $wpdb;
	$langs = $wpdb->get_results( "SELECT lang FROM {$wpdb->prefix}easymail_subscribers GROUP BY lang" , ARRAY_N );
	if ( $langs ) {
		$output = array();
		foreach ( $langs as $key => $val ) {
			if ( !empty($val[0]) ) $output[] = $val[0];
		}
		return $output;
	} else {
		return array( ALO_em_short_langcode ( get_locale() ) );
	}
}



/**
 * Return the long name of language
 */
function ALO_em_format_code_lang( $code = '' ) {
	$code = strtolower( substr( $code, 0, 2 ) );
	$lang_codes = array(
		'aa' => 'Afar', 'ab' => 'Abkhazian', 'af' => 'Afrikaans', 'ak' => 'Akan', 'sq' => 'Albanian', 'am' => 'Amharic', 'ar' => 'Arabic', 'an' => 'Aragonese', 'hy' => 'Armenian', 'as' => 'Assamese', 'av' => 'Avaric', 'ae' => 'Avestan', 'ay' => 'Aymara', 'az' => 'Azerbaijani', 'ba' => 'Bashkir', 'bm' => 'Bambara', 'eu' => 'Basque', 'be' => 'Belarusian', 'bn' => 'Bengali',
		'bh' => 'Bihari', 'bi' => 'Bislama', 'bs' => 'Bosnian', 'br' => 'Breton', 'bg' => 'Bulgarian', 'my' => 'Burmese', 'ca' => 'Catalan; Valencian', 'ch' => 'Chamorro', 'ce' => 'Chechen', 'zh' => 'Chinese', 'cu' => 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic', 'cv' => 'Chuvash', 'kw' => 'Cornish', 'co' => 'Corsican', 'cr' => 'Cree',
		'cs' => 'Czech', 'da' => 'Danish', 'dv' => 'Divehi; Dhivehi; Maldivian', 'nl' => 'Dutch; Flemish', 'dz' => 'Dzongkha', 'en' => 'English', 'eo' => 'Esperanto', 'et' => 'Estonian', 'ee' => 'Ewe', 'fo' => 'Faroese', 'fj' => 'Fijjian', 'fi' => 'Finnish', 'fr' => 'French', 'fy' => 'Western Frisian', 'ff' => 'Fulah', 'ka' => 'Georgian', 'de' => 'German', 'gd' => 'Gaelic; Scottish Gaelic',
		'ga' => 'Irish', 'gl' => 'Galician', 'gv' => 'Manx', 'el' => 'Greek, Modern', 'gn' => 'Guarani', 'gu' => 'Gujarati', 'ht' => 'Haitian; Haitian Creole', 'ha' => 'Hausa', 'he' => 'Hebrew', 'hz' => 'Herero', 'hi' => 'Hindi', 'ho' => 'Hiri Motu', 'hu' => 'Hungarian', 'ig' => 'Igbo', 'is' => 'Icelandic', 'io' => 'Ido', 'ii' => 'Sichuan Yi', 'iu' => 'Inuktitut', 'ie' => 'Interlingue',
		'ia' => 'Interlingua (International Auxiliary Language Association)', 'id' => 'Indonesian', 'ik' => 'Inupiaq', 'it' => 'Italian', 'jv' => 'Javanese', 'ja' => 'Japanese', 'kl' => 'Kalaallisut; Greenlandic', 'kn' => 'Kannada', 'ks' => 'Kashmiri', 'kr' => 'Kanuri', 'kk' => 'Kazakh', 'km' => 'Central Khmer', 'ki' => 'Kikuyu; Gikuyu', 'rw' => 'Kinyarwanda', 'ky' => 'Kirghiz; Kyrgyz',
		'kv' => 'Komi', 'kg' => 'Kongo', 'ko' => 'Korean', 'kj' => 'Kuanyama; Kwanyama', 'ku' => 'Kurdish', 'lo' => 'Lao', 'la' => 'Latin', 'lv' => 'Latvian', 'li' => 'Limburgan; Limburger; Limburgish', 'ln' => 'Lingala', 'lt' => 'Lithuanian', 'lb' => 'Luxembourgish; Letzeburgesch', 'lu' => 'Luba-Katanga', 'lg' => 'Ganda', 'mk' => 'Macedonian', 'mh' => 'Marshallese', 'ml' => 'Malayalam',
		'mi' => 'Maori', 'mr' => 'Marathi', 'ms' => 'Malay', 'mg' => 'Malagasy', 'mt' => 'Maltese', 'mo' => 'Moldavian', 'mn' => 'Mongolian', 'na' => 'Nauru', 'nv' => 'Navajo; Navaho', 'nr' => 'Ndebele, South; South Ndebele', 'nd' => 'Ndebele, North; North Ndebele', 'ng' => 'Ndonga', 'ne' => 'Nepali', 'nn' => 'Norwegian Nynorsk; Nynorsk, Norwegian', 'nb' => 'Bokmål, Norwegian, Norwegian Bokmål',
		'no' => 'Norwegian', 'ny' => 'Chichewa; Chewa; Nyanja', 'oc' => 'Occitan, Provençal', 'oj' => 'Ojibwa', 'or' => 'Oriya', 'om' => 'Oromo', 'os' => 'Ossetian; Ossetic', 'pa' => 'Panjabi; Punjabi', 'fa' => 'Persian', 'pi' => 'Pali', 'pl' => 'Polish', 'pt' => 'Portuguese', 'ps' => 'Pushto', 'qu' => 'Quechua', 'rm' => 'Romansh', 'ro' => 'Romanian', 'rn' => 'Rundi', 'ru' => 'Russian',
		'sg' => 'Sango', 'sa' => 'Sanskrit', 'sr' => 'Serbian', 'hr' => 'Croatian', 'si' => 'Sinhala; Sinhalese', 'sk' => 'Slovak', 'sl' => 'Slovenian', 'se' => 'Northern Sami', 'sm' => 'Samoan', 'sn' => 'Shona', 'sd' => 'Sindhi', 'so' => 'Somali', 'st' => 'Sotho, Southern', 'es' => 'Spanish; Castilian', 'sc' => 'Sardinian', 'ss' => 'Swati', 'su' => 'Sundanese', 'sw' => 'Swahili',
		'sv' => 'Swedish', 'ty' => 'Tahitian', 'ta' => 'Tamil', 'tt' => 'Tatar', 'te' => 'Telugu', 'tg' => 'Tajik', 'tl' => 'Tagalog', 'th' => 'Thai', 'bo' => 'Tibetan', 'ti' => 'Tigrinya', 'to' => 'Tonga (Tonga Islands)', 'tn' => 'Tswana', 'ts' => 'Tsonga', 'tk' => 'Turkmen', 'tr' => 'Turkish', 'tw' => 'Twi', 'ug' => 'Uighur; Uyghur', 'uk' => 'Ukrainian', 'ur' => 'Urdu', 'uz' => 'Uzbek',
		've' => 'Venda', 'vi' => 'Vietnamese', 'vo' => 'Volapük', 'cy' => 'Welsh','wa' => 'Walloon','wo' => 'Wolof', 'xh' => 'Xhosa', 'yi' => 'Yiddish', 'yo' => 'Yoruba', 'za' => 'Zhuang; Chuang', 'zu' => 'Zulu' );
	//$lang_codes = apply_filters( 'lang_codes', $lang_codes, $code );
	return strtr( $code, $lang_codes );
}


/**
 * Create options (if not exist yet) with array of pre-domain text in all languages
 * param 	reset_defaults		if yes create defaults (useful also if new langs installed)
 */
 
function ALO_em_setup_predomain_texts( $reset_defaults = false ) {
	//Required pre-domain text
	require_once( 'languages/alo-easymail-predomain.php');
	
	global $alo_em_textpre;
	foreach ( $alo_em_textpre as $key => $sub ) {
		// add/update only if not exists or forced
		if ( !get_option($key.'_default') || $reset_defaults ) {
			update_option ( $key.'_default', $sub );
		}
	}
}

/**
 * Assign a subscriber to a language	
 */
function ALO_em_assign_subscriber_to_lang ( $subscriber, $lang ) {
	global $wpdb;
	$wpdb->update(    "{$wpdb->prefix}easymail_subscribers",
		            array ( 'lang' => $lang ),
		            array ( 'ID' => $subscriber )
		        );
}

?>
