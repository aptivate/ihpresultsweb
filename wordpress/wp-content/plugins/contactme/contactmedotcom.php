<?php
/**
 * Main plugin definition
 * Plugin Name: Contact Form by ContactMe.com
 * Plugin URI: http://www.contactme.com/
 * Description: Contact form and button by ContactMe.com
 * Author: ContactMe.com
 * Author URI: http://www.contactme.com/
 * Version: 2.1
 */

// Adding Contact Me Asset Files (JS + CSS) 
function load_button_code() {
	$contact_me_data = unserialize(get_option("contact_me_data"));
	if (count($contact_me_data["button"]) == 0) return;
	echo "<script type='text/javascript'>var _cmo = {";
	$count = 0;
	foreach ($contact_me_data["button"] as $key => $value) {
		$count++;
		echo $key.': "'. $value.'"';
		if ($count < count($contact_me_data["button"])) echo ",";
	}
	echo "}; (function() {var cms = document.createElement('script'); cms.type = 'text/javascript'; cms.async = true; cms.src = '".$contact_me_data["button_src"]."'; var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(cms, s);})();</script>";
}

add_action('init', 'contact_me_assets');

function contact_me_assets() {
	$contact_me_data = unserialize(get_option("contact_me_data"));
	if (count($contact_me_data) == 0) return;
	
	if (function_exists('wp_footer')) {
		if (!is_admin()){
			if (!$_POST['contact_me_data']) {
				if (isset($contact_me_data["form_id"]) && $contact_me_data["sticky_button"] == "true") {
					add_action( 'wp_footer', 'load_button_code' ); 
				}
			}
		}
	}
	elseif (function_exists('wp_head')) {
		if (!is_admin()){
			if (!$_POST['contact_me_data']) {
				if (isset($contact_me_data["form_id"]) && $contact_me_data["sticky_button"] == "true") {
					add_action( 'wp_head', 'load_button_code' ); 
				}
			}
		}
	}
}

// Adding Admin Menu
add_action('admin_menu', 'contact_me_plugin_menu');

function contact_me_plugin_menu() {
	add_options_page('ContactMe Settings', 'ContactMe Form', 10, __FILE__, 'contact_me_setup');
}


function contact_me_setup() {
	$contact_me_data = unserialize(get_option("contact_me_data"));
	if ($_POST) {
		$contact_me_data = unserialize(stripslashes($_POST["contact_me_data"]));
		$contact_me_action = $contact_me_data["action"];
		unset($contact_me_data["action"]);
		
		if ($contact_me_action == "save_account") { 
			$old_data = unserialize(get_option('contact_me_data'));
			if ($old_data["wp_page_id"]) wp_delete_post($old_data["wp_page_id"]);
			if ($contact_me_data["publish_page"] == "true") {
				if (!get_post($contact_me_data["wp_page_id"])) {
					$contact_me_page_id = wp_insert_post(array(
						'post_status' => 'publish',
						'post_type' => 'page',
						'post_name' => $contact_me_data["button"]["label"],
						'post_title' => $contact_me_data["button"]["label"],
						'comment_status' => 'closed',
						'post_content' => '<iframe src="'.$contact_me_data["embed_src"].'" frameborder="0" scrolling="no" allowtransparency="true" style="height: '.$contact_me_data["embed_height"].'px; width: '.$contact_me_data["embed_width"].'px;"></iframe>'
					));
					$contact_me_data["wp_page_id"] = $contact_me_page_id;
				}
			}
			update_option("contact_me_data", serialize($contact_me_data));
		}
		elseif ($contact_me_action == "save_settings") { 
			if (get_option('contact_me_data')) {
				$contact_me_data = array_merge(unserialize(get_option('contact_me_data')), $contact_me_data);
			}

			if ($contact_me_data["publish_page"] == "true") {
				if (!get_post($contact_me_data["wp_page_id"])) {
					$contact_me_page_id = wp_insert_post(array(
						'post_status' => 'publish',
						'post_type' => 'page',
						'post_name' => $contact_me_data["button"]["label"],
						'post_title' => $contact_me_data["button"]["label"],
						'comment_status' => 'closed',
						'post_content' => '<iframe src="'.$contact_me_data["embed_src"].'" frameborder="0" scrolling="no" allowtransparency="true" style="height: '.$contact_me_data["embed_height"].'px; width: '.$contact_me_data["embed_width"].'px;"></iframe>'
					));
					$contact_me_data["wp_page_id"] = $contact_me_page_id;
				} else {
					$contact_me_page_id = wp_update_post(array(
						'ID' => $contact_me_data["wp_page_id"],
						'post_status' => 'publish',
						'post_type' => 'page',
						'post_name' => $contact_me_data["button"]["label"],
						'post_title' => $contact_me_data["button"]["label"],
						'comment_status' => 'closed',
						'post_content' => '<iframe src="'.$contact_me_data["embed_src"].'" frameborder="0" scrolling="no" allowtransparency="true" style="height: '.$contact_me_data["embed_height"].'px; width: '.$contact_me_data["embed_width"].'px;"></iframe>'
					));
					$contact_me_data["wp_page_id"] = $contact_me_page_id;
				}
			} else {
				wp_delete_post($contact_me_data["wp_page_id"]);
				unset($contact_me_data["wp_page_id"]);
			}
			update_option("contact_me_data", serialize($contact_me_data));
		}
	}
?>
<script type="text/javascript">
function xd_resize(data) {
	if (typeof data.width == 'undefined' || typeof data.height == 'undefined') return;
	jQuery("#contact_me_frame").css("width", data.width+"px");
	jQuery("#contact_me_frame").css("height", data.height+"px");
}

function xd_callback(data) {
	jQuery("#contact_me_data").val(data.data);
	jQuery("#contact_me_form").submit();
}
</script>
<form method="post" id="contact_me_form" action="">
	<input type="hidden" id="contact_me_data" name="contact_me_data" value="" />
</form>
<iframe id="contact_me_frame" src="http://www.contactme.com/wordpress?plugin_url=<?php echo get_bloginfo('wpurl') . '/wp-content/plugins/contactme' ?>&<?php echo http_build_query($contact_me_data) ?>" frameborder="0" scrolling="no" allowtransparency="true" style="width: 720px; height: 650px; margin: 15px 15px 0 5px;"></iframe>
<?php  
}

register_uninstall_hook(__FILE__, 'contact_me_uninstall');
register_deactivation_hook(__FILE__, 'contact_me_uninstall');
	
function contact_me_uninstall() {
	$old_data = unserialize(get_option('contact_me_data'));
	if ($old_data["wp_page_id"]) wp_delete_post($old_data["wp_page_id"]);
	update_option("contact_me_data", "");
}
?>