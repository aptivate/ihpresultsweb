<?php // No direct access, only through WP
if(preg_match('#' . basename(__FILE__) . '#', $_SERVER['PHP_SELF'])) die('You can\'t call this page directly.'); 
if ( !current_user_can('send_easymail_newsletters') && !current_user_can('manage_easymail_newsletters') ) 	wp_die(__('Cheatin&#8217; uh?'));
?>


<div class="wrap">
    <div id="icon-tools" class="icon32"><br /></div>
    <h2>ALO EasyMail Newsletter</h2>

<?php
// All available languages
$languages = ALO_em_get_all_languages( false );

// For Tabs
$send_tab_active = $reports_tab_active = $templates_tab_active = "";
$sel_active_class = "nav-tab-active";
$active_tab = false;


/*******************************************************************************
 * Submit newsletter
 ******************************************************************************/

if(isset($_REQUEST['submit'])) {
	if ( !current_user_can('send_easymail_newsletters') ) 	wp_die(__('Cheatin&#8217; uh?'));
	check_admin_referer('alo-easymail_main');
	
    // prepare array with recipients' addresses
    $recipients = array();

    // prepare for error
    $error = "";
    
    // Requested langs
    $to_langs = ( isset($_POST['check_lang']) ) ? $_POST['check_lang'] : false;

    // Retrieve post info for TAG
	$pID = ( isset($_POST['select_post']) && (int)$_POST['select_post']) ? $_POST['select_post'] : false;
	if ($pID) $obj_post = get_post($pID);
    
   	// If any add NO-REGISTERED E-MAILS
    if ( isset($_POST['emails_add']) && trim($_POST['emails_add']) != "" ) {
        //$wrong_add_email = "";  // show them in error div
        $non_reg_emails = explode(",", $_POST['emails_add']);
        foreach ($non_reg_emails as $non_reg_email) {
            $trim_non_reg_email = trim($non_reg_email);
            $recipients[$trim_non_reg_email]['email'] = $trim_non_reg_email; // no check, add
            $recipients[$trim_non_reg_email]['name'] = "";
            $recipients[$trim_non_reg_email]['firstname'] = "";
        }
    }
    
    // If request add all SUBSCRIBERS
    if ( isset($_POST['all_subscribers']) && $_POST['all_subscribers'] == 'checked') {
        $subs = ALO_em_get_recipients_subscribers();
        foreach ($subs as $sub) {
        	// do not add the subscribers with not required langs 
        	$search_lang = ( !empty($sub->lang) ) ? $sub->lang : "UNKNOWN"; // if subscriber has not specified lang
        	if ( $to_langs && array_search($search_lang, $to_langs)=== false ) continue;
            $recipients[$sub->email]['email'] = $sub->email;
            $recipients[$sub->email]['name'] = $sub->name;
            $recipients[$sub->email]['firstname'] = $sub->name;
            $recipients[$sub->email]['unikey'] = $sub->unikey; 
            $recipients[$sub->email]['lang'] = $sub->lang; 
        }
    } else { // if not requested all subcribers, maybe requested only by selected lists?
		if ( isset($_POST['check_list']) && is_array ($_POST['check_list']) ) {
			$subs = ALO_em_get_recipients_subscribers( $_POST['check_list'] );
			if ( $subs) {
				foreach ( $subs as $sub ) {
					// do not add the subscribers with not required langs 
					$search_lang = ( !empty($sub->lang) ) ? $sub->lang : "UNKNOWN"; // if subscriber has not specified lang
					if ( $to_langs && array_search($search_lang, $to_langs)=== false ) continue;
		            $recipients[$sub->email]['email'] = $sub->email;
		            $recipients[$sub->email]['name'] = $sub->name;
		            $recipients[$sub->email]['firstname'] = $sub->name;
		            $recipients[$sub->email]['unikey'] = $sub->unikey; 
		            $recipients[$sub->email]['lang'] = $sub->lang; 
				}
			}
		}
    }
    
    // If request add all REGISTERED users
    if ( isset($_POST['all_regusers']) && $_POST['all_regusers'] == 'checked') {
        $reg_users = ALO_em_get_recipients_registered ();
        if ($reg_users) {
		    foreach ($reg_users as $reg_user) {
		    	// login name as default name if first/lastname are empty
	    	 	//$user_info = get_userdata( $reg_user->UID );
	    	 	//$user_loginname = $user_info->user_login;
	    	 	if ( get_user_meta($reg_user->UID, 'first_name', true) != "" ) {
	    	 	   	$reg_firstname =  ucfirst(get_user_meta($reg_user->UID, 'first_name', true));
	    	 	} else {
	    	 		$reg_firstname =  get_user_meta($reg_user->UID, 'nickname', true);
	    	 	}
	    	 	if ( get_user_meta($reg_user->UID, 'first_name', true) != "" || get_user_meta($reg_user->UID, 'last_name', true) != "" ) {
	    	 	   	$reg_name =  ucfirst(get_user_meta($reg_user->UID, 'first_name',true))." " .ucfirst(get_user_meta($reg_user->UID,'last_name',true));
	    	 	} else {
	    	 		$reg_name = get_user_meta($reg_user->UID, 'nickname', true);
	    	 	}	    	 	
		        $recipients[$reg_user->user_email]['email'] = $reg_user->user_email;
		        $recipients[$reg_user->user_email]['name'] = $reg_name; 
		        $recipients[$reg_user->user_email]['firstname'] = $reg_firstname; 
		        $recipients[$reg_user->user_email]['lang'] = $reg_user->lang;
		    }
		}
    }
    
    
    // Subject
    $subject = stripslashes($wpdb->escape($_POST['title']));
    
    // Main content
    $main_content = stripslashes($_POST['content']);
	
	// Check errors
	$error_on_submit = false;
	if ($subject == "" || $main_content == "") {
		$fbk_msg = "error";
		$error_on_submit = true;
    }
    if (count($recipients) < 1 ) {
        $fbk_msg = "norecipients";
        $error_on_submit = true;
    }
    
    // If no errors let's go!
    if ( $error_on_submit == false ) {
		
		// Save emails'list for next sending, if request
		if ( isset($_POST['ck_save_list']) ) update_option( 'ALO_em_list_user_'.$user_ID, trim($_POST['emails_add']) );
		
		// Tracking feature
		$tracking  = ( isset($_POST['ck_tracking']) && $_POST['ck_tracking'] != "" ) ? $_POST['ck_tracking'] : "";
	   
		// need a numeric index array
		$num_rec = array();
		$n =0;
		foreach($recipients as $rec) {
			$num_rec[$n]= $rec;
			$n ++;
		}
		
		// adjust content (post tags)
		$updated_content = $main_content;
	   
		$updated_content = str_replace("\n", "<br />", $updated_content);
		// trim <br> added when rendering html tables (thanks to gunu)
		$updated_content = str_replace( array("<br /><t", "<br/><t", "<br><t"), "<t", $updated_content);
		$updated_content = str_replace( array("<br /></t", "<br/></t", "<br></t"), "</t", $updated_content);
		
		// Add/update template
		if ( isset($_POST['ck_save_template']) ) {
			$and_tpl = "";
			if (isset($_POST['tpl_id']) && is_numeric($_POST['tpl_id']) ) {
			  	if ( ALO_em_update_template ( $_POST['tpl_id'], $user_ID, $subject, $main_content ) ) $and_tpl = "saved";
			} else {
				if ( ALO_em_add_new_template ( $user_ID, $subject, $main_content ) ) $and_tpl = "saved";
			}
		}
		
		/* 
		
		// TAG: [POST-TITLE]
		if ($pID) {
		    $updated_content = str_replace("[POST-TITLE]", "<a href='".get_permalink($obj_post->ID). "'>". get_the_title($obj_post->ID) ."</a>", $updated_content);      
		} else {
		    $updated_content = str_replace("[POST-TITLE]", "", $updated_content);
		}

		// TAG: [POST-CONTENT]
		if ($pID) {
		    $updated_content = str_replace("[POST-CONTENT]", $obj_post->post_content, $updated_content);
		} else {
		    $updated_content = str_replace("[POST-CONTENT]", "", $updated_content);
		}
		
		// TAG: [POST-EXCERPT] - if any
		if ($pID && !empty($obj_post->post_excerpt)) {
		    $updated_content = str_replace("[POST-EXCERPT]", $obj_post->post_excerpt, $updated_content);       
		} else {
		    $updated_content = str_replace("[POST-EXCERPT]", "", $updated_content);
		}
		
		// TAG: [SITE-LINK]
		$updated_content = str_replace("[SITE-LINK]", "<a href='".get_option ('siteurl')."'>".get_option('blogname')."</a>", $updated_content);       
		
		*/
		      
		//echo "<pre>";print_r($num_rec);echo "</pre>";exit;
		/*
		//---------
		// DEBUG
		//---------    
		echo "HEADERS: ".$headers."<br />";
		echo "SUBJECT: ".$subject."<br />";
		echo "CONTENT: ".$updated_content."<br />";
		echo "PLAIN CONTENT:<br /><pre>" . ALO_em_html2plain($updated_content) ."</pre><br />";
		foreach ($recipients as $rec) {
		    echo "<pre>";print_r ($rec);echo "</pre>";
		}
		// echo $wpdb->last_query;
		//echo "<pre>";print_r ($_REQUEST);echo "</pre>";
		*/
		
		// add the newsletter to db
		if ( ALO_em_add_new_batch ( $user_ID, $subject, $updated_content, serialize($num_rec), $tracking, $pID ) == true) {
			$fbk_msg = "success";
			$_REQUEST['tab'] = "reports"; // show report
		} else {
			$fbk_msg = "nosending";
		}	
	
	} // end if $error_on_submit == false
}



