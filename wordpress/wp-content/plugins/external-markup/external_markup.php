<?php
/*
Plugin Name: External markup
Description: Retrieve parts of external content and include in blog framework
Author: TV4 AB, Aptivate
Version: 3.0
Author URI: http://www.tv4.se
*/

function em_Admin(){
	if(isset($_POST["submitted"])){
		$em_external_src = $_POST["input_external_src"];
		$em_external_src_cache = $_POST["input_external_src_cache"];
		
		update_option("em_external_src", $em_external_src);
		
		if(is_numeric($em_external_src_cache)){
			update_option("em_external_src_cache", $em_external_src_cache);
			$numeric_error = 0;
		}else{
			$numeric_error = 1;
		}
		
		if($numeric_error == 0){
			echo "<div id=\"message\" class=\"updated fade\"><p><strong>External markup settings is updated.</strong></p></div>";
		}else{
			echo "<div id=\"message\" class=\"updated fade\"><p><strong>External Cache must be numeric.</strong></p></div>";
		}
	}
?>
	<style type="text/css">
		th{font-weight: normal;padding-right: 10px;text-align: left;}
		table input{font-size: 11px;width: 200px;}
		div.external-markup-text{float: left;margin-left: 50px;width: 300px;}
		div.external-markup-text h4{margin: 0;padding: 0;}
		div.external-markup-text p{font-size: 11px; margin: 0 0 10px 0;padding: 0;}
		div.clear-float{clear: both;}
	</style>
	<div class="wrap">
		<h2>External markup settings</h2>
		<form method="post" name="options" target="_self">
			<table align="left">
				<tr>
					<th><label for="input_external_src">External URL:</label></th>
					<td><input id="input_external_src" name="input_external_src" type="text" value="<?php echo get_option("em_external_src"); ?>" /></td>
				</tr>
				<tr>
					<th><label for="input_external_src_cache">External Cache (seconds):</label></th>
					<td><input id="input_external_src_cache" name="input_external_src_cache" type="text" value="<?php echo get_option("em_external_src_cache"); ?>" /></td>
				</tr>
			</table>
			
			<div class="external-markup-text">
				<h4>Usage</h4>
				<p>The markup from external source must be tagged with specific html-comments. Plugin retrives markup from start/end comments.</p>

				<p>The htmlfile path is default set to /themes/TEMPLATENAME/em_cache/. Create folder /themes/TEMPLATENAME/em_cache/ and make it writeable (chmod 777)</p>

				<h4>Example</h4>
				<p>For retriving navigation markup from http://www.tv4.se:<br />Function call in template:  em_showContent("main-navigation start","main-navigation end",EM_EXAMPLE,FALSE)</p>

				<p><b>For more details, see readme.txt</b></p>
			</div>
			
			<div class="clear-float">&nbsp;</div>
			
			<p class="submit">
				<input name="submitted" type="hidden" value="yes" />
				<input type="submit" name="Submit" value="Update Options &raquo;" />
			</p>
		</form>
	</div>
<?php 
	}
	
	function em_Reg_Admin() {
		add_submenu_page('options-general.php', 'External markup', 'External markup', 10, __FILE__, 'em_Admin');
	}

	add_action('admin_menu', 'em_Reg_Admin');

/* Define retrival of options and the Blog ID */
define("BLOG_ID", $blog_id);
define("CACHE_TIME", get_option("em_cache_time"));
define("CACHE_DIR", get_option("em_cache_dir", "em_cache"));

/* -------------------------------------------------------------------------------------
	Define the different cached html files names and path.
	The path is default set to /themes/TEMPLATENAME/em_cache/
	The folder /themes/TEMPLATENAME/em_cache/ must be writeable (chmod 777)
	
	Default namesetting on the cached files is: blog_BLOG_ID_XXX.html
	The BLOG_ID is used for creating unique files, important when using Wordpress MU
---------------------------------------------------------------------------------------- */
define("EM_EXAMPLE", TEMPLATEPATH."/em_cache/blog_".BLOG_ID."_EXAMPLE.html");

/* 
----------------------------------------------------------------------------------------
	Function em_showContent is called from the templates. 
	It checks if the cached file already exists or it's to old (based on CACHE_TIME).
	$retrive_start = Start retriving from html comment
	$retrive_stop = Stop retriving before html comment
	$retrive_filename = Filename of cached htmlfile
----------------------------------------------------------------------------------------
*/
function em_showContent($retrive_start, $retrive_stop, $url, $cache_filename,
	$compress_file)
{
	if ($cache_filename)
	{
		$cache_filename = CACHE_DIR."/".$cache_filename;
	}
	
	if (!file_exists($cache_filename) || (time()-filemtime($cache_filename) >= CACHE_TIME))
	{
    	echo em_getContent($retrive_start, $retrive_stop, $url, $cache_filename,
    		$compress_file);
  	}
  	else
  	{
		include($cache_filename);
	}
}

function em_extract($content, $start_marker, $end_marker)
{
	$start_comment = "<!-- ".$start_marker." -->";
	$end_comment = "<!-- ".$end_marker." -->";
	$start_index   = stripos($content, $start_comment);
	$included_part = substr($content, $start_index + strlen($start_comment));
	$end_index     = stripos($included_part, $end_comment);
	$included_part = substr($included_part, 0, $end_index);
	return $included_part;
}

function em_error($message)
{
	return "<div class='em_error'>external_markup: $message</div>";
}

/* 
----------------------------------------------------------------------------------------
	Function em_getContent is called from function em_showContent if needed.
	em_showContent retrives the external markup with CURL or fOPEN.
	If the content that is returned is NULL, no cached file is created.
	$compress_file = If the file will be compressed when writing it (use with caution)
----------------------------------------------------------------------------------------
*/
function em_getContent($retrive_start, $retrive_stop, $url, $cache_filename, $compress_file)
{
	$markup = "";

	if (function_exists("curl_init"))
	{
		$ch = curl_init();
		$timeout = 5;
		curl_setopt($ch, CURLOPT_HEADER, 0);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT,$timeout);
		
		$markup = curl_exec($ch);
		if ($markup == FALSE)
		{
			$markup = em_error("Failed to retrieve URL: ".curl_error($ch));
		}
		
		curl_close($ch);
	}
	else
	{
		if ($fp = fopen($url, 'r')) {
			$markup = '';
			while ($line = fread($fp, 1024)) {
				$markup .= $line;
			}
			fclose($fp);
		} else {
			// Error when retriving data
		}
	}

	$data = em_extract($markup, $retrive_start, $retrive_stop);
	$data_length = strlen($data);

	if ($data_length < 1)
	{
		$data = em_error("No data returned from $url");
	}
	elseif ($cache_filename)
	{
		$fh = fopen($cache_filename, "w");
		if ($fh == FALSE)
		{
			$data = em_error("Failed to open cache file for writing: " .
				$cache_filename) . $data;
		}
		else
		{
			if ($compress_file == 1)
			{
				fwrite($fh, em_compress_file($data));
			}
			else
			{
				fwrite($fh, $data);
			}
		
			fclose($fh);
		}
	}
	
	return $data;
}

/* function based on: http://davidwalsh.name/compress-xhtml-page-output-php-output-buffers */
function em_compress_file($data){
	$search = array('/\>[^\S ]+/s','/[^\S ]+\</s','/(\s)+/s');
	$replace = array('>','<','\\1');
	$data = preg_replace($search, $replace, $data);
	return $data;
}
?>
