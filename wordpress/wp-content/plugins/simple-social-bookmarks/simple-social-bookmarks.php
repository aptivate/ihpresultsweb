<?php
/*
Plugin Name: Simple Social Bookmarks
Plugin URI: http://www.artiss.co.uk/simple-social-bookmarks
Description: Display links to social bookmark sites
Version: 3.0
Author: David Artiss
Author URI: http://www.artiss.co.uk
*/
define('simple_social_bookmarks_version','3.0');
include_once(WP_PLUGIN_DIR.'/'.str_replace(basename( __FILE__),"",plugin_basename(__FILE__))."define-bookmarks.php");

function simple_social_bookmarks($url="",$shorturl="",$style="",$add_paras="") {

    // Get parameters
    $icon_folder=social_bookmarks_parameters($add_paras,"iconfolder");
    $default=strtolower(social_bookmarks_parameters($add_paras,"default"));
    $nofollow=strtolower(social_bookmarks_parameters($add_paras,"nofollow"));
    $target=strtolower(social_bookmarks_parameters($add_paras,"target"));
    $priority=social_bookmarks_parameters($add_paras,"priority");
    $separator=strtolower(social_bookmarks_parameters($add_paras,"separator"));
    $unique_id=strtolower(social_bookmarks_parameters($add_paras,"id"));

    // Set up Shareaholic & AddThis URLs
    $shareaholic_url="http://www.shareaholic.com/api/share/?v=1&amp;apitype=1&amp;apikey=15770959566489cc042799dbc40c7cda4&amp;service=[service]&amp;title=[title]&amp;link=[url]";
    $addthis_url="http://api.addthis.com/oexchange/0.8/forward/[service]/offer?url=[url]&amp;title=[title]";
    $addtoany_url="http://www.addtoany.com/add_to/[service]?linkurl=[url]&linkname=[title]";

    // Set default parameters values
    $plugin_folder=WP_PLUGIN_URL.'/'.str_replace(basename( __FILE__),"",plugin_basename(__FILE__)); 
    
    if ($default=="") {$default="basic";}
    if ($nofollow=="no") {$nofollow='';} else {$nofollow=' rel="nofollow"';}
    if ($style!="") {$style=' style="'.$style.'"';}
    if ($target!="") {$target=' target="'.$target.'"';}
    if ($icon_folder=="") {
        $icon_folder=$plugin_folder."default/";
    } else {
        $icon_folder=get_bloginfo('template_url')."/".$icon_folder."/";
    }
    if ($url=="") {$url=get_permalink($post->ID);} 

    if (substr($shorturl,0,4)!="http") {$shorturl="";}
    if ($shorturl=="") {$shorturl=$url;}
    if (($priority!="123")&&($priority!="132")&&($priority!="213")&&($priority!="231")&&($priority!="312")&&($priority!="321")) {$priority="123";}
    
    // Get the post title and blog URL
    $title=urlencode(html_entity_decode(get_the_title($post->ID),ENT_QUOTES,'UTF-8'));
    $email_title=rawurlencode(html_entity_decode(get_the_title($post->ID),ENT_QUOTES,'UTF-8'));
    $email_text=rawurlencode($url);

    // Build the services array and output plugin information as an HTML comment
    $social_sites=setup_social_sites();
    $echoout="<!-- Simple Social Bookmarks v".simple_social_bookmarks_version." | http://www.artiss.co.uk/simple-social-bookmarks -->\n";
    $echoout.="<!-- ".__("Using icon folder at ").$icon_folder." -->\n";

    $tools=false;
    // Loop through the services array and output each that has been selected
    foreach ($social_sites as $social_data) {

        if (($social_data[0]!="")or($social_data[1]!="")or($social_data[2]!="")or($social_data[3]!="")) {

            // Extract individual fields for current service
            if (substr($social_data[0],0,1)=="#") {
                $basic=true;
                $alt_text=substr($social_data[0],1);
            } else {
                $basic=false;
                $alt_text=$social_data[0];
            }
            if (substr($social_data[1],0,1)=="#") {
                $shorten=true;
                $social_data[1]=substr($social_data[1],1);
            } else {
                $shorten=false;
            }
            $service_name=$social_data[1];
            $icon_name=$social_data[1];
            $addthis_service=$social_data[2];
            $shareaholic_service=$social_data[3];
            $addtoany_service=$social_data[4];
            $service_url=$social_data[5];

            // Determine which service to use (or supplied URL)
            $loop=0;
            $service_found=false;
            while (($loop<3)&&(!$service_found)) {
                $service=substr($priority,$loop,1);
                if (($service==1)&&($addthis_service!="")) {
                    $service_url=str_replace('[service]',$addthis_service,$addthis_url);
                    $service_found=true;
                }
                if (($service==2)&&($shareaholic_service!="")) {
                    $service_url=str_replace('[service]',$shareaholic_service,$shareaholic_url);
                    $service_found=true;
                } 
                if (($service==3)&&($addtoany_service!="")) {
                    $service_url=str_replace('[service]',$addtoany_service,$addtoany_url);
                    $service_found=true;
                }                 
                $loop++;
            }
            //if (($addthis_service!="")or($shareaholic_service!="")) {
            //    if (($addthis_service!="")&&(($shareaholic_service=="")or($priority!="shareaholic"))) {
            //        $service_url=str_replace('[service]',$addthis_service,$addthis_url); 
            //    } else {
            //        $service_url=str_replace('[service]',$shareaholic_service,$shareaholic_url);
            //    }
            //}
            if ($shorten) {$service_url=str_replace('[url]','[shorturl]',$service_url);}

            // Look to see if a parameter exists for the current service
            $option=strtolower(social_bookmarks_parameters($add_paras,$service_name));

            // Decide if service should be displayed
            $switch=false;
            if ((($basic===false)&&($default=="on"))or(($basic===true)&&($default!="off"))) {$switch=true;}

            // Add service to output (if appropriate)
            if (($option=="on")or(($switch===true)&&($option!="off"))) {

                // If we are displaying tools and a separator has been requested then display it
                // Switch tools flag off so the separator is not shown again
                if ($first_tool) {
                    if ($separator=="yes") {$echoout.="<img src=\"".$icon_folder."separator.png\" alt=\"".__("Separator")."\" title=\"".__("Separator")."\" class=\"ssb_sep\"".$style."/>";}
                    $first_tool=false;
                }

                // Now generate the XHTML for the social bookmark
                $echoout.="<a href=\"".$service_url."\" class=\"ssb\"".$target.$nofollow;
                if ($unique_id!="") {
                    // Add the code for animation, if required
                    $image_id=$service_name."_".$unique_id;
                    $mouseover=" document.getElementById('".$image_id."').src='".$icon_folder.$icon_name."_hov.png';";
                    $mouseout=" document.getElementById('".$image_id."').src='".$icon_folder.$icon_name.".png';";
                    $echoout.=" onmouseover=\"".$mouseover."\"";
                    $echoout.=" onmouseout=\"".$mouseout."\"";
                }
                $echoout.="><img src=\"".$icon_folder.$icon_name.".png\" ";
                if ($unique_id!="") {$echoout.="id=\"".$image_id."\" ";}
                $echoout.="alt=\"".$alt_text."\" title=\"".$alt_text."\" class=\"ssb\"".$style." />";
                $echoout.="</a>\n";
            }
        } else {
            // Blank record found, indicating a change from bookmarks to tools
            $first_tool=true;
        }
    }

    // Replace all the possible parameters within the URL
    $echoout=str_replace('[url]',$url,$echoout);
    $echoout=str_replace('[shorturl]',$shorturl,$echoout);
    $echoout=str_replace('[title]',$title,$echoout);
    $echoout=str_replace('[email_title]',$email_title,$echoout);
    $echoout=str_replace('[email_text]',$email_text,$echoout); 
    $echoout.="<!-- ".__("End of Simple Social Bookmarks code")." -->\n";
    return $echoout; 
}

// Function to extract parameters from an input string (1.0)
function social_bookmarks_parameters($input,$para) {
    $start=strpos(strtolower($input),$para."=");
    $content="";
    if ($start!==false) {
        $start=$start+strlen($para)+1;
        $end=strpos(strtolower($input),"&",$start);
        if ($end!==false) {$end=$end-1;} else {$end=strlen($input);}
        $content=substr($input,$start,$end-$start+1);
    }
    return $content;
}
?>