/*******************************************************************************
 * Submit template
 ******************************************************************************/
 
if(isset($_REQUEST['submit_tpl'])) {
    if ( !current_user_can('send_easymail_newsletters') ) 	wp_die(__('Cheatin&#8217; uh?'));
    check_admin_referer('alo-easymail_main');
    
    // Subject
    $subject = stripslashes($wpdb->escape($_POST['title']));
    
    // Main content
    $main_content = stripslashes($_POST['content']);

	// Check for errors
	$error_on_submit = false;
    if ($subject == "" || $main_content == "") {
       	$fbk_msg = "tpl_error";  
       	$error_on_submit = true;
    }
      
    // If no errors let's go!
    if ( $error_on_submit == false ) { 
    
	   	// UPDATE the template to db
		if ( isset($_POST['task']) && $_POST['task'] == "update_tpl" && isset($_POST['tpl_id']) && is_numeric($_POST['tpl_id']) ) {
		  	if ( ALO_em_update_template ( $_POST['tpl_id'], $user_ID, $subject, $main_content ) == true) {
				$fbk_msg = "tpl_saved";
			} else {
				$fbk_msg = "tpl_nosaved";
			}
		} else {
			// ADD the template to db
			if ( ALO_em_add_new_template ( $user_ID, $subject, $main_content ) == true) {
				$fbk_msg = "tpl_saved";
			} else {
				$fbk_msg = "tpl_nosaved";
			}
		}	
		unset($_POST);
		
	} // end if $error_on_submit == false
}


/**
 * Set Tabs
 */
