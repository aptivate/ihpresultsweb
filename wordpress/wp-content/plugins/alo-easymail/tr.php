<?php 

include('../../../wp-load.php');
global $wpdb;

/*

Feature inspired by phplist: http://www.phplist.com/
Many thanks to those are working on it!


eg. link in email:
'<img src="{...path_to_easymail_dir...}tr.php?n={idnewsletter}&e1={account_email}&e2={domain_email.lt}d&k={12345_subscriber_unikey}" width="1" height="1" border="0" >';
*/

ob_start();
error_reporting(0);

$newsletter	= ( isset($_REQUEST['n']) && (int)$_REQUEST['n'] ) ? $wpdb->escape( $_REQUEST['n'] ) : false;
$e1			= ( isset($_REQUEST['e1']) ) ? $wpdb->escape( $_REQUEST['e1'] ) : "";
$e2			= ( isset($_REQUEST['e2']) ) ? $wpdb->escape( $_REQUEST['e2'] ) : "";
$email		= ( is_email ( $e1."@".$e2 ) ) ? $e1."@".$e2 : false;
$unikey		= ( isset($_REQUEST['k']) ) ? $wpdb->escape( $_REQUEST['k'] ) : false;

$can_add = false; // prepare permission

if ( $newsletter && $email && $unikey ) {
	
	// check subscriber id and unikey
	$can_add	= ALO_em_check_subscriber_email_and_unikey ( $email, $unikey );

	// If already tracking, don't add again!
	if ( ALO_em_recipient_is_tracked ( $email, $newsletter, "V" ) ) $can_add = false;
    
    if ( $can_add ) { // So, if can add, insert in db
	    ALO_em_add_tracking ( $email, $newsletter, "V" );
	}
}

//echo $wpdb->last_query;

// print 1 pixel png image
@ob_end_clean();
header("Content-Type: image/png");
print base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAABGdBTUEAALGPC/xhBQAAAAZQTFRF////AAAAVcLTfgAAAAF0Uk5TAEDm2GYAAAABYktHRACIBR1IAAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH0gQCEx05cqKA8gAAAApJREFUeJxjYAAAAAIAAUivpHEAAAAASUVORK5CYII=');

?>
