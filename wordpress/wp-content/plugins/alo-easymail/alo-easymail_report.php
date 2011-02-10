<?php
include('../../../wp-blog-header.php');
//require_once('alo-easymail-widget.php'); // added GAL
auth_redirect();
if ( !current_user_can('send_easymail_newsletters') && !current_user_can('manage_easymail_newsletters') ) 	wp_die(__('Cheatin&#8217; uh?'));

//print_r ($_REQUEST); // DEBUG

if($wp_version >= '2.6.5') check_admin_referer('alo-easymail_main');


if (isset($_REQUEST['id']) && (int)$_REQUEST['id']) {        
    // ID of newsletter (to make the report)
    $id = $_REQUEST['id'];
    
    // Lang
    $lang = ( isset($_REQUEST['lang'])) ? $_REQUEST['lang'] : false;
    
    // If admin he can see
	$can_see_all = ( current_user_can('manage_easymail_newsletters') && current_user_can('manage_easymail_subscribers') ) ? true: false;//($user_level >= 8)? true: false;
    
    $where_user = ($can_see_all)? "" : " AND user = %d ";
	$newsletter = $wpdb->get_row( $wpdb->prepare( "SELECT * FROM {$wpdb->prefix}easymail_sendings WHERE sent=1 AND ID = %d {$where_user}", $id, $user_ID ) );
	
	if (!$newsletter) {
		die("The requested page doesn't exists.");
	} else {
		?>
		
		<style type="text/css">
			#tabs-1 {padding:1px 12px;border-bottom:1px dotted #aaa}
			dl {font-size:80%}
			dd {font-weight:bold;margin-bottm:5px}
	
			#tabs-2 {padding:10px 12px;}
			.tot {font-weight:bold;}
			.success {color:#0c6;font-weight:bold;}
			.error {color:#f00;font-weight:bold;}
			table {font-size:75%;width:550px;margin:0 auto;}
			td {padding:4px}
			td.center {text-align:center}
			#mailbody img { height: 5em; width: auto; display: block; }
		</style>
		
		<!--
		<script type="text/javascript">
			jQuery(function() {
				jQuery('#slider').tabs({ fxFade: true, fxSpeed: 'fast' });
			});
			function setcolor(fileid,color) {
				jQuery(fileid).css("background", color );
			};
		</script>
		-->
		
		<div id="slider" class="wrap">
			<!--
			<ul id="tabs">
				<li><a href="#tabs-1">...</a></li>
				<li><a href="#tabs-2">...</a></li>
			</ul>
			-->
			
			<!-- Newsletter's general details -->
			<div id="tabs-1">
				<dl>
					<dt><?php _e("Subject", "alo-easymail");  ?>:</dt>
					<dd><?php echo stripslashes ( ALO_em_translate_text ( $lang, $newsletter->subject ) ) ?></dd>
				</dl>
				<?php if ($newsletter->user != $user_ID) {
					echo "<dl><dt>".__("Scheduled by", "alo-easymail").":</dt>";
					echo "<dd>".get_user_meta($newsletter->user, 'nickname',true) . "</dd></dl>";
				} ?>
				<dl>
					<dt><?php _e("Added on", "alo-easymail") ?>:</dt>
					<dd><?php echo $newsletter->start_at ?></dd>
				</dl>
				<dl>
					<dt><?php _e("Completed", "alo-easymail") ?>:</dt>
					<dd><?php echo $newsletter->last_at ?></dd>
				</dl>		
				<dl>
					<dt><?php _e("Main body", "alo-easymail") ?> (<?php _e("without formatting", "alo-easymail") ?>):</dt>
					<dd style="font-weight:normal;font-size:90%" id="mailbody"><?php echo strip_tags( ALO_em_translate_text ( $lang, $newsletter->content), "<img>") ?></dd>
				</dl>	
			</div>
		
			<!-- Newsletter's recipients list -->
			<div id="tabs-2">
				<?php
				// List of recipients
				$recipients = unserialize( $newsletter->recipients );
				$tot_rec = count($recipients);
			
				$ok_rec = 0; // count success
				$ko_rec = 0; // count failed
				$vi_rec = 0; // count view
				foreach ($recipients as $recipient) {
	   				if ( $recipient['result'] >= 1) {
	   					$ok_rec ++;
	   					if ( ALO_em_recipient_is_tracked ( $recipient['email'], $id, 'V' ) ) {
	   						$vi_rec ++;
	   					}
	   				} else {
	   					$ko_rec ++;
	   				}
	   			}
				?>	
				
				<table style="width:100%;margin-top:10px">
					<thead><tr>
						<th scope="col"><?php _e("Total sendings", "alo-easymail") ?></th>
						<th scope="col"><?php _e("Sendings succesful", "alo-easymail") ?></th>
						<th scope="col"><?php _e("Sendings viewed", "alo-easymail"); echo " ". ALO_em_help_tooltip( __("The plugin tries to count how many recipients open the newsletter", "alo-easymail") . ". ". __("Available only for subscribers; for other e-mail addresses the value is always negative", "alo-easymail") ); ?></th>
						<th scope="col"><?php _e("Sendings failed", "alo-easymail") ?></th>
					</tr></thead>
				<tbody><tr>
					<td class="tot center" style="width:25%"><?php echo $tot_rec ?>
					<td class="success center" style="width:25%"><?php echo $ok_rec ?>
					<td class="success center" style="width:25%"><?php echo $vi_rec ?>
					<td class="error center" style="width:25%"><?php echo $ko_rec ?>	
					</tr></tbody>
				</table>
											
				<table style="margin-top:25px">
					<thead>
					<tr>
						<th scope="col"></th>
						<th scope="col"><?php _e("E-mail", "alo-easymail") ?></th>
						<th scope="col"><?php _e("Name", "alo-easymail") ?></th>
						<th scope="col"><?php _e("Language", "alo-easymail") ?></th>
						<th scope="col"><?php _e("Sent", "alo-easymail") ?></th>
						<th scope="col"><?php _e("Viewed", "alo-easymail") ?></th>						
					</tr>
				</thead>

				<tbody>
				<?php
				$class = "";
				$n = 0;
				foreach ($recipients as $recipient) {
					$class = ('' == $class) ? "style='background-color:#eee;'" : "";
					$n ++;
					echo "<tr $class ><td>".$n."</td><td>".$recipient['email']."</td><td>".$recipient['name']."</td>";
					echo "<td class='center'>". ALO_em_get_lang_flag($recipient['lang'], 'name') ."</td>";
					echo "<td class='center'><img src='".ALO_EM_PLUGIN_URL."/images/".(($recipient['result'] == 1)? "yes.png":"no.png") ."' /></td>";
					echo "<td class='center'>";
					echo "<img src='".ALO_EM_PLUGIN_URL."/images/".(($recipient['result'] == 1 && ALO_em_recipient_is_tracked ( $recipient['email'], $id, 'V' ))? "yes.png":"no.png") ."' />";
					echo "</td></tr>";
					//echo "<pre>"; print_r($recipient);echo "</pre>";
				}
				?>
			</tbody></table>
			</div>
			
		</div> <!-- end slider -->
		
	<?php } // end if $newsletter
} // edn if (isset($_REQUEST['id']) && (int)$_REQUEST['id'])
exit;
?>