if ( empty($active_tab) ) {
	if ( isset( $_REQUEST['tab']) ) {
		if ( $_REQUEST['tab'] == "reports") {
			$active_tab = "reports";
			$reports_tab_active = $sel_active_class;
		} else if ( $_REQUEST['tab'] == "templates") {
			$active_tab = "templates";
			$templates_tab_active = $sel_active_class;		
		} else { 
			$active_tab = "send";
			$send_tab_active = $sel_active_class;		
		}
	} else {
		$active_tab = "send";
		$send_tab_active = $sel_active_class;	
	} 
}


// Reset base url (cut message vars...)
$clean_url = remove_query_arg( array('tab', 'message', 'task', 'id') );
?>

	<h2 style="border-bottom:1px solid #CCCCCC">
	<a href="<?php echo add_query_arg( 'tab', 'send', $clean_url) ?>" class="nav-tab <?php echo $send_tab_active ?>">&raquo; <?php _e("Send newsletter", "alo-easymail") ?></a>
	<a href="<?php echo add_query_arg( 'tab', 'reports', $clean_url ) ?>" class="nav-tab <?php echo $reports_tab_active ?>">&raquo; <?php _e("Reports", "alo-easymail") ?></a>
	<a href="<?php echo add_query_arg( 'tab', 'templates', $clean_url ) ?>" class="nav-tab <?php echo $templates_tab_active ?>">&raquo; <?php _e("Templates", "alo-easymail") ?></a>
	</h2>

    <div id="dashboard-widgets-wrap">


    
<?php 
/**
 * --- start MAIN --------------------------------------------------------------
 */
?>

<?php
// Possible levelIf can manage all newsletters
$can_edit_all	= ( current_user_can('manage_easymail_newsletters') && current_user_can('manage_easymail_subscribers') ) ? true: false;
$can_edit_own	= ( current_user_can('manage_easymail_newsletters') ) ? true: false;
$can_see_own	= ( current_user_can('send_easymail_newsletters') ) ? true: false;

// $can_see_all 	= ( current_user_can('manage_easymail_newsletters') ) ? true: false; //($user_level >= 8)?




/**
 * Other Requested actions
 */
if ( isset( $_REQUEST['task']) ) {
	// Cancel one of own newsletter in sending queue
	if ( $_REQUEST['task'] == "del_send" && isset( $_REQUEST['id'])) {
		$where_user = ( $can_edit_all )? "" : " AND user = %d ";
		$check_id = $wpdb->query( $wpdb->prepare( "SELECT ID FROM {$wpdb->prefix}easymail_sendings WHERE ID = %d {$where_user}", $_REQUEST['id'], $user_ID ) );
		if ($check_id) {
			if ( ALO_em_delete_newsletter ( $_REQUEST['id'] ) ) {		
				echo '<div id="message" class="updated fade"><p><strong>'.__("Newsletter successfully deleted", "alo-easymail").'</strong></p></div>';
			} else {
				echo '<div id="message" class="error"><p><strong>'.__("Impossible to delete the selected newsletter", "alo-easymail").'</strong></p></div>';		
			}
		
		}
	}
	
	// Delete a template
	if ( $_REQUEST['task'] == "del_tpl" && isset( $_REQUEST['id'])) {
		$where_user = ( $can_edit_all )? "" : " AND user = %d ";
		$check_id = $wpdb->query( $wpdb->prepare( "SELECT ID FROM {$wpdb->prefix}easymail_sendings WHERE ID = %d {$where_user} AND sent = 9", $_REQUEST['id'], $user_ID ) );
		if ($check_id) {
			if ( ALO_em_delete_newsletter ( $_REQUEST['id'] ) ) {		
				echo '<div id="message" class="updated fade"><p><strong>'.__("Template successfully deleted", "alo-easymail").'</strong></p></div>';
			} else {
				echo '<div id="message" class="error"><p><strong>'.__("Impossible to delete the selected template", "alo-easymail").'</strong></p></div>';		
			}
		
		}
	}

	// Send a newsletter from a template / Modify a template
	if ( ($_REQUEST['task'] == "send_tpl" || $_REQUEST['task'] == "mod_tpl") && isset( $_REQUEST['id'])) {
		$where_user = ( $can_edit_all )? "" : " AND user = %d ";
		$from_template = $wpdb->get_row( $wpdb->prepare( "SELECT ID, subject, content, sent FROM {$wpdb->prefix}easymail_sendings WHERE ID = %d {$where_user} AND sent = 9", $_REQUEST['id'], $user_ID ) );
	}	
}


/**
 * If feedback message 
 */
if ( !empty( $fbk_msg )) :
	switch( $fbk_msg ) {
		case 'success':		// ok, sending scheduled
			$fbk_msg = '<div id="message" class="updated fade">';
			$fbk_msg .= '<p><img src="'.ALO_EM_PLUGIN_URL.'/images/16-email-add.png" /> ';
			$fbk_msg .= '<strong>'.__("New sending added with success!", "alo-easymail").'</strong></p>';
			if ( isset( $and_tpl ) ) $fbk_msg .= '<p>'.__("Template saved", "alo-easymail").'.</p>';
			$fbk_msg .= "</div>";
			break;
		case 'error':		// error in inputs
			$fbk_msg = '<div id="message" class="error">';
			$fbk_msg .= '<p><img src="'.ALO_EM_PLUGIN_URL.'/images/no.png" /> ';
			$fbk_msg .= '<strong>'.__("Inputs are incompled or wrong. Please check and try again.", "alo-easymail").'</strong></p>';
			if ( isset( $and_tpl ) ) $fbk_msg .= '<p>'.__("Template saved", "alo-easymail").'.</p>';
			$fbk_msg .= "</div>";
			break;
		case 'norecipients': // no recipients selected
			$fbk_msg = '<div id="message" class="error">';
			$fbk_msg .= '<p><img src="'.ALO_EM_PLUGIN_URL.'/images/no.png" /> ';
			$fbk_msg .= '<strong>'.__("No recipients selected.", "alo-easymail").'</strong></p>';
			$fbk_msg .= "</div>";
			break;
		case 'nosending':	// error on sending
			$fbk_msg = '<div id="message" class="error">';
			$fbk_msg .= '<p><img src="'.ALO_EM_PLUGIN_URL.'/images/no.png" /> ';
			$fbk_msg .= '<strong>'.__("Impossible to send. Please try again.", "alo-easymail").'</strong></p>';
			$fbk_msg .= "</div>";
			break;

		case 'tpl_saved':	// template saved
			$fbk_msg = '<div id="message" class="updated fade">';
			$fbk_msg .= '<p><img src="'.ALO_EM_PLUGIN_URL.'/images/16-email-add.png" /> ';
			$fbk_msg .= '<strong>'.__("Template saved", "alo-easymail").'</strong></p>';
			$fbk_msg .= "</div>";
			break;			
		case 'tpl_nosaved':	// error on template saving
			$fbk_msg = '<div id="message" class="error">';
			$fbk_msg .= '<p><img src="'.ALO_EM_PLUGIN_URL.'/images/no.png" /> ';
			$fbk_msg .= '<strong>'.__("Impossible to save the template. Please try again.", "alo-easymail").'</strong></p>';
			$fbk_msg .= "</div>";
			break;		
		case 'tpl_error':	// error in template inputs
			$fbk_msg = '<div id="message" class="error">';
			$fbk_msg .= '<p><img src="'.ALO_EM_PLUGIN_URL.'/images/no.png" /> ';
			$fbk_msg .= '<strong>'.__("Inputs are incompled or wrong. Please check and try again.", "alo-easymail").'</strong></p>';
			$fbk_msg .= "</div>";
			break;				
		default:
			$fbk_msg = "";
	}
	echo $fbk_msg;
endif; // end if ( isset( $_REQUEST['message']))


/*--------------------------------------
	REPORTS Tab
--------------------------------------*/
if ( $active_tab == "reports" ) :
/*------------------------------------*/	


$linkthick = wp_nonce_url( ALO_EM_PLUGIN_URL . '/alo-easymail_report.php?', 'alo-easymail_main');
?>

<script language="javascript">
function openReport(id){
    tb_show( '<?php _e("Newsletter report", "alo-easymail") ?>',"<?php echo $linkthick ?>&id="+id+"&lang=<?php echo ALO_em_get_language ()?>&TB_iframe=true&height=430&width=600",false);
    return false;
}
</script>

<?php
/**
 * Search for newsletters TO SEND in queue
 */
$news_on_queue =  $wpdb->get_results("SELECT * FROM {$wpdb->prefix}easymail_sendings WHERE sent = 0 ORDER BY ID ASC");
//echo "<pre>";print_r($news_on_queue);echo "</pre>";
if (count($news_on_queue)) { ?>
	<table class="widefat" style='margin-top:10px'>
		<caption style="margin:10px;"><strong><?php _e("Newsletters scheduled for sending", "alo-easymail") ?></strong> (<a href="<?php echo $_SERVER['SCRIPT_NAME']; ?>?page=alo-easymail/alo-easymail_main.php&amp;tab=reports"><?php _e("refresh", "alo-easymail") ?>&raquo;</a>)</caption>
		<thead><tr>
			<th scope="col" style="width:5%"><div style="text-align: center;"><?php _e("Queue", "alo-easymail") ?></div></th>
			<th scope="col" style="width:15%"><?php _e("Scheduled by", "alo-easymail") ?></th>
			<th scope="col" ><?php _e("Added on", "alo-easymail") ?></th>
			<th scope="col"><?php _e("Subject", "alo-easymail") ?></th>
			<th scope="col" style="width:10%"><?php _e("Progress", "alo-easymail") ?></th>			
			<th scope="col" style="width:15%"><?php _e("Action", "alo-easymail") ?></th>
		</tr></thead>
		<tbody id="the-list">
	<?php
	$class = 'alternate';
	$row_count = 0;
	foreach ($news_on_queue as $q) {
		$class = ('alternate' == $class) ? '' : 'alternate';
		$class = ($row_count == 0) ? 'updated': $class;
		echo "<tr id='que-{$q->ID}' class='$class'>\n"; ?>
		<th scope="row" style="text-align: center;">
		    <?php if ($row_count == 0) {
		    	echo '<img src="'.ALO_EM_PLUGIN_URL.'/images/16-email-forward.png" title="'.__("now sending", "alo-easymail").'" alt="" />';
			   } else {
			    echo $row_count; 
			   }
			   ?>
        </th>
		<td><?php 
			if ($q->user == $user_ID) {
				echo "<strong>".__("you", "alo-easymail")."</strong>";
			} else {
				if ( $can_edit_all ) {
					echo get_user_meta($q->user, 'nickname', true);
				} else {
					echo"<em>".__("another user", "alo-easymail")."</em>";
				}
			}
		?></td>
		<td><?php echo date("d/m/Y", strtotime($q->start_at))." h.".date("H:i", strtotime($q->start_at)) ?></td>
		<td><?php echo ($q->user == $user_ID || $can_edit_all )? stripslashes ( ALO_em___( $q->subject ) ) : ""; ?></td>
		<td><?php 
			$q_recipients = unserialize( $q->recipients );
			$q_tot = count($q_recipients);
			$n_sent = 0;
			foreach ($q_recipients as $qr) {
		   		if ( isset($qr['result']) ) $n_sent ++;
		   	}
			echo round($n_sent*100/ $q_tot ) . " %" ;
		?></td>
		<td>
			<?php if ( ( $q->user == $user_ID && $can_edit_own ) || $can_edit_all ) {
				echo "<a href='edit.php?page=alo-easymail/alo-easymail_main.php&amp;tab=reports&amp;task=del_send&amp;id=".$q->ID."' title='".__("Cancel", "alo-easymail")."' ";
				echo " onclick=\"return confirm('".__("Do you really want to stop and cancel this sending?", "alo-easymail")."');\">";
				echo __("Cancel", "alo-easymail"). "</a>";
			} 
		?></td>
		<?php
		echo "</tr>";
		$row_count++;
	}
	echo "</tbody></table>";
	echo "<p>&nbsp;</p>";
}
?>

<?php
/**
 * Search for newsletters ALREADY sent by the USER (of by ALL users, if admin)
 */
$where_user = ( $can_edit_all )? "" : "AND user=".$user_ID;
$news_done =  $wpdb->get_results("SELECT * FROM {$wpdb->prefix}easymail_sendings WHERE sent = 1 {$where_user} ORDER BY ID DESC");
//echo "<pre>";print_r($news_on_queue);echo "</pre>";
if (count($news_done)) { ?>
	<table class="widefat" style='margin-top:10px'>
		<caption style="margin:10px;"><strong><?php echo ( $can_edit_all ==false)? __("Newsletters sent BY YOU", "alo-easymail") : __("Newsletters sent BY ALL USERS", "alo-easymail") ?></strong></caption>
		<thead><tr>
			<th scope="col" style="width:5%"><div style="text-align: center;">#</div></th>
			<?php if ( $can_edit_all ) echo '<th scope="col" style="width:15%">'.__("Scheduled by", "alo-easymail").'</th>'; ?>
			<th scope="col"><?php _e("Added on", "alo-easymail") ?></th>
			<th scope="col"><?php _e("Completed", "alo-easymail") ?></th>
			<th scope="col"><?php _e("Subject", "alo-easymail") ?></th>
			<th scope="col" style="width:15%"><?php _e("Report", "alo-easymail") ?></th>
		</tr></thead>
		<tbody id="the-list">
	<?php
	$class = 'alternate';
	$row_count = 0;
	foreach ($news_done as $q) {
		$class = ('alternate' == $class) ? '' : 'alternate';
		echo "<tr id='news-done-{$q->ID}' class='$class'>\n"; ?>
		<th scope="row" style="text-align: center;">
		    <?php echo count($news_done) - $row_count;?>
        </th>
		<?php if ( $can_edit_all ) {
			echo "<td>". ( ($q->user == $user_ID)? "<strong>".__("you", "alo-easymail")."</strong>": get_user_meta($q->user, 'nickname', true) ). "</td>";
		} ?>
		<td><?php echo date("d/m/Y", strtotime($q->start_at))." h.".date("H:i", strtotime($q->start_at)) ?></td>
		<td><?php echo date("d/m/Y", strtotime($q->last_at))." h.".date("H:i", strtotime($q->last_at)) ?></td>
		<td><?php echo ($q->user == $user_ID || $can_edit_all )? stripslashes ( ALO_em___( $q->subject ) ) : "" ?></td>
		<td>
			<?php if ( ($q->user == $user_ID && $can_edit_own ) || $can_edit_all ) {
				echo "<a href='edit.php?page=alo-easymail/alo-easymail_main.php&amp;tab=reports&amp;task=del_send&amp;id=".$q->ID."' title='".__("Delete", "alo-easymail")."' ";
				echo " onclick=\"return confirm('".__("Do you really want to delete the report of this newsletter?", "alo-easymail")."');\">";
				echo __("Delete", "alo-easymail"). "</a> - ";
				echo "<a href='' title='".__("View", "alo-easymail")."' ";
				echo " onclick=\"return openReport({$q->ID})\">";
				echo __("View", "alo-easymail"). "</a>";
			} 
		?></td>
		<?php
		echo "</tr>";
		$row_count++;
	}
	echo "</tbody></table>";
	echo "<p>&nbsp;</p>";
}
?>

<?php


/*--------------------------------------
	SEND Tab
--------------------------------------*/
endif; // end reports tab
if ( $active_tab == "send" ) :
/*------------------------------------*/	

?>

<script type="text/javascript">
function openPopup(){
    var popup = window.open('','popup','toolbar=no,location=yes,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=740,height=300,left=0,top=0');
    post.submit();
    return false;
}

function checkEmailList () {
	var emaillist = document.getElementById("emails_add").value;
	// cut last comma, if any
	if ( emaillist.charAt(emaillist.length -1) == "," ) { 
	    document.getElementById("emails_add").value = emaillist.slice(0, -1);
	    emaillist = emaillist.slice(0, -1);
	}
	var wrong_list = "";
	if (emaillist) {
		document.getElementById("response-emails-add").innerHTML = "<?php _e("Checking...", "alo-easymail") ?>";
		// each addresses
		var lines = emaillist.split(",");
		for (x=0; x < lines.length; x++){
			var regmail = /^[_a-z0-9+-]+(\.[_a-z0-9+-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)+$/;
			if (!regmail.test(lines[x]))	{
				wrong_list += lines[x] + ", ";
			}
		}
	}
	if (wrong_list != "") {
		wrong_list = wrong_list.slice(0, -2);
		document.getElementById("response-emails-add").innerHTML = "<p style='color:#f00;'><em><?php _e("Warning! Some addresses seem to be wrong", "alo-easymail") ?>:</em><br />" + wrong_list + ".</p>";
	} else {
		document.getElementById("response-emails-add").innerHTML = "";
	}
    return false;
}

function toggle_visibility(id) {
    var e = document.getElementById(id);
    if(e.style.display == 'block') {
      e.style.display = 'none';
    } else {
      e.style.display = 'block';
     }
}
</script>

<form name="post" action="" method="post" id="post" name="post" >

<h3><?php _e("Recipients", "alo-easymail") ?></h3>

<table class="form-table">
<tbody>

<tr valign="top">
<th scope="row"><?php _e("Choose the kind of recipients", "alo-easymail") ?>:</th>
<td>

<div style="float:left;margin-right:50px"><strong><?php _e("Main groups", "alo-easymail"); ?>:</strong><ul>
	<?php $checked = ( isset($_POST['all_subscribers']) ) ? ' checked="checked" ' : ''; ?>
	<li><input type="checkbox" name="all_subscribers" id="all_subscribers" value="checked" <?php echo $checked ?> /><label for="all_subscribers"><?php echo __("All subscribers", "alo-easymail"). " (". count( ALO_em_get_recipients_subscribers() ) .")"; ?></label></li>
	<?php $checked = ( isset($_POST['all_regusers']) ) ? ' checked="checked" ' : ''; ?>
	<li><input type="checkbox" name="all_regusers" id="all_regusers" value="checked" <?php echo $checked ?> /><label for="all_regusers"><?php echo __("All registered users", "alo-easymail"). " (". count ( ALO_em_get_recipients_registered () ) .")"; ?></label></li>	
</ul></div>

<?php // mailing lists
$mailinglists = ALO_em_get_mailinglists( 'admin,public' );
if ($mailinglists) { ?>
	<div style="float:left;margin-right:50px"><strong><?php _e("Mailing Lists", "alo-easymail"); ?>:</strong><ul>
	<?php	
	foreach ( $mailinglists as $list => $val) { 
		if ( $val['available'] == "deleted" || $val['available'] == "hidden" ) continue; 
			$checked = ( isset($_POST['check_list']) && in_array($list, $_POST['check_list']) ) ? ' checked="checked" ' : '';
			?>
			<li><input type="checkbox" name="check_list[]" id="list_<?php echo $list ?>" value="<?php echo $list ?>" <?php echo $checked ?>/><label for="list_<?php echo $list ?>"><?php echo ALO_em_translate_multilangs_array ( ALO_em_get_language(), $val['name'], true ) . " (".  count ( ALO_em_get_recipients_subscribers( $list ) ).")"; ?></label></li>
	<?php } ?>
	</ul></div>
<?php } // end if ?>

<?php // Language filter
if ($languages) { ?>
	<div style="float:left;margin-right:50px"><strong><?php _e("Filter subscribers according to languages", "alo-easymail"); ?>:</strong>
	<?php echo ALO_em_help_tooltip( __("This filter works only for subscribers (all/lists), not for registered users", "alo-easymail") ) ?>
	<ul>
	<?php $checked = ( isset($_POST['check_lang_all']) || !isset($_POST['submit']) ) ? ' checked="checked" ' : ''; ?>
	<?php	
	foreach ( $languages as $index => $lang) {  
			$checked = ( (isset($_POST['check_lang']) && in_array($lang, $_POST['check_lang'])) || !isset($_POST['submit']) ) ? ' checked="checked" ' : '';
			$tot_sub_x_lang = ALO_em_count_subscribers_by_lang( $lang, true );
			?>
			<li><input type="checkbox" name="check_lang[]" id="check_lang_<?php echo $lang ?>" value="<?php echo $lang ?>" <?php echo $checked ?>/><label for="check_lang_<?php echo $lang ?>"> <?php echo esc_html ( ALO_em_get_lang_name ( $lang ) ) . " (". $tot_sub_x_lang .")"; ?></label></li>
	<?php } ?>
	<?php $checked = ( (isset($_POST['check_lang']) && in_array( "UNKNOWN", $_POST['check_lang'])) || !isset($_POST['submit']) ) ? ' checked="checked" ' : ''; ?>
	<li><input type="checkbox" name="check_lang[]" id="check_lang_unknown" value="UNKNOWN" <?php echo $checked ?> /><label for="check_lang_unknown"> <?php _e("Not specified / others", "alo-easymail"); ?> (<?php echo ALO_em_count_subscribers_by_lang(false, true) ?>)</label> <?php echo ALO_em_help_tooltip( __("That includes subscribers who did not choose any language or specified a language no longer available", "alo-easymail").". ". __("These subscribers will receive the newsletter in the main language of the site", "alo-easymail") ) ?></li>	
	</ul></div>
<?php } // end if ?>


<div style="float:left;margin-top:10px;margin-right:50px;width:600px">
	<span class="description"><?php _e("Between brackets the number of recipients belonging to each group or list", "alo-easymail") ?>.
	<?php _e("Do not worry about recipients belonging to more than one group or list: the plugin avoids sending twice to the same recipient", "alo-easymail") ?>.</span>
</div>
</td>
</tr>

<tr valign="top">
<th scope="row"><?php _e("To send to other people insert a list of e-mail addresses separated by comma (,)", "alo-easymail") ?>:</th>
<?php $list_emails = ( isset($_POST['emails_add']) ) ? $_POST['emails_add'] : get_option ( 'ALO_em_list_user_'.$user_ID, "" ); ?>
<td><textarea id="emails_add" value="" name="emails_add" rows="3" cols="70" onblur="checkEmailList()"><?php echo $list_emails; ?></textarea>
<div id="response-emails-add"></div></td>
</tr>

<tr valign="top">
<th scope="row"><label for="ck_save_list"><?php _e("Save the list of email addresses for next sending", "alo-easymail") ?></label></th>
<td valign="middle"><input type="checkbox" name="ck_save_list" id="ck_save_list" value="checked" checked="checked" /></td>
</tr>

</tbody>
</table>

<h3 style='margin-top:20px;'><?php _e("Subject and text of the e-mail", "alo-easymail") ?></h3>

<table class="form-table">
<tbody>

<tr valign="top">
<th scope="row"><?php _e("Choose to send a simple generic e-mail or one about a specific post", "alo-easymail") ?>
</th>

<td>
<?php
$n_last_posts = (get_option('ALO_em_lastposts'))? get_option('ALO_em_lastposts'): 10;
$args = array(
	'numberposts' => $n_last_posts,
	'order' => 'DESC',
	'orderby' => 'date'
	); 

$get_posts = get_posts($args);
$tot_posts = count($get_posts);

echo '<select name="select_post" id="select_post" >';
echo '<option value="0">['.__("generic e-mail: no post selected", "alo-easymail").']</option>';
if ($tot_posts) { 
    foreach($get_posts as $post) :
        $select_post_selected = ( isset($_POST['select_post']) && $post->ID == $_POST['select_post'] ) ? 'selected="selected"': '';
        echo '<option value="'.$post->ID.'" '. $select_post_selected .'>&middot; '. get_the_title($post->ID).' </option>';
    endforeach;
}
echo '</select>'; 
?>
<br /><span class="description"><?php _e("If you choose a post you can use the post tags (see below) in the main content", "alo-easymail") ?>.</span>
</td>
</tr>

<tr valign="top">
<th scope="row"><strong><?php _e("Subject", "alo-easymail") ?></strong>:</th>
<?php 
$subj = ""; 
if ( !empty($from_template) ) {
	$subj = htmlspecialchars ( stripslashes ( $from_template->subject ) );
} else {
	$subj = ( isset($_POST['title'])? htmlspecialchars ( stripslashes ( $_POST['title'] ) ) : "");
}
?>
<td>
<div class="postbox" id="titlediv">
<div class="inside">
<input type="text" size="70" name="title" id="title" value="<?php echo $subj ?>" maxlength="150" />
</div></div>
</td>
</tr>


<tr valign="top">
<th scope="row"><strong><?php _e("Main body", "alo-easymail") ?></strong> <span class="description"><br />(<?php _e("you can use the tags listed below", "alo-easymail") ?>)</span>:</th>
<td> <?php // open td ?>
<div id="poststuff">
<div id="<?php echo user_can_richedit() ? 'postdivrich' : 'postdiv'; ?>" class="postarea">
<?php if ( !empty($from_template) ) {
	$main_content = $from_template->content;
} else {
	$main_content = ( isset($_POST['content'])? $_POST['content'] : "");
}
the_editor ($main_content); ?>
</div></div>

<p><a href="#" onclick="toggle_visibility('tags-table'); return false" class="button"><?php _e("View tags", "alo-easymail") ?></a></p>
<div id="tags-table" style="display: none;">
<?php ALO_em_tags_table(); ?>
</div>

</td> <?php // close td ?>
</tr>

<tr valign="top">
<th scope="row"><label for="ck_save_template">
<?php 
if ( !empty($from_template) ) { 
	_e("Update the template (subject and main body)", "alo-easymail");
} else {
	_e("Save the subject and the main body as template", "alo-easymail");
}
?></label></th>
<td valign="middle"><input type="checkbox" name="ck_save_template" id="ck_save_template" value="checked" />
<span class="description"><?php echo __("You can manage templates with the button at the top of the page", "alo-easymail") ?>.</span>
<?php
if ( !empty($from_template) ) { 
	echo '<input type="hidden" name="tpl_id" value="'. $from_template->ID . '">';
} 
?>
</td></tr>

</tbody>
</table>

<h3 style='margin-top:20px;'><?php _e("Send", "alo-easymail") ?></h3>

<table class="form-table">
<tbody>
<tr valign="top">
<th scope="row"><label for="ck_tracking"><?php _e("Track when viewed", "alo-easymail") ?></label></th>
<td><input type="checkbox" name="ck_tracking" id="ck_tracking" value="ALO_EM" checked="checked" />
<span class="description"><?php echo __("The plugin tries to count how many recipients open the newsletter", "alo-easymail").". (". __("This feedback depends on recipients&#39; e-mail client, so the result is approximate and probably undersized", "alo-easymail").")." ?></span>
</td>
</tr>
<tr valign="top">
<th scope="row" style="text-align:right">
<?php // Submit ?>
    <span class="submit">
    <?php wp_nonce_field('alo-easymail_main'); ?>
    <input type="submit" name="submit" id="submit" value="<?php  _e('Add to sending queue', 'alo-easymail'); ?>" class="button-primary" onclick="this.value='<?php _e("PLEASE WAIT: sending...", "alo-easymail") ?>';"/>
    </span>   
</th>
<td valign="middle"><strong><?php _e("Click ONCE and wait for the sending to be over", "alo-easymail") ?>.</strong></td>
</tr>
</tbody>
</table>

</form>

<?php
/*--------------------------------------
	TEMPLATES Tab
--------------------------------------*/
endif; // end send tab
if ( $active_tab == "templates" ) :
/*------------------------------------*/	

// If upgraded an old version, transform old user template in a new template
if ( get_option ( 'ALO_em_template_user_'.$user_ID ) ) {
	ALO_em_add_new_template ( $user_ID, __('Your template', 'alo-easymail'), get_option ( 'ALO_em_template_user_'.$user_ID ) );
	delete_option ('ALO_em_template_user_'.$user_ID); // now useless, delete it
} else { // standard tpl
	if ( ALO_em_how_user_templates($user_ID) == 0 ) {
		ALO_em_add_new_template ( $user_ID, __('Template example (edit me)', 'alo-easymail') , get_option ( 'ALO_em_template' ) );
	}
}
?>

<script type="text/javascript">
	function toggle_visibility(id) {
		var e = document.getElementById(id);
		if(e.style.display == 'block') {
		  e.style.display = 'none';
		} else {
		  e.style.display = 'block';
		 }
	}
</script>

<?php

/**
 * Search for user's TEMPLATES
 */
$templates =  $wpdb->get_results("SELECT ID, start_at, last_at, user, subject, content, sent FROM {$wpdb->prefix}easymail_sendings WHERE sent = 9 AND user={$user_ID} ORDER BY last_at DESC");
//echo "<pre>";print_r($templates);echo "</pre>";
if (count($templates)) { ?>
	<table class="widefat" style='margin-top:10px'>
		<caption style="margin:10px;"><strong><?php _e("Newsletter templates", "alo-easymail") ?></strong></caption>
		<thead><tr>
			<th scope="col"><?php _e("Last modified on", "alo-easymail") ?></th>
			<th scope="col"><?php _e("Created on", "alo-easymail") ?></th>
			<th scope="col"><?php _e("Subject", "alo-easymail") ?></th>
			<th scope="col"><?php _e("Action", "alo-easymail") ?></th>
		</tr></thead>
		<tbody id="the-list">
	<?php
	$class = 'alternate';
	$row_count = 0;
	foreach ($templates as $t) {
		$class = ('alternate' == $class) ? '' : 'alternate';
		echo "<tr id='news-done-{$t->ID}' class='$class'>\n"; ?>
		<td><?php echo date("d/m/Y", strtotime($t->last_at))." h.".date("H:i", strtotime($t->last_at)) ?></td>
		<td><?php echo date("d/m/Y", strtotime($t->start_at))." h.".date("H:i", strtotime($t->start_at)) ?></td>		
		<td style="width:40%"><?php echo ($t->user == $user_ID )? stripslashes ( ALO_em___( $t->subject ) ) /*stripslashes ( $t->subject )*/ : "" ?></td>
		<td>
			<?php if ( $t->user == $user_ID && $can_edit_own ) {
				echo "<a href='edit.php?page=alo-easymail/alo-easymail_main.php&amp;tab=templates&amp;task=del_tpl&amp;id=".$t->ID."' title='".__("Delete", "alo-easymail")."' ";
				echo " onclick=\"return confirm('".__("Do you really want to delete this template?", "alo-easymail")."');\">";
				echo __("Delete", "alo-easymail"). "</a> - ";
				echo "<a href='edit.php?page=alo-easymail/alo-easymail_main.php&amp;tab=templates&amp;task=mod_tpl&amp;id=".$t->ID."'  title='". __("Edit", "alo-easymail") ."' >". __("Edit", "alo-easymail"). "</a> - ";
				echo "<a href='edit.php?page=alo-easymail/alo-easymail_main.php&amp;tab=send&amp;task=send_tpl&amp;id=".$t->ID."' title='". __("Send", "alo-easymail") ."' >". __("Send", "alo-easymail"). "</a>";
			} 
		?></td>
		<?php
		echo "</tr>";
		$row_count++;
	}
	echo "</tbody></table>";
	echo "<p>&nbsp;</p>";
} else {
	echo "<p>". __("There are no templates yet", "alo-easymail") .".</p>";
}
?>

<h3>
<?php
if ( !empty($from_template) ) { 
	_e("Update template", "alo-easymail");
} else {
	_e("New template", "alo-easymail");
}
?>
</h3>

<form name="post" action="" method="post" id="post" name="post" >

<table class="form-table">
<tbody>

<tr valign="top">
<th scope="row"><strong><?php _e("Subject", "alo-easymail") ?></strong>:</th>
<?php 
$subj = "";
if ( !empty($from_template) ) {
	$subj = htmlspecialchars ( stripslashes ( $from_template->subject ) );
} else if ( isset($_POST['title'])) {
	$subj = htmlspecialchars ( stripslashes ( $_POST['title'] ) );
}
?>
<td>
<div class="postbox" id="titlediv">
<div class="inside">
<input type="text" size="70" name="title" id="title" value="<?php echo $subj ?>" maxlength="150" />
</div></div>

</td>
</tr>


<tr valign="top">
<th scope="row"><strong><?php _e("Main body", "alo-easymail") ?></strong> <span class="description"><br />(<?php _e("you can use the tags listed below", "alo-easymail") ?>)</span>:</th>
<td> <?php // open td ?>
<div id="poststuff">
<div id="<?php echo user_can_richedit() ? 'postdivrich' : 'postdiv'; ?>" class="postarea">
<?php 
$main_content = "";
if ( !empty($from_template) ) {
	$main_content = $from_template->content;
} else if ( isset($_POST['content'])) {
	$main_content = $_POST['content'];
}
the_editor ($main_content); ?>
</div></div>

<p><a href="#" onclick="toggle_visibility('tags-table'); return false" class="button"><?php _e("View tags", "alo-easymail") ?></a></p>
<div id="tags-table" style="display: none;">
<?php ALO_em_tags_table(); ?>
</div>

<tr valign="top">
<th scope="row"> 
</th>
<td>
<?php // Submit ?>
    <span class="submit">
    <?php wp_nonce_field('alo-easymail_main'); ?>
    <input type="submit" name="submit_tpl" id="submit_tpl" value="<?php  _e('Save', 'alo-easymail'); ?>" class="button-primary" onclick="this.value='<?php _e("PLEASE WAIT: saving...", "alo-easymail") ?>';"/>
    </span>  
</td>
</tr>

</tbody>
</table>

<?php
if ( !empty($from_template) ) { 
	echo '<input type="hidden" name="task" value="update_tpl">';
	echo '<input type="hidden" name="tpl_id" value="'. $from_template->ID . '">';
} 
?>
<input type="hidden" name="tab" value="templates">

</form>

<?php
/*------------------------------------*/
endif; // end templates tab
/*------------------------------------*/
?>

<p></p>
<p><?php echo ALO_EM_FOOTER; ?></p>


<?php
/**
 * --- end MAIN ----------------------------------------------------------------
 */
?>

        </div>	
        
        
        <div class="clear">
        </div>
    </div>
</div><!-- wrap -->	
