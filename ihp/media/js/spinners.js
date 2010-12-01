
    

  

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html;charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
        <title>spinners.js at master from staaky's spinners - GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />

    <link href="https://assets0.github.com/stylesheets/bundle_common.css?9cca70593ea5e402012810a9233fc52d8f97cb13" media="screen" rel="stylesheet" type="text/css" />
<link href="https://assets0.github.com/stylesheets/bundle_github.css?9cca70593ea5e402012810a9233fc52d8f97cb13" media="screen" rel="stylesheet" type="text/css" />

    <script type="text/javascript" charset="utf-8">
      var GitHub = {}
      var github_user = null
      
    </script>
    <script src="https://assets2.github.com/javascripts/jquery/jquery-1.4.2.min.js?9cca70593ea5e402012810a9233fc52d8f97cb13" type="text/javascript"></script>
    <script src="https://assets2.github.com/javascripts/bundle_common.js?9cca70593ea5e402012810a9233fc52d8f97cb13" type="text/javascript"></script>
<script src="https://assets3.github.com/javascripts/bundle_github.js?9cca70593ea5e402012810a9233fc52d8f97cb13" type="text/javascript"></script>

        <script type="text/javascript" charset="utf-8">
      GitHub.spy({
        repo: "staaky/spinners"
      })
    </script>

    
  
    
  

  <link href="https://github.com/staaky/spinners/commits/master.atom" rel="alternate" title="Recent Commits to spinners:master" type="application/atom+xml" />

        <meta name="description" content="JavaScript loading animations in pure Canvas!" />
    <script type="text/javascript">
      GitHub.nameWithOwner = GitHub.nameWithOwner || "staaky/spinners";
      GitHub.currentRef = 'master';
    </script>
  

            <script type="text/javascript">
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-3769691-2']);
      _gaq.push(['_trackPageview']);
      (function() {
        var ga = document.createElement('script');
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        ga.setAttribute('async', 'true');
        document.documentElement.firstChild.appendChild(ga);
      })();
    </script>

  </head>

  

  <body class="logged_out ">
    

    
      <script type="text/javascript">
        var _kmq = _kmq || [];
        function _kms(u){
          var s = document.createElement('script'); var f = document.getElementsByTagName('script')[0]; s.type = 'text/javascript'; s.async = true;
          s.src = u; f.parentNode.insertBefore(s, f);
        }
        _kms('//i.kissmetrics.com/i.js');_kms('//doug1izaerwt3.cloudfront.net/406e8bf3a2b8846ead55afb3cfaf6664523e3a54.1.js');
      </script>
    

    

    

    

    <div class="subnavd" id="main">
      <div id="header" class="true">
        
          <a class="logo boring" href="https://github.com">
            <img src="/images/modules/header/logov3.png?changed" class="default" alt="github" />
            <![if !IE]>
            <img src="/images/modules/header/logov3-hover.png" class="hover" alt="github" />
            <![endif]>
          </a>
        
        
        <div class="topsearch">
  
    <ul class="nav logged_out">
      <li class="pricing"><a href="/plans">Pricing and Signup</a></li>
      <li><a href="/explore">Explore GitHub</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="https://github.com/login">Login</a></li>
    </ul>
  
</div>

      </div>

      
      
        
    <div class="site">
      <div class="pagehead repohead vis-public   ">

      

      <div class="title-actions-bar">
        <h1>
          <a href="/staaky">staaky</a> / <strong><a href="https://github.com/staaky/spinners">spinners</a></strong>
          
          
        </h1>

        
    <ul class="actions">
      

      
        <li class="for-owner" style="display:none"><a href="https://github.com/staaky/spinners/admin" class="minibutton btn-admin "><span><span class="icon"></span>Admin</span></a></li>
        <li>
          <a href="/staaky/spinners/toggle_watch" class="minibutton btn-watch " id="watch_button" onclick="var f = document.createElement('form'); f.style.display = 'none'; this.parentNode.appendChild(f); f.method = 'POST'; f.action = this.href;var s = document.createElement('input'); s.setAttribute('type', 'hidden'); s.setAttribute('name', 'authenticity_token'); s.setAttribute('value', '7ed14d1a6644ac2eca49f7be6b7072ba1f41afa5'); f.appendChild(s);f.submit();return false;" style="display:none"><span><span class="icon"></span>Watch</span></a>
          <a href="/staaky/spinners/toggle_watch" class="minibutton btn-watch " id="unwatch_button" onclick="var f = document.createElement('form'); f.style.display = 'none'; this.parentNode.appendChild(f); f.method = 'POST'; f.action = this.href;var s = document.createElement('input'); s.setAttribute('type', 'hidden'); s.setAttribute('name', 'authenticity_token'); s.setAttribute('value', '7ed14d1a6644ac2eca49f7be6b7072ba1f41afa5'); f.appendChild(s);f.submit();return false;" style="display:none"><span><span class="icon"></span>Unwatch</span></a>
        </li>
        
          
            <li class="for-notforked" style="display:none"><a href="/staaky/spinners/fork" class="minibutton btn-fork " id="fork_button" onclick="var f = document.createElement('form'); f.style.display = 'none'; this.parentNode.appendChild(f); f.method = 'POST'; f.action = this.href;var s = document.createElement('input'); s.setAttribute('type', 'hidden'); s.setAttribute('name', 'authenticity_token'); s.setAttribute('value', '7ed14d1a6644ac2eca49f7be6b7072ba1f41afa5'); f.appendChild(s);f.submit();return false;"><span><span class="icon"></span>Fork</span></a></li>
            <li class="for-hasfork" style="display:none"><a href="#" class="minibutton btn-fork " id="your_fork_button"><span><span class="icon"></span>Your Fork</span></a></li>
          

          
        
      
      
      <li class="repostats">
        <ul class="repo-stats">
          <li class="watchers"><a href="/staaky/spinners/watchers" title="Watchers" class="tooltipped downwards">17</a></li>
          <li class="forks"><a href="/staaky/spinners/network" title="Forks" class="tooltipped downwards">1</a></li>
        </ul>
      </li>
    </ul>

      </div>

        
  <ul class="tabs">
    <li><a href="https://github.com/staaky/spinners/tree/master" class="selected" highlight="repo_source">Source</a></li>
    <li><a href="https://github.com/staaky/spinners/commits/master" highlight="repo_commits">Commits</a></li>
    <li><a href="/staaky/spinners/network" highlight="repo_network">Network</a></li>
    <li><a href="/staaky/spinners/pulls" highlight="repo_pulls">Pull Requests (0)</a></li>

    

    
      
      <li><a href="/staaky/spinners/issues" highlight="issues">Issues (0)</a></li>
    

            
    <li><a href="/staaky/spinners/graphs" highlight="repo_graphs">Graphs</a></li>

    <li class="contextswitch nochoices">
      <span class="toggle leftwards" >
        <em>Branch:</em>
        <code>master</code>
      </span>
    </li>
  </ul>

  <div style="display:none" id="pl-description"><p><em class="placeholder">click here to add a description</em></p></div>
  <div style="display:none" id="pl-homepage"><p><em class="placeholder">click here to add a homepage</em></p></div>

  <div class="subnav-bar">
  
  <ul>
    <li>
      <a href="#" class="dropdown">Switch Branches (1)</a>
      <ul>
        
          
            <li><strong>master &#x2713;</strong></li>
            
      </ul>
    </li>
    <li>
      <a href="#" class="dropdown defunct">Switch Tags (0)</a>
      
    </li>
    <li>
    
    <a href="/staaky/spinners/branches" class="manage">Branch List</a>
    
    </li>
  </ul>
</div>

  
  
  
  
  
  



        
    <div id="repo_details" class="metabox clearfix">
      <div id="repo_details_loader" class="metabox-loader" style="display:none">Sending Request&hellip;</div>

        <a href="/staaky/spinners/downloads" class="download-source" id="download_button" title="Download source, tagged packages and binaries."><span class="icon"></span>Downloads</a>

      <div id="repository_desc_wrapper">
      <div id="repository_description" rel="repository_description_edit">
        
          <p>JavaScript loading animations in pure Canvas!
            <span id="read_more" style="display:none">&mdash; <a href="#readme">Read more</a></span>
          </p>
        
      </div>

      <div id="repository_description_edit" style="display:none;" class="inline-edit">
        <form action="/staaky/spinners/admin/update" method="post"><div style="margin:0;padding:0"><input name="authenticity_token" type="hidden" value="7ed14d1a6644ac2eca49f7be6b7072ba1f41afa5" /></div>
          <input type="hidden" name="field" value="repository_description">
          <input type="text" class="textfield" name="value" value="JavaScript loading animations in pure Canvas!">
          <div class="form-actions">
            <button class="minibutton"><span>Save</span></button> &nbsp; <a href="#" class="cancel">Cancel</a>
          </div>
        </form>
      </div>

      
      <div class="repository-homepage" id="repository_homepage" rel="repository_homepage_edit">
        <p><a href="http://" rel="nofollow"></a></p>
      </div>

      <div id="repository_homepage_edit" style="display:none;" class="inline-edit">
        <form action="/staaky/spinners/admin/update" method="post"><div style="margin:0;padding:0"><input name="authenticity_token" type="hidden" value="7ed14d1a6644ac2eca49f7be6b7072ba1f41afa5" /></div>
          <input type="hidden" name="field" value="repository_homepage">
          <input type="text" class="textfield" name="value" value="">
          <div class="form-actions">
            <button class="minibutton"><span>Save</span></button> &nbsp; <a href="#" class="cancel">Cancel</a>
          </div>
        </form>
      </div>
      </div>
      <div class="rule "></div>
            <div id="url_box" class="url-box">
        <ul class="clone-urls">
          
            
            <li id="http_clone_url"><a href="https://github.com/staaky/spinners.git" data-permissions="Read-Only">HTTP</a></li>
            <li id="public_clone_url"><a href="git://github.com/staaky/spinners.git" data-permissions="Read-Only">Git Read-Only</a></li>
          
          
        </ul>
        <input type="text" spellcheck="false" id="url_field" class="url-field" />
              <span style="display:none" id="url_box_clippy"></span>
      <span id="clippy_tooltip_url_box_clippy" class="clippy-tooltip tooltipped" title="copy to clipboard">
      <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
              width="14"
              height="14"
              class="clippy"
              id="clippy" >
      <param name="movie" value="https://assets2.github.com/flash/clippy.swf?v5"/>
      <param name="allowScriptAccess" value="always" />
      <param name="quality" value="high" />
      <param name="scale" value="noscale" />
      <param NAME="FlashVars" value="id=url_box_clippy&amp;copied=&amp;copyto=">
      <param name="bgcolor" value="#FFFFFF">
      <param name="wmode" value="opaque">
      <embed src="https://assets2.github.com/flash/clippy.swf?v5"
             width="14"
             height="14"
             name="clippy"
             quality="high"
             allowScriptAccess="always"
             type="application/x-shockwave-flash"
             pluginspage="http://www.macromedia.com/go/getflashplayer"
             FlashVars="id=url_box_clippy&amp;copied=&amp;copyto="
             bgcolor="#FFFFFF"
             wmode="opaque"
      />
      </object>
      </span>

        <p id="url_description">This URL has <strong>Read+Write</strong> access</p>
      </div>
    </div>


        

      </div><!-- /.pagehead -->

      









<script type="text/javascript">
  GitHub.currentCommitRef = 'master'
  GitHub.currentRepoOwner = 'staaky'
  GitHub.currentRepo = "spinners"
  GitHub.downloadRepo = '/staaky/spinners/archives/master'
  GitHub.revType = "master"

  GitHub.controllerName = "blob"
  GitHub.actionName     = "show"
  GitHub.currentAction  = "blob#show"

  

  
</script>








  <div id="commit">
    <div class="group">
        
  <div class="envelope commit">
    <div class="human">
      
        <div class="message"><pre><a href="/staaky/spinners/commit/bdc5c21f0439057d2014134847f2fbc52d95b0a1">more readme corrections</a> </pre></div>
      

      <div class="actor">
        <div class="gravatar">
          
          <img src="https://secure.gravatar.com/avatar/3d85f3bc674c199d42fa03f5da5bbb33?s=140&d=https%3A%2F%2Fgithub.com%2Fimages%2Fgravatars%2Fgravatar-140.png" alt="" width="30" height="30"  />
        </div>
        <div class="name"><a href="/staaky">staaky</a> <span>(author)</span></div>
        <div class="date">
          <abbr class="relatize" title="2010-11-09 09:34:28">Tue Nov 09 09:34:28 -0800 2010</abbr>
        </div>
      </div>

      

    </div>
    <div class="machine">
      <span>c</span>ommit&nbsp;&nbsp;<a href="/staaky/spinners/commit/bdc5c21f0439057d2014134847f2fbc52d95b0a1" hotkey="c">bdc5c21f0439057d2014</a><br />
      <span>t</span>ree&nbsp;&nbsp;&nbsp;&nbsp;<a href="/staaky/spinners/tree/bdc5c21f0439057d2014134847f2fbc52d95b0a1" hotkey="t">ba7c5f36e68e13486ac1</a><br />
      
        <span>p</span>arent&nbsp;
        
        <a href="/staaky/spinners/tree/e0206ca8cd06dcadf9c93c1e246ded41add2a742" hotkey="p">e0206ca8cd06dcadf9c9</a>
      

    </div>
  </div>

    </div>
  </div>



  
    <div id="path">
      <b><a href="/staaky/spinners/tree/master">spinners</a></b> / spinners.js       <span style="display:none" id="clippy_4376">spinners.js</span>
      
      <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
              width="110"
              height="14"
              class="clippy"
              id="clippy" >
      <param name="movie" value="https://assets1.github.com/flash/clippy.swf?v5"/>
      <param name="allowScriptAccess" value="always" />
      <param name="quality" value="high" />
      <param name="scale" value="noscale" />
      <param NAME="FlashVars" value="id=clippy_4376&amp;copied=copied!&amp;copyto=copy to clipboard">
      <param name="bgcolor" value="#FFFFFF">
      <param name="wmode" value="opaque">
      <embed src="https://assets1.github.com/flash/clippy.swf?v5"
             width="110"
             height="14"
             name="clippy"
             quality="high"
             allowScriptAccess="always"
             type="application/x-shockwave-flash"
             pluginspage="http://www.macromedia.com/go/getflashplayer"
             FlashVars="id=clippy_4376&amp;copied=copied!&amp;copyto=copy to clipboard"
             bgcolor="#FFFFFF"
             wmode="opaque"
      />
      </object>
      

    </div>

    <div id="files">
      <div class="file">
        <div class="meta">
          <div class="info">
            <span class="icon"><img alt="Txt" height="16" src="https://assets2.github.com/images/icons/txt.png?bd5b57138194d8b178fd949e16173262d8b89778" width="16" /></span>
            <span class="mode" title="File Mode">100644</span>
            
              <span>514 lines (413 sloc)</span>
            
            <span>11.314 kb</span>
          </div>
          <ul class="actions">
            
              <li><a id="file-edit-link" href="#" rel="/staaky/spinners/file-edit/__ref__/spinners.js">edit</a></li>
            
            <li><a href="/staaky/spinners/raw/master/spinners.js" id="raw-url">raw</a></li>
            
              <li><a href="/staaky/spinners/blame/master/spinners.js">blame</a></li>
            
            <li><a href="/staaky/spinners/commits/master/spinners.js">history</a></li>
          </ul>
        </div>
        
  <div class="data type-javascript">
    
      <table cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <pre class="line_numbers"><span id="LID1" rel="#L1">1</span>
<span id="LID2" rel="#L2">2</span>
<span id="LID3" rel="#L3">3</span>
<span id="LID4" rel="#L4">4</span>
<span id="LID5" rel="#L5">5</span>
<span id="LID6" rel="#L6">6</span>
<span id="LID7" rel="#L7">7</span>
<span id="LID8" rel="#L8">8</span>
<span id="LID9" rel="#L9">9</span>
<span id="LID10" rel="#L10">10</span>
<span id="LID11" rel="#L11">11</span>
<span id="LID12" rel="#L12">12</span>
<span id="LID13" rel="#L13">13</span>
<span id="LID14" rel="#L14">14</span>
<span id="LID15" rel="#L15">15</span>
<span id="LID16" rel="#L16">16</span>
<span id="LID17" rel="#L17">17</span>
<span id="LID18" rel="#L18">18</span>
<span id="LID19" rel="#L19">19</span>
<span id="LID20" rel="#L20">20</span>
<span id="LID21" rel="#L21">21</span>
<span id="LID22" rel="#L22">22</span>
<span id="LID23" rel="#L23">23</span>
<span id="LID24" rel="#L24">24</span>
<span id="LID25" rel="#L25">25</span>
<span id="LID26" rel="#L26">26</span>
<span id="LID27" rel="#L27">27</span>
<span id="LID28" rel="#L28">28</span>
<span id="LID29" rel="#L29">29</span>
<span id="LID30" rel="#L30">30</span>
<span id="LID31" rel="#L31">31</span>
<span id="LID32" rel="#L32">32</span>
<span id="LID33" rel="#L33">33</span>
<span id="LID34" rel="#L34">34</span>
<span id="LID35" rel="#L35">35</span>
<span id="LID36" rel="#L36">36</span>
<span id="LID37" rel="#L37">37</span>
<span id="LID38" rel="#L38">38</span>
<span id="LID39" rel="#L39">39</span>
<span id="LID40" rel="#L40">40</span>
<span id="LID41" rel="#L41">41</span>
<span id="LID42" rel="#L42">42</span>
<span id="LID43" rel="#L43">43</span>
<span id="LID44" rel="#L44">44</span>
<span id="LID45" rel="#L45">45</span>
<span id="LID46" rel="#L46">46</span>
<span id="LID47" rel="#L47">47</span>
<span id="LID48" rel="#L48">48</span>
<span id="LID49" rel="#L49">49</span>
<span id="LID50" rel="#L50">50</span>
<span id="LID51" rel="#L51">51</span>
<span id="LID52" rel="#L52">52</span>
<span id="LID53" rel="#L53">53</span>
<span id="LID54" rel="#L54">54</span>
<span id="LID55" rel="#L55">55</span>
<span id="LID56" rel="#L56">56</span>
<span id="LID57" rel="#L57">57</span>
<span id="LID58" rel="#L58">58</span>
<span id="LID59" rel="#L59">59</span>
<span id="LID60" rel="#L60">60</span>
<span id="LID61" rel="#L61">61</span>
<span id="LID62" rel="#L62">62</span>
<span id="LID63" rel="#L63">63</span>
<span id="LID64" rel="#L64">64</span>
<span id="LID65" rel="#L65">65</span>
<span id="LID66" rel="#L66">66</span>
<span id="LID67" rel="#L67">67</span>
<span id="LID68" rel="#L68">68</span>
<span id="LID69" rel="#L69">69</span>
<span id="LID70" rel="#L70">70</span>
<span id="LID71" rel="#L71">71</span>
<span id="LID72" rel="#L72">72</span>
<span id="LID73" rel="#L73">73</span>
<span id="LID74" rel="#L74">74</span>
<span id="LID75" rel="#L75">75</span>
<span id="LID76" rel="#L76">76</span>
<span id="LID77" rel="#L77">77</span>
<span id="LID78" rel="#L78">78</span>
<span id="LID79" rel="#L79">79</span>
<span id="LID80" rel="#L80">80</span>
<span id="LID81" rel="#L81">81</span>
<span id="LID82" rel="#L82">82</span>
<span id="LID83" rel="#L83">83</span>
<span id="LID84" rel="#L84">84</span>
<span id="LID85" rel="#L85">85</span>
<span id="LID86" rel="#L86">86</span>
<span id="LID87" rel="#L87">87</span>
<span id="LID88" rel="#L88">88</span>
<span id="LID89" rel="#L89">89</span>
<span id="LID90" rel="#L90">90</span>
<span id="LID91" rel="#L91">91</span>
<span id="LID92" rel="#L92">92</span>
<span id="LID93" rel="#L93">93</span>
<span id="LID94" rel="#L94">94</span>
<span id="LID95" rel="#L95">95</span>
<span id="LID96" rel="#L96">96</span>
<span id="LID97" rel="#L97">97</span>
<span id="LID98" rel="#L98">98</span>
<span id="LID99" rel="#L99">99</span>
<span id="LID100" rel="#L100">100</span>
<span id="LID101" rel="#L101">101</span>
<span id="LID102" rel="#L102">102</span>
<span id="LID103" rel="#L103">103</span>
<span id="LID104" rel="#L104">104</span>
<span id="LID105" rel="#L105">105</span>
<span id="LID106" rel="#L106">106</span>
<span id="LID107" rel="#L107">107</span>
<span id="LID108" rel="#L108">108</span>
<span id="LID109" rel="#L109">109</span>
<span id="LID110" rel="#L110">110</span>
<span id="LID111" rel="#L111">111</span>
<span id="LID112" rel="#L112">112</span>
<span id="LID113" rel="#L113">113</span>
<span id="LID114" rel="#L114">114</span>
<span id="LID115" rel="#L115">115</span>
<span id="LID116" rel="#L116">116</span>
<span id="LID117" rel="#L117">117</span>
<span id="LID118" rel="#L118">118</span>
<span id="LID119" rel="#L119">119</span>
<span id="LID120" rel="#L120">120</span>
<span id="LID121" rel="#L121">121</span>
<span id="LID122" rel="#L122">122</span>
<span id="LID123" rel="#L123">123</span>
<span id="LID124" rel="#L124">124</span>
<span id="LID125" rel="#L125">125</span>
<span id="LID126" rel="#L126">126</span>
<span id="LID127" rel="#L127">127</span>
<span id="LID128" rel="#L128">128</span>
<span id="LID129" rel="#L129">129</span>
<span id="LID130" rel="#L130">130</span>
<span id="LID131" rel="#L131">131</span>
<span id="LID132" rel="#L132">132</span>
<span id="LID133" rel="#L133">133</span>
<span id="LID134" rel="#L134">134</span>
<span id="LID135" rel="#L135">135</span>
<span id="LID136" rel="#L136">136</span>
<span id="LID137" rel="#L137">137</span>
<span id="LID138" rel="#L138">138</span>
<span id="LID139" rel="#L139">139</span>
<span id="LID140" rel="#L140">140</span>
<span id="LID141" rel="#L141">141</span>
<span id="LID142" rel="#L142">142</span>
<span id="LID143" rel="#L143">143</span>
<span id="LID144" rel="#L144">144</span>
<span id="LID145" rel="#L145">145</span>
<span id="LID146" rel="#L146">146</span>
<span id="LID147" rel="#L147">147</span>
<span id="LID148" rel="#L148">148</span>
<span id="LID149" rel="#L149">149</span>
<span id="LID150" rel="#L150">150</span>
<span id="LID151" rel="#L151">151</span>
<span id="LID152" rel="#L152">152</span>
<span id="LID153" rel="#L153">153</span>
<span id="LID154" rel="#L154">154</span>
<span id="LID155" rel="#L155">155</span>
<span id="LID156" rel="#L156">156</span>
<span id="LID157" rel="#L157">157</span>
<span id="LID158" rel="#L158">158</span>
<span id="LID159" rel="#L159">159</span>
<span id="LID160" rel="#L160">160</span>
<span id="LID161" rel="#L161">161</span>
<span id="LID162" rel="#L162">162</span>
<span id="LID163" rel="#L163">163</span>
<span id="LID164" rel="#L164">164</span>
<span id="LID165" rel="#L165">165</span>
<span id="LID166" rel="#L166">166</span>
<span id="LID167" rel="#L167">167</span>
<span id="LID168" rel="#L168">168</span>
<span id="LID169" rel="#L169">169</span>
<span id="LID170" rel="#L170">170</span>
<span id="LID171" rel="#L171">171</span>
<span id="LID172" rel="#L172">172</span>
<span id="LID173" rel="#L173">173</span>
<span id="LID174" rel="#L174">174</span>
<span id="LID175" rel="#L175">175</span>
<span id="LID176" rel="#L176">176</span>
<span id="LID177" rel="#L177">177</span>
<span id="LID178" rel="#L178">178</span>
<span id="LID179" rel="#L179">179</span>
<span id="LID180" rel="#L180">180</span>
<span id="LID181" rel="#L181">181</span>
<span id="LID182" rel="#L182">182</span>
<span id="LID183" rel="#L183">183</span>
<span id="LID184" rel="#L184">184</span>
<span id="LID185" rel="#L185">185</span>
<span id="LID186" rel="#L186">186</span>
<span id="LID187" rel="#L187">187</span>
<span id="LID188" rel="#L188">188</span>
<span id="LID189" rel="#L189">189</span>
<span id="LID190" rel="#L190">190</span>
<span id="LID191" rel="#L191">191</span>
<span id="LID192" rel="#L192">192</span>
<span id="LID193" rel="#L193">193</span>
<span id="LID194" rel="#L194">194</span>
<span id="LID195" rel="#L195">195</span>
<span id="LID196" rel="#L196">196</span>
<span id="LID197" rel="#L197">197</span>
<span id="LID198" rel="#L198">198</span>
<span id="LID199" rel="#L199">199</span>
<span id="LID200" rel="#L200">200</span>
<span id="LID201" rel="#L201">201</span>
<span id="LID202" rel="#L202">202</span>
<span id="LID203" rel="#L203">203</span>
<span id="LID204" rel="#L204">204</span>
<span id="LID205" rel="#L205">205</span>
<span id="LID206" rel="#L206">206</span>
<span id="LID207" rel="#L207">207</span>
<span id="LID208" rel="#L208">208</span>
<span id="LID209" rel="#L209">209</span>
<span id="LID210" rel="#L210">210</span>
<span id="LID211" rel="#L211">211</span>
<span id="LID212" rel="#L212">212</span>
<span id="LID213" rel="#L213">213</span>
<span id="LID214" rel="#L214">214</span>
<span id="LID215" rel="#L215">215</span>
<span id="LID216" rel="#L216">216</span>
<span id="LID217" rel="#L217">217</span>
<span id="LID218" rel="#L218">218</span>
<span id="LID219" rel="#L219">219</span>
<span id="LID220" rel="#L220">220</span>
<span id="LID221" rel="#L221">221</span>
<span id="LID222" rel="#L222">222</span>
<span id="LID223" rel="#L223">223</span>
<span id="LID224" rel="#L224">224</span>
<span id="LID225" rel="#L225">225</span>
<span id="LID226" rel="#L226">226</span>
<span id="LID227" rel="#L227">227</span>
<span id="LID228" rel="#L228">228</span>
<span id="LID229" rel="#L229">229</span>
<span id="LID230" rel="#L230">230</span>
<span id="LID231" rel="#L231">231</span>
<span id="LID232" rel="#L232">232</span>
<span id="LID233" rel="#L233">233</span>
<span id="LID234" rel="#L234">234</span>
<span id="LID235" rel="#L235">235</span>
<span id="LID236" rel="#L236">236</span>
<span id="LID237" rel="#L237">237</span>
<span id="LID238" rel="#L238">238</span>
<span id="LID239" rel="#L239">239</span>
<span id="LID240" rel="#L240">240</span>
<span id="LID241" rel="#L241">241</span>
<span id="LID242" rel="#L242">242</span>
<span id="LID243" rel="#L243">243</span>
<span id="LID244" rel="#L244">244</span>
<span id="LID245" rel="#L245">245</span>
<span id="LID246" rel="#L246">246</span>
<span id="LID247" rel="#L247">247</span>
<span id="LID248" rel="#L248">248</span>
<span id="LID249" rel="#L249">249</span>
<span id="LID250" rel="#L250">250</span>
<span id="LID251" rel="#L251">251</span>
<span id="LID252" rel="#L252">252</span>
<span id="LID253" rel="#L253">253</span>
<span id="LID254" rel="#L254">254</span>
<span id="LID255" rel="#L255">255</span>
<span id="LID256" rel="#L256">256</span>
<span id="LID257" rel="#L257">257</span>
<span id="LID258" rel="#L258">258</span>
<span id="LID259" rel="#L259">259</span>
<span id="LID260" rel="#L260">260</span>
<span id="LID261" rel="#L261">261</span>
<span id="LID262" rel="#L262">262</span>
<span id="LID263" rel="#L263">263</span>
<span id="LID264" rel="#L264">264</span>
<span id="LID265" rel="#L265">265</span>
<span id="LID266" rel="#L266">266</span>
<span id="LID267" rel="#L267">267</span>
<span id="LID268" rel="#L268">268</span>
<span id="LID269" rel="#L269">269</span>
<span id="LID270" rel="#L270">270</span>
<span id="LID271" rel="#L271">271</span>
<span id="LID272" rel="#L272">272</span>
<span id="LID273" rel="#L273">273</span>
<span id="LID274" rel="#L274">274</span>
<span id="LID275" rel="#L275">275</span>
<span id="LID276" rel="#L276">276</span>
<span id="LID277" rel="#L277">277</span>
<span id="LID278" rel="#L278">278</span>
<span id="LID279" rel="#L279">279</span>
<span id="LID280" rel="#L280">280</span>
<span id="LID281" rel="#L281">281</span>
<span id="LID282" rel="#L282">282</span>
<span id="LID283" rel="#L283">283</span>
<span id="LID284" rel="#L284">284</span>
<span id="LID285" rel="#L285">285</span>
<span id="LID286" rel="#L286">286</span>
<span id="LID287" rel="#L287">287</span>
<span id="LID288" rel="#L288">288</span>
<span id="LID289" rel="#L289">289</span>
<span id="LID290" rel="#L290">290</span>
<span id="LID291" rel="#L291">291</span>
<span id="LID292" rel="#L292">292</span>
<span id="LID293" rel="#L293">293</span>
<span id="LID294" rel="#L294">294</span>
<span id="LID295" rel="#L295">295</span>
<span id="LID296" rel="#L296">296</span>
<span id="LID297" rel="#L297">297</span>
<span id="LID298" rel="#L298">298</span>
<span id="LID299" rel="#L299">299</span>
<span id="LID300" rel="#L300">300</span>
<span id="LID301" rel="#L301">301</span>
<span id="LID302" rel="#L302">302</span>
<span id="LID303" rel="#L303">303</span>
<span id="LID304" rel="#L304">304</span>
<span id="LID305" rel="#L305">305</span>
<span id="LID306" rel="#L306">306</span>
<span id="LID307" rel="#L307">307</span>
<span id="LID308" rel="#L308">308</span>
<span id="LID309" rel="#L309">309</span>
<span id="LID310" rel="#L310">310</span>
<span id="LID311" rel="#L311">311</span>
<span id="LID312" rel="#L312">312</span>
<span id="LID313" rel="#L313">313</span>
<span id="LID314" rel="#L314">314</span>
<span id="LID315" rel="#L315">315</span>
<span id="LID316" rel="#L316">316</span>
<span id="LID317" rel="#L317">317</span>
<span id="LID318" rel="#L318">318</span>
<span id="LID319" rel="#L319">319</span>
<span id="LID320" rel="#L320">320</span>
<span id="LID321" rel="#L321">321</span>
<span id="LID322" rel="#L322">322</span>
<span id="LID323" rel="#L323">323</span>
<span id="LID324" rel="#L324">324</span>
<span id="LID325" rel="#L325">325</span>
<span id="LID326" rel="#L326">326</span>
<span id="LID327" rel="#L327">327</span>
<span id="LID328" rel="#L328">328</span>
<span id="LID329" rel="#L329">329</span>
<span id="LID330" rel="#L330">330</span>
<span id="LID331" rel="#L331">331</span>
<span id="LID332" rel="#L332">332</span>
<span id="LID333" rel="#L333">333</span>
<span id="LID334" rel="#L334">334</span>
<span id="LID335" rel="#L335">335</span>
<span id="LID336" rel="#L336">336</span>
<span id="LID337" rel="#L337">337</span>
<span id="LID338" rel="#L338">338</span>
<span id="LID339" rel="#L339">339</span>
<span id="LID340" rel="#L340">340</span>
<span id="LID341" rel="#L341">341</span>
<span id="LID342" rel="#L342">342</span>
<span id="LID343" rel="#L343">343</span>
<span id="LID344" rel="#L344">344</span>
<span id="LID345" rel="#L345">345</span>
<span id="LID346" rel="#L346">346</span>
<span id="LID347" rel="#L347">347</span>
<span id="LID348" rel="#L348">348</span>
<span id="LID349" rel="#L349">349</span>
<span id="LID350" rel="#L350">350</span>
<span id="LID351" rel="#L351">351</span>
<span id="LID352" rel="#L352">352</span>
<span id="LID353" rel="#L353">353</span>
<span id="LID354" rel="#L354">354</span>
<span id="LID355" rel="#L355">355</span>
<span id="LID356" rel="#L356">356</span>
<span id="LID357" rel="#L357">357</span>
<span id="LID358" rel="#L358">358</span>
<span id="LID359" rel="#L359">359</span>
<span id="LID360" rel="#L360">360</span>
<span id="LID361" rel="#L361">361</span>
<span id="LID362" rel="#L362">362</span>
<span id="LID363" rel="#L363">363</span>
<span id="LID364" rel="#L364">364</span>
<span id="LID365" rel="#L365">365</span>
<span id="LID366" rel="#L366">366</span>
<span id="LID367" rel="#L367">367</span>
<span id="LID368" rel="#L368">368</span>
<span id="LID369" rel="#L369">369</span>
<span id="LID370" rel="#L370">370</span>
<span id="LID371" rel="#L371">371</span>
<span id="LID372" rel="#L372">372</span>
<span id="LID373" rel="#L373">373</span>
<span id="LID374" rel="#L374">374</span>
<span id="LID375" rel="#L375">375</span>
<span id="LID376" rel="#L376">376</span>
<span id="LID377" rel="#L377">377</span>
<span id="LID378" rel="#L378">378</span>
<span id="LID379" rel="#L379">379</span>
<span id="LID380" rel="#L380">380</span>
<span id="LID381" rel="#L381">381</span>
<span id="LID382" rel="#L382">382</span>
<span id="LID383" rel="#L383">383</span>
<span id="LID384" rel="#L384">384</span>
<span id="LID385" rel="#L385">385</span>
<span id="LID386" rel="#L386">386</span>
<span id="LID387" rel="#L387">387</span>
<span id="LID388" rel="#L388">388</span>
<span id="LID389" rel="#L389">389</span>
<span id="LID390" rel="#L390">390</span>
<span id="LID391" rel="#L391">391</span>
<span id="LID392" rel="#L392">392</span>
<span id="LID393" rel="#L393">393</span>
<span id="LID394" rel="#L394">394</span>
<span id="LID395" rel="#L395">395</span>
<span id="LID396" rel="#L396">396</span>
<span id="LID397" rel="#L397">397</span>
<span id="LID398" rel="#L398">398</span>
<span id="LID399" rel="#L399">399</span>
<span id="LID400" rel="#L400">400</span>
<span id="LID401" rel="#L401">401</span>
<span id="LID402" rel="#L402">402</span>
<span id="LID403" rel="#L403">403</span>
<span id="LID404" rel="#L404">404</span>
<span id="LID405" rel="#L405">405</span>
<span id="LID406" rel="#L406">406</span>
<span id="LID407" rel="#L407">407</span>
<span id="LID408" rel="#L408">408</span>
<span id="LID409" rel="#L409">409</span>
<span id="LID410" rel="#L410">410</span>
<span id="LID411" rel="#L411">411</span>
<span id="LID412" rel="#L412">412</span>
<span id="LID413" rel="#L413">413</span>
<span id="LID414" rel="#L414">414</span>
<span id="LID415" rel="#L415">415</span>
<span id="LID416" rel="#L416">416</span>
<span id="LID417" rel="#L417">417</span>
<span id="LID418" rel="#L418">418</span>
<span id="LID419" rel="#L419">419</span>
<span id="LID420" rel="#L420">420</span>
<span id="LID421" rel="#L421">421</span>
<span id="LID422" rel="#L422">422</span>
<span id="LID423" rel="#L423">423</span>
<span id="LID424" rel="#L424">424</span>
<span id="LID425" rel="#L425">425</span>
<span id="LID426" rel="#L426">426</span>
<span id="LID427" rel="#L427">427</span>
<span id="LID428" rel="#L428">428</span>
<span id="LID429" rel="#L429">429</span>
<span id="LID430" rel="#L430">430</span>
<span id="LID431" rel="#L431">431</span>
<span id="LID432" rel="#L432">432</span>
<span id="LID433" rel="#L433">433</span>
<span id="LID434" rel="#L434">434</span>
<span id="LID435" rel="#L435">435</span>
<span id="LID436" rel="#L436">436</span>
<span id="LID437" rel="#L437">437</span>
<span id="LID438" rel="#L438">438</span>
<span id="LID439" rel="#L439">439</span>
<span id="LID440" rel="#L440">440</span>
<span id="LID441" rel="#L441">441</span>
<span id="LID442" rel="#L442">442</span>
<span id="LID443" rel="#L443">443</span>
<span id="LID444" rel="#L444">444</span>
<span id="LID445" rel="#L445">445</span>
<span id="LID446" rel="#L446">446</span>
<span id="LID447" rel="#L447">447</span>
<span id="LID448" rel="#L448">448</span>
<span id="LID449" rel="#L449">449</span>
<span id="LID450" rel="#L450">450</span>
<span id="LID451" rel="#L451">451</span>
<span id="LID452" rel="#L452">452</span>
<span id="LID453" rel="#L453">453</span>
<span id="LID454" rel="#L454">454</span>
<span id="LID455" rel="#L455">455</span>
<span id="LID456" rel="#L456">456</span>
<span id="LID457" rel="#L457">457</span>
<span id="LID458" rel="#L458">458</span>
<span id="LID459" rel="#L459">459</span>
<span id="LID460" rel="#L460">460</span>
<span id="LID461" rel="#L461">461</span>
<span id="LID462" rel="#L462">462</span>
<span id="LID463" rel="#L463">463</span>
<span id="LID464" rel="#L464">464</span>
<span id="LID465" rel="#L465">465</span>
<span id="LID466" rel="#L466">466</span>
<span id="LID467" rel="#L467">467</span>
<span id="LID468" rel="#L468">468</span>
<span id="LID469" rel="#L469">469</span>
<span id="LID470" rel="#L470">470</span>
<span id="LID471" rel="#L471">471</span>
<span id="LID472" rel="#L472">472</span>
<span id="LID473" rel="#L473">473</span>
<span id="LID474" rel="#L474">474</span>
<span id="LID475" rel="#L475">475</span>
<span id="LID476" rel="#L476">476</span>
<span id="LID477" rel="#L477">477</span>
<span id="LID478" rel="#L478">478</span>
<span id="LID479" rel="#L479">479</span>
<span id="LID480" rel="#L480">480</span>
<span id="LID481" rel="#L481">481</span>
<span id="LID482" rel="#L482">482</span>
<span id="LID483" rel="#L483">483</span>
<span id="LID484" rel="#L484">484</span>
<span id="LID485" rel="#L485">485</span>
<span id="LID486" rel="#L486">486</span>
<span id="LID487" rel="#L487">487</span>
<span id="LID488" rel="#L488">488</span>
<span id="LID489" rel="#L489">489</span>
<span id="LID490" rel="#L490">490</span>
<span id="LID491" rel="#L491">491</span>
<span id="LID492" rel="#L492">492</span>
<span id="LID493" rel="#L493">493</span>
<span id="LID494" rel="#L494">494</span>
<span id="LID495" rel="#L495">495</span>
<span id="LID496" rel="#L496">496</span>
<span id="LID497" rel="#L497">497</span>
<span id="LID498" rel="#L498">498</span>
<span id="LID499" rel="#L499">499</span>
<span id="LID500" rel="#L500">500</span>
<span id="LID501" rel="#L501">501</span>
<span id="LID502" rel="#L502">502</span>
<span id="LID503" rel="#L503">503</span>
<span id="LID504" rel="#L504">504</span>
<span id="LID505" rel="#L505">505</span>
<span id="LID506" rel="#L506">506</span>
<span id="LID507" rel="#L507">507</span>
<span id="LID508" rel="#L508">508</span>
<span id="LID509" rel="#L509">509</span>
<span id="LID510" rel="#L510">510</span>
<span id="LID511" rel="#L511">511</span>
<span id="LID512" rel="#L512">512</span>
<span id="LID513" rel="#L513">513</span>
<span id="LID514" rel="#L514">514</span>
</pre>
          </td>
          <td width="100%">
            
              
                <div class="highlight"><pre><div class='line' id='LC1'><span class="cm">/*  Spinners 1.0</span></div><div class='line' id='LC2'><span class="cm"> *  (c) 2010 Nick Stakenburg - http://www.nickstakenburg.com</span></div><div class='line' id='LC3'><span class="cm"> *</span></div><div class='line' id='LC4'><span class="cm"> *  Spinners is freely distributable under the terms of an MIT-style license.</span></div><div class='line' id='LC5'><span class="cm"> *</span></div><div class='line' id='LC6'><span class="cm"> *  Works with your framework of choice using BridgeJS:</span></div><div class='line' id='LC7'><span class="cm"> *  http://www.github.com/staaky/bridgejs</span></div><div class='line' id='LC8'><span class="cm"> *</span></div><div class='line' id='LC9'><span class="cm"> *  Requires ExplorerCanvas to work in Internet Explorer:</span></div><div class='line' id='LC10'><span class="cm"> *  http://code.google.com/p/explorercanvas</span></div><div class='line' id='LC11'><span class="cm"> */</span></div><div class='line' id='LC12'><br/></div><div class='line' id='LC13'><span class="kd">var</span> <span class="nx">Spinners</span> <span class="o">=</span> <span class="p">{</span></div><div class='line' id='LC14'>&nbsp;&nbsp;<span class="nx">Version</span><span class="o">:</span> <span class="s1">&#39;1.0&#39;</span></div><div class='line' id='LC15'><span class="p">};</span></div><div class='line' id='LC16'><br/></div><div class='line' id='LC17'><span class="p">(</span><span class="kd">function</span><span class="p">(</span><span class="nx">$B</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC18'><span class="nx">$B</span><span class="p">.</span><span class="nb">Object</span><span class="p">.</span><span class="nx">extend</span><span class="p">(</span><span class="nx">Spinners</span><span class="p">,</span> <span class="p">{</span></div><div class='line' id='LC19'>&nbsp;&nbsp;<span class="nx">spinners</span><span class="o">:</span> <span class="p">[],</span></div><div class='line' id='LC20'><br/></div><div class='line' id='LC21'>&nbsp;&nbsp;<span class="nx">Required</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC22'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">Bridge</span><span class="o">:</span> <span class="s1">&#39;0.2.0&#39;</span></div><div class='line' id='LC23'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC24'><br/></div><div class='line' id='LC25'>&nbsp;&nbsp;<span class="nx">support</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC26'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">canvas</span><span class="o">:</span> <span class="o">!!</span><span class="nb">document</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="s1">&#39;canvas&#39;</span><span class="p">).</span><span class="nx">getContext</span></div><div class='line' id='LC27'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC28'>&nbsp;&nbsp;</div><div class='line' id='LC29'>&nbsp;&nbsp;<span class="nx">insertScript</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">source</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC30'>	<span class="k">try</span> <span class="p">{</span></div><div class='line' id='LC31'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nb">document</span><span class="p">.</span><span class="nx">write</span><span class="p">(</span><span class="s2">"&lt;script type=&#39;text/javascript&#39; src=&#39;"</span> <span class="o">+</span> <span class="nx">source</span> <span class="o">+</span> <span class="s2">"&#39;&gt;&lt;\/script&gt;"</span><span class="p">);</span></div><div class='line' id='LC32'>	<span class="p">}</span> <span class="k">catch</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC33'>	  <span class="nx">Bridge</span><span class="p">.</span><span class="nx">$$</span><span class="p">(</span><span class="s1">&#39;head&#39;</span><span class="p">).</span><span class="nx">source</span><span class="p">[</span><span class="mi">0</span><span class="p">].</span><span class="nx">appendChild</span><span class="p">(</span><span class="k">new</span> <span class="nx">Bridge</span><span class="p">.</span><span class="nx">Element</span><span class="p">(</span><span class="s1">&#39;script&#39;</span><span class="p">,</span> <span class="p">{</span></div><div class='line' id='LC34'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">src</span><span class="o">:</span> <span class="nx">source</span><span class="p">,</span></div><div class='line' id='LC35'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">type</span><span class="o">:</span> <span class="s1">&#39;text/javascript&#39;</span></div><div class='line' id='LC36'>	  <span class="p">}));</span></div><div class='line' id='LC37'>	<span class="p">}</span></div><div class='line' id='LC38'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC39'>&nbsp;&nbsp;</div><div class='line' id='LC40'>&nbsp;&nbsp;<span class="nx">require</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">library</span><span class="p">,</span> <span class="nx">name</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC41'>	  <span class="k">if</span> <span class="p">((</span><span class="k">typeof</span> <span class="nb">window</span><span class="p">[</span><span class="nx">library</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;undefined&#39;</span><span class="p">)</span> <span class="o">||</span></div><div class='line' id='LC42'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">convertVersionString</span><span class="p">(</span><span class="nb">window</span><span class="p">[</span><span class="nx">library</span><span class="p">].</span><span class="nx">Version</span><span class="p">)</span> <span class="o">&lt;</span></div><div class='line' id='LC43'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">convertVersionString</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">Required</span><span class="p">[</span><span class="nx">library</span><span class="p">])))</span></div><div class='line' id='LC44'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">throw</span><span class="p">(</span><span class="s1">&#39;Spinners requires &#39;</span> <span class="o">+</span> <span class="p">(</span><span class="nx">name</span> <span class="o">||</span> <span class="nx">library</span><span class="p">)</span> <span class="o">+</span> <span class="s1">&#39; &gt;= &#39;</span> <span class="o">+</span> <span class="k">this</span><span class="p">.</span><span class="nx">Required</span><span class="p">[</span><span class="nx">library</span><span class="p">]);</span></div><div class='line' id='LC45'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC46'><br/></div><div class='line' id='LC47'>&nbsp;&nbsp;<span class="nx">convertVersionString</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">versionString</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC48'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">v</span> <span class="o">=</span> <span class="nx">versionString</span><span class="p">.</span><span class="nx">replace</span><span class="p">(</span><span class="sr">/_.*|\./g</span><span class="p">,</span> <span class="s1">&#39;&#39;</span><span class="p">);</span></div><div class='line' id='LC49'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">v</span> <span class="o">=</span> <span class="nb">parseInt</span><span class="p">(</span><span class="nx">v</span> <span class="o">+</span> <span class="nx">Bridge</span><span class="p">.</span><span class="nb">String</span><span class="p">.</span><span class="nx">times</span><span class="p">(</span><span class="s1">&#39;0&#39;</span><span class="p">,</span> <span class="mi">4</span> <span class="o">-</span> <span class="nx">v</span><span class="p">.</span><span class="nx">length</span><span class="p">));</span></div><div class='line' id='LC50'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">versionString</span><span class="p">.</span><span class="nx">indexOf</span><span class="p">(</span><span class="s1">&#39;_&#39;</span><span class="p">)</span> <span class="o">&gt;</span> <span class="o">-</span><span class="mi">1</span> <span class="o">?</span> <span class="nx">v</span> <span class="o">-</span> <span class="mi">1</span> <span class="o">:</span> <span class="nx">v</span><span class="p">;</span></div><div class='line' id='LC51'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC52'>&nbsp;&nbsp;</div><div class='line' id='LC53'>&nbsp;&nbsp;<span class="nx">start</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC54'>	<span class="k">this</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="s1">&#39;Bridge&#39;</span><span class="p">);</span></div><div class='line' id='LC55'><br/></div><div class='line' id='LC56'>	<span class="c1">// require excanvas</span></div><div class='line' id='LC57'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="k">this</span><span class="p">.</span><span class="nx">support</span><span class="p">.</span><span class="nx">canvas</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="nb">window</span><span class="p">.</span><span class="nx">G_vmlCanvasManager</span><span class="p">)</span></div><div class='line' id='LC58'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">throw</span><span class="p">(</span><span class="s1">&#39;Spinners requires ExplorerCanvas&#39;</span><span class="p">);</span></div><div class='line' id='LC59'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC60'><br/></div><div class='line' id='LC61'>&nbsp;&nbsp;<span class="nx">get</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">element</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC62'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">element</span> <span class="o">=</span> <span class="nx">$B</span><span class="p">.</span><span class="nx">$</span><span class="p">(</span><span class="nx">element</span><span class="p">).</span><span class="nx">source</span><span class="p">;</span></div><div class='line' id='LC63'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">element</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span></div><div class='line' id='LC64'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">matched</span> <span class="o">=</span> <span class="kc">null</span><span class="p">;</span></div><div class='line' id='LC65'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">$B</span><span class="p">.</span><span class="nx">_each</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">spinners</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">spinner</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC66'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">spinner</span><span class="p">.</span><span class="nx">element</span> <span class="o">==</span> <span class="nx">element</span><span class="p">)</span></div><div class='line' id='LC67'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">matched</span> <span class="o">=</span> <span class="nx">spinner</span><span class="p">;</span></div><div class='line' id='LC68'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">});</span></div><div class='line' id='LC69'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">matched</span><span class="p">;</span>    </div><div class='line' id='LC70'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC71'><br/></div><div class='line' id='LC72'>&nbsp;&nbsp;<span class="nx">add</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">spinner</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC73'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">spinners</span><span class="p">.</span><span class="nx">push</span><span class="p">(</span><span class="nx">spinner</span><span class="p">);</span>  </div><div class='line' id='LC74'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC75'>&nbsp;&nbsp;</div><div class='line' id='LC76'>&nbsp;&nbsp;<span class="nx">remove</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">element</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC77'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">spinner</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">get</span><span class="p">(</span><span class="nx">element</span><span class="p">);</span></div><div class='line' id='LC78'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nx">spinner</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC79'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">spinner</span><span class="p">.</span><span class="nx">remove</span><span class="p">();</span></div><div class='line' id='LC80'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">spinners</span> <span class="o">=</span> <span class="nx">$B</span><span class="p">.</span><span class="nb">Array</span><span class="p">.</span><span class="nx">without</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">spinners</span><span class="p">,</span> <span class="nx">spinner</span><span class="p">);</span></div><div class='line' id='LC81'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC82'>&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC83'>&nbsp;&nbsp;</div><div class='line' id='LC84'>&nbsp;&nbsp;<span class="c1">// remove all spinners that are not attached to the DOM</span></div><div class='line' id='LC85'>&nbsp;&nbsp;<span class="nx">removeDetached</span><span class="o">:</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC86'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">$B</span><span class="p">.</span><span class="nx">each</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">spinners</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">spinner</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC87'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span> <span class="p">{</span></div><div class='line' id='LC88'>&nbsp;&nbsp;&nbsp;&nbsp;	<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">spinner</span><span class="p">.</span><span class="nx">element</span><span class="p">.</span><span class="nx">offsetParent</span><span class="p">)</span></div><div class='line' id='LC89'>&nbsp;&nbsp;&nbsp;&nbsp;	  <span class="k">this</span><span class="p">.</span><span class="nx">remove</span><span class="p">(</span><span class="nx">spinner</span><span class="p">.</span><span class="nx">element</span><span class="p">);</span>  </div><div class='line' id='LC90'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span> <span class="k">catch</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC91'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">remove</span><span class="p">(</span><span class="nx">spinner</span><span class="p">.</span><span class="nx">element</span><span class="p">);</span></div><div class='line' id='LC92'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC93'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span> <span class="k">this</span><span class="p">);</span></div><div class='line' id='LC94'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC95'><span class="p">});</span></div><div class='line' id='LC96'><br/></div><div class='line' id='LC97'><br/></div><div class='line' id='LC98'><br/></div><div class='line' id='LC99'><span class="cm">/*</span></div><div class='line' id='LC100'><span class="cm"> * Math</span></div><div class='line' id='LC101'><span class="cm"> */</span></div><div class='line' id='LC102'><span class="kd">function</span> <span class="nx">pyth</span><span class="p">(</span><span class="nx">a</span><span class="p">,</span><span class="nx">b</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC103'>&nbsp;&nbsp;<span class="k">return</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">sqrt</span><span class="p">(</span><span class="nx">a</span><span class="o">*</span><span class="nx">a</span> <span class="o">+</span> <span class="nx">b</span><span class="o">*</span><span class="nx">b</span><span class="p">);</span></div><div class='line' id='LC104'><span class="p">}</span></div><div class='line' id='LC105'><br/></div><div class='line' id='LC106'><span class="kd">function</span> <span class="nx">degrees</span><span class="p">(</span><span class="nx">radian</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC107'>&nbsp;&nbsp;<span class="k">return</span> <span class="p">(</span><span class="nx">radian</span><span class="o">*</span><span class="mi">180</span><span class="p">)</span> <span class="o">/</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">PI</span><span class="p">;</span></div><div class='line' id='LC108'><span class="p">}</span></div><div class='line' id='LC109'><br/></div><div class='line' id='LC110'><span class="kd">function</span> <span class="nx">radian</span><span class="p">(</span><span class="nx">degrees</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC111'>&nbsp;&nbsp;<span class="k">return</span> <span class="p">(</span><span class="nx">degrees</span><span class="o">*</span><span class="nb">Math</span><span class="p">.</span><span class="nx">PI</span><span class="p">)</span> <span class="o">/</span> <span class="mi">180</span><span class="p">;</span></div><div class='line' id='LC112'><span class="p">}</span></div><div class='line' id='LC113'><br/></div><div class='line' id='LC114'><span class="kd">function</span> <span class="nx">scrollArray</span><span class="p">(</span><span class="nx">array</span><span class="p">,</span> <span class="nx">distance</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC115'>&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">distance</span><span class="p">)</span> <span class="k">return</span> <span class="nx">array</span><span class="p">;</span></div><div class='line' id='LC116'>&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">first</span> <span class="o">=</span> <span class="nx">array</span><span class="p">.</span><span class="nx">slice</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="nx">distance</span><span class="p">),</span></div><div class='line' id='LC117'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">last</span>  <span class="o">=</span> <span class="nx">array</span><span class="p">.</span><span class="nx">slice</span><span class="p">(</span><span class="nx">distance</span><span class="p">,</span> <span class="nx">array</span><span class="p">.</span><span class="nx">length</span><span class="p">);</span></div><div class='line' id='LC118'>&nbsp;&nbsp;<span class="k">return</span> <span class="nx">last</span><span class="p">.</span><span class="nx">concat</span><span class="p">(</span><span class="nx">first</span><span class="p">);</span></div><div class='line' id='LC119'><span class="p">}</span></div><div class='line' id='LC120'><br/></div><div class='line' id='LC121'><span class="cm">/*</span></div><div class='line' id='LC122'><span class="cm"> * Helpers</span></div><div class='line' id='LC123'><span class="cm"> */</span></div><div class='line' id='LC124'><span class="kd">var</span> <span class="nx">Canvas</span> <span class="o">=</span> <span class="p">{</span></div><div class='line' id='LC125'>&nbsp;&nbsp;<span class="nx">drawRoundedRectangle</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">ctx</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC126'>	<span class="kd">var</span> <span class="nx">options</span> <span class="o">=</span> <span class="nx">$B</span><span class="p">.</span><span class="nb">Object</span><span class="p">.</span><span class="nx">extend</span><span class="p">({</span></div><div class='line' id='LC127'>	  <span class="nx">top</span><span class="o">:</span>          <span class="mi">0</span><span class="p">,</span></div><div class='line' id='LC128'>	  <span class="nx">left</span><span class="o">:</span>         <span class="mi">0</span><span class="p">,</span></div><div class='line' id='LC129'>	  <span class="nx">width</span><span class="o">:</span>        <span class="mi">0</span><span class="p">,</span></div><div class='line' id='LC130'>	  <span class="nx">height</span><span class="o">:</span>       <span class="mi">0</span><span class="p">,</span></div><div class='line' id='LC131'>	  <span class="nx">radius</span><span class="o">:</span>       <span class="mi">0</span></div><div class='line' id='LC132'>	<span class="p">},</span> <span class="nx">arguments</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">||</span> <span class="p">{});</span></div><div class='line' id='LC133'><br/></div><div class='line' id='LC134'>	<span class="kd">var</span> <span class="nx">o</span>      <span class="o">=</span> <span class="nx">options</span><span class="p">,</span></div><div class='line' id='LC135'>	    <span class="nx">left</span>   <span class="o">=</span> <span class="nx">o</span><span class="p">.</span><span class="nx">left</span><span class="p">,</span></div><div class='line' id='LC136'>		<span class="nx">top</span>    <span class="o">=</span> <span class="nx">o</span><span class="p">.</span><span class="nx">top</span><span class="p">,</span></div><div class='line' id='LC137'>		<span class="nx">width</span>  <span class="o">=</span> <span class="nx">o</span><span class="p">.</span><span class="nx">width</span><span class="p">,</span></div><div class='line' id='LC138'>		<span class="nx">height</span> <span class="o">=</span> <span class="nx">o</span><span class="p">.</span><span class="nx">height</span><span class="p">,</span></div><div class='line' id='LC139'>		<span class="nx">radius</span> <span class="o">=</span> <span class="nx">o</span><span class="p">.</span><span class="nx">radius</span><span class="p">;</span></div><div class='line' id='LC140'><br/></div><div class='line' id='LC141'>	<span class="nx">ctx</span><span class="p">.</span><span class="nx">beginPath</span><span class="p">();</span></div><div class='line' id='LC142'><br/></div><div class='line' id='LC143'>	<span class="nx">ctx</span><span class="p">.</span><span class="nx">moveTo</span><span class="p">(</span><span class="nx">left</span> <span class="o">+</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">top</span><span class="p">);</span></div><div class='line' id='LC144'>	<span class="nx">ctx</span><span class="p">.</span><span class="nx">arc</span><span class="p">(</span><span class="nx">left</span> <span class="o">+</span> <span class="nx">width</span> <span class="o">-</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">top</span> <span class="o">+</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">radian</span><span class="p">(</span><span class="o">-</span><span class="mi">90</span><span class="p">),</span> <span class="nx">radian</span><span class="p">(</span><span class="mi">0</span><span class="p">),</span> <span class="kc">false</span><span class="p">);</span></div><div class='line' id='LC145'>	<span class="nx">ctx</span><span class="p">.</span><span class="nx">arc</span><span class="p">(</span><span class="nx">left</span> <span class="o">+</span> <span class="nx">width</span> <span class="o">-</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">top</span> <span class="o">+</span> <span class="nx">height</span> <span class="o">-</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">radian</span><span class="p">(</span><span class="mi">0</span><span class="p">),</span> <span class="nx">radian</span><span class="p">(</span><span class="mi">90</span><span class="p">),</span> <span class="kc">false</span><span class="p">);</span></div><div class='line' id='LC146'>	<span class="nx">ctx</span><span class="p">.</span><span class="nx">arc</span><span class="p">(</span><span class="nx">left</span> <span class="o">+</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">top</span> <span class="o">+</span> <span class="nx">height</span> <span class="o">-</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">radian</span><span class="p">(</span><span class="mi">90</span><span class="p">),</span> <span class="nx">radian</span><span class="p">(</span><span class="mi">180</span><span class="p">),</span> <span class="kc">false</span><span class="p">);</span></div><div class='line' id='LC147'>	<span class="nx">ctx</span><span class="p">.</span><span class="nx">arc</span><span class="p">(</span><span class="nx">left</span> <span class="o">+</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">top</span> <span class="o">+</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">radius</span><span class="p">,</span> <span class="nx">radian</span><span class="p">(</span><span class="o">-</span><span class="mi">180</span><span class="p">),</span> <span class="nx">radian</span><span class="p">(</span><span class="o">-</span><span class="mi">90</span><span class="p">),</span> <span class="kc">false</span><span class="p">);</span></div><div class='line' id='LC148'><br/></div><div class='line' id='LC149'>	<span class="nx">ctx</span><span class="p">.</span><span class="nx">closePath</span><span class="p">();</span></div><div class='line' id='LC150'><br/></div><div class='line' id='LC151'>	<span class="nx">ctx</span><span class="p">.</span><span class="nx">fill</span><span class="p">();</span></div><div class='line' id='LC152'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC153'><span class="p">};</span></div><div class='line' id='LC154'><br/></div><div class='line' id='LC155'><br/></div><div class='line' id='LC156'><span class="kd">var</span> <span class="nx">Color</span> <span class="o">=</span> <span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC157'>&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">hexNumber</span> <span class="o">=</span> <span class="s1">&#39;0123456789abcdef&#39;</span><span class="p">,</span></div><div class='line' id='LC158'>	  <span class="nx">hexRegExp</span> <span class="o">=</span> <span class="k">new</span> <span class="nb">RegExp</span><span class="p">(</span><span class="s1">&#39;[&#39;</span> <span class="o">+</span> <span class="nx">hexNumber</span> <span class="o">+</span> <span class="s1">&#39;]&#39;</span><span class="p">,</span> <span class="s1">&#39;g&#39;</span><span class="p">);</span></div><div class='line' id='LC159'>&nbsp;&nbsp;</div><div class='line' id='LC160'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">returnRGB</span><span class="p">(</span><span class="nx">rgb</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC161'>	<span class="kd">var</span> <span class="nx">result</span> <span class="o">=</span> <span class="nx">rgb</span><span class="p">;</span></div><div class='line' id='LC162'>	<span class="nx">result</span><span class="p">.</span><span class="nx">red</span> <span class="o">=</span> <span class="nx">rgb</span><span class="p">[</span><span class="mi">0</span><span class="p">];</span></div><div class='line' id='LC163'>	<span class="nx">result</span><span class="p">.</span><span class="nx">green</span> <span class="o">=</span> <span class="nx">rgb</span><span class="p">[</span><span class="mi">1</span><span class="p">];</span></div><div class='line' id='LC164'>	<span class="nx">result</span><span class="p">.</span><span class="nx">blue</span> <span class="o">=</span> <span class="nx">rgb</span><span class="p">[</span><span class="mi">2</span><span class="p">];</span></div><div class='line' id='LC165'>	<span class="k">return</span> <span class="nx">result</span><span class="p">;</span></div><div class='line' id='LC166'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC167'>&nbsp;&nbsp;</div><div class='line' id='LC168'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">h2d</span><span class="p">(</span><span class="nx">h</span><span class="p">)</span> <span class="p">{</span> <span class="k">return</span> <span class="nb">parseInt</span><span class="p">(</span><span class="nx">h</span><span class="p">,</span><span class="mi">16</span><span class="p">);</span> <span class="p">}</span></div><div class='line' id='LC169'><br/></div><div class='line' id='LC170'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">hex2rgb</span><span class="p">(</span><span class="nx">hex</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC171'>	  <span class="kd">var</span> <span class="nx">rgb</span> <span class="o">=</span> <span class="p">[];</span></div><div class='line' id='LC172'><br/></div><div class='line' id='LC173'>	  <span class="k">if</span> <span class="p">(</span><span class="nx">hex</span><span class="p">.</span><span class="nx">indexOf</span><span class="p">(</span><span class="s1">&#39;#&#39;</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span> <span class="nx">hex</span> <span class="o">=</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">substring</span><span class="p">(</span><span class="mi">1</span><span class="p">);</span></div><div class='line' id='LC174'>	  <span class="nx">hex</span> <span class="o">=</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">toLowerCase</span><span class="p">();</span></div><div class='line' id='LC175'><br/></div><div class='line' id='LC176'>	  <span class="k">if</span> <span class="p">(</span><span class="nx">hex</span><span class="p">.</span><span class="nx">replace</span><span class="p">(</span><span class="nx">hexRegExp</span><span class="p">,</span> <span class="s1">&#39;&#39;</span><span class="p">)</span> <span class="o">!=</span> <span class="s1">&#39;&#39;</span><span class="p">)</span></div><div class='line' id='LC177'>		<span class="k">return</span> <span class="kc">null</span><span class="p">;</span></div><div class='line' id='LC178'><br/></div><div class='line' id='LC179'>	  <span class="k">if</span> <span class="p">(</span><span class="nx">hex</span><span class="p">.</span><span class="nx">length</span> <span class="o">==</span> <span class="mi">3</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC180'>		 <span class="nx">rgb</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">charAt</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span> <span class="o">+</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">charAt</span><span class="p">(</span><span class="mi">0</span><span class="p">);</span></div><div class='line' id='LC181'>		 <span class="nx">rgb</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">charAt</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span> <span class="o">+</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">charAt</span><span class="p">(</span><span class="mi">1</span><span class="p">);</span></div><div class='line' id='LC182'>		 <span class="nx">rgb</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span> <span class="o">=</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">charAt</span><span class="p">(</span><span class="mi">2</span><span class="p">)</span> <span class="o">+</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">charAt</span><span class="p">(</span><span class="mi">2</span><span class="p">);</span></div><div class='line' id='LC183'>	  <span class="p">}</span> <span class="k">else</span> <span class="p">{</span></div><div class='line' id='LC184'>		 <span class="nx">rgb</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">substring</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="mi">2</span><span class="p">);</span></div><div class='line' id='LC185'>		 <span class="nx">rgb</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">substring</span><span class="p">(</span><span class="mi">2</span><span class="p">,</span> <span class="mi">4</span><span class="p">);</span></div><div class='line' id='LC186'>		 <span class="nx">rgb</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span> <span class="o">=</span> <span class="nx">hex</span><span class="p">.</span><span class="nx">substring</span><span class="p">(</span><span class="mi">4</span><span class="p">);</span></div><div class='line' id='LC187'>	  <span class="p">}</span></div><div class='line' id='LC188'>	  <span class="k">for</span><span class="p">(</span><span class="kd">var</span> <span class="nx">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="nx">i</span> <span class="o">&lt;</span> <span class="nx">rgb</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span> <span class="nx">i</span><span class="o">++</span><span class="p">)</span></div><div class='line' id='LC189'>		<span class="nx">rgb</span><span class="p">[</span><span class="nx">i</span><span class="p">]</span> <span class="o">=</span> <span class="nx">h2d</span><span class="p">(</span><span class="nx">rgb</span><span class="p">[</span><span class="nx">i</span><span class="p">]);</span></div><div class='line' id='LC190'><br/></div><div class='line' id='LC191'>	  <span class="k">return</span> <span class="nx">returnRGB</span><span class="p">(</span><span class="nx">rgb</span><span class="p">);</span></div><div class='line' id='LC192'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC193'>&nbsp;&nbsp;</div><div class='line' id='LC194'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">hex2rgba</span><span class="p">(</span><span class="nx">hex</span><span class="p">,</span> <span class="nx">opacity</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC195'>	  <span class="kd">var</span> <span class="nx">rgba</span> <span class="o">=</span> <span class="nx">hex2rgb</span><span class="p">(</span><span class="nx">hex</span><span class="p">);</span></div><div class='line' id='LC196'>	  <span class="nx">rgba</span><span class="p">[</span><span class="mi">3</span><span class="p">]</span> <span class="o">=</span> <span class="nx">opacity</span><span class="p">;</span></div><div class='line' id='LC197'>	  <span class="nx">rgba</span><span class="p">.</span><span class="nx">opacity</span> <span class="o">=</span> <span class="nx">opacity</span><span class="p">;</span></div><div class='line' id='LC198'>	  <span class="k">return</span> <span class="nx">rgba</span><span class="p">;</span></div><div class='line' id='LC199'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC200'>&nbsp;&nbsp;</div><div class='line' id='LC201'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">hex2fill</span><span class="p">(</span><span class="nx">hex</span><span class="p">,</span> <span class="nx">opacity</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC202'>	  <span class="k">if</span> <span class="p">(</span><span class="nx">$B</span><span class="p">.</span><span class="nb">Object</span><span class="p">.</span><span class="nx">isUndefined</span><span class="p">(</span><span class="nx">opacity</span><span class="p">))</span> <span class="nx">opacity</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span></div><div class='line' id='LC203'>	  <span class="k">return</span> <span class="s2">"rgba("</span> <span class="o">+</span> <span class="nx">hex2rgba</span><span class="p">(</span><span class="nx">hex</span><span class="p">,</span> <span class="nx">opacity</span><span class="p">).</span><span class="nx">join</span><span class="p">()</span> <span class="o">+</span> <span class="s2">")"</span><span class="p">;</span></div><div class='line' id='LC204'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC205'>&nbsp;&nbsp;</div><div class='line' id='LC206'>&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">rgb2hex</span> <span class="o">=</span> <span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC207'>	<span class="kd">function</span> <span class="nx">toPaddedString</span><span class="p">(</span><span class="nx">string</span><span class="p">,</span> <span class="nx">length</span><span class="p">,</span> <span class="nx">radix</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC208'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">string</span> <span class="o">=</span> <span class="p">(</span><span class="nx">string</span><span class="p">).</span><span class="nx">toString</span><span class="p">(</span><span class="nx">radix</span> <span class="o">||</span> <span class="mi">10</span><span class="p">);</span></div><div class='line' id='LC209'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">$B</span><span class="p">.</span><span class="nb">String</span><span class="p">.</span><span class="nx">times</span><span class="p">(</span><span class="s1">&#39;0&#39;</span><span class="p">,</span> <span class="nx">length</span> <span class="o">-</span> <span class="nx">string</span><span class="p">.</span><span class="nx">length</span><span class="p">)</span> <span class="o">+</span> <span class="nx">string</span><span class="p">;</span></div><div class='line' id='LC210'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC211'><br/></div><div class='line' id='LC212'>	<span class="k">return</span> <span class="kd">function</span><span class="p">(</span><span class="nx">red</span><span class="p">,</span> <span class="nx">green</span><span class="p">,</span> <span class="nx">blue</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC213'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="s1">&#39;#&#39;</span> <span class="o">+</span> <span class="nx">toPaddedString</span><span class="p">(</span><span class="nx">red</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">16</span><span class="p">)</span> <span class="o">+</span></div><div class='line' id='LC214'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">toPaddedString</span><span class="p">(</span><span class="nx">green</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">16</span><span class="p">)</span> <span class="o">+</span></div><div class='line' id='LC215'>				   <span class="nx">toPaddedString</span><span class="p">(</span><span class="nx">blue</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">16</span><span class="p">);</span></div><div class='line' id='LC216'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">};</span></div><div class='line' id='LC217'>&nbsp;&nbsp;<span class="p">})();</span></div><div class='line' id='LC218'><br/></div><div class='line' id='LC219'>&nbsp;&nbsp;<span class="k">return</span> <span class="p">{</span></div><div class='line' id='LC220'>	<span class="nx">hex2rgb</span><span class="o">:</span> <span class="nx">hex2rgb</span><span class="p">,</span></div><div class='line' id='LC221'>	<span class="nx">hex2fill</span><span class="o">:</span> <span class="nx">hex2fill</span><span class="p">,</span></div><div class='line' id='LC222'>	<span class="nx">rgb2hex</span><span class="o">:</span> <span class="nx">rgb2hex</span></div><div class='line' id='LC223'>&nbsp;&nbsp;<span class="p">};</span></div><div class='line' id='LC224'><span class="p">})();</span></div><div class='line' id='LC225'><br/></div><div class='line' id='LC226'><br/></div><div class='line' id='LC227'><span class="cm">/*</span></div><div class='line' id='LC228'><span class="cm"> * Spinner</span></div><div class='line' id='LC229'><span class="cm"> */</span></div><div class='line' id='LC230'><span class="kd">function</span> <span class="nx">Spinner</span><span class="p">(</span><span class="nx">element</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC231'>&nbsp;&nbsp;<span class="nx">element</span> <span class="o">=</span> <span class="nx">$B</span><span class="p">.</span><span class="nx">$</span><span class="p">(</span><span class="nx">element</span><span class="p">);</span></div><div class='line' id='LC232'>&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">element</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span></div><div class='line' id='LC233'><br/></div><div class='line' id='LC234'>&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">element</span> <span class="o">=</span> <span class="nx">element</span><span class="p">.</span><span class="nx">source</span><span class="p">;</span></div><div class='line' id='LC235'><br/></div><div class='line' id='LC236'>&nbsp;&nbsp;<span class="nx">Spinners</span><span class="p">.</span><span class="nx">remove</span><span class="p">(</span><span class="nx">element</span><span class="p">);</span></div><div class='line' id='LC237'>&nbsp;&nbsp;<span class="nx">Spinners</span><span class="p">.</span><span class="nx">removeDetached</span><span class="p">();</span></div><div class='line' id='LC238'><br/></div><div class='line' id='LC239'>&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">options</span> <span class="o">=</span> <span class="nx">$B</span><span class="p">.</span><span class="nb">Object</span><span class="p">.</span><span class="nx">extend</span><span class="p">({</span></div><div class='line' id='LC240'>	<span class="nx">radii</span><span class="o">:</span>     <span class="p">[</span><span class="mi">8</span><span class="p">,</span> <span class="mi">12</span><span class="p">],</span></div><div class='line' id='LC241'>	<span class="nx">dash</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC242'>	  <span class="nx">width</span><span class="o">:</span> <span class="mf">1.5</span><span class="p">,</span></div><div class='line' id='LC243'>&nbsp;&nbsp;	  <span class="nx">color</span><span class="o">:</span> <span class="s1">&#39;#000&#39;</span></div><div class='line' id='LC244'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC245'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">dashes</span><span class="o">:</span>    <span class="mi">24</span><span class="p">,</span></div><div class='line' id='LC246'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">opacity</span><span class="o">:</span>   <span class="mi">1</span><span class="p">,</span></div><div class='line' id='LC247'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">speed</span><span class="o">:</span>     <span class="p">.</span><span class="mi">7</span><span class="p">,</span></div><div class='line' id='LC248'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">build</span><span class="o">:</span>     <span class="kc">true</span></div><div class='line' id='LC249'>&nbsp;&nbsp;<span class="p">},</span> <span class="nx">arguments</span><span class="p">[</span><span class="mi">1</span><span class="p">]);</span></div><div class='line' id='LC250'><br/></div><div class='line' id='LC251'>&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">_position</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span></div><div class='line' id='LC252'>&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">_state</span> <span class="o">=</span> <span class="s1">&#39;stopped&#39;</span><span class="p">;</span></div><div class='line' id='LC253'><br/></div><div class='line' id='LC254'>&nbsp;&nbsp;<span class="c1">// In some cases IE6 doesn&#39;t show a spinner when it&#39;s build</span></div><div class='line' id='LC255'>&nbsp;&nbsp;<span class="c1">// inside a hidden element. This allows you to delay the build</span></div><div class='line' id='LC256'>&nbsp;&nbsp;<span class="c1">// to avoid that</span></div><div class='line' id='LC257'>&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">build</span><span class="p">)</span> <span class="k">this</span><span class="p">.</span><span class="nx">build</span><span class="p">();</span></div><div class='line' id='LC258'><br/></div><div class='line' id='LC259'>&nbsp;&nbsp;<span class="nx">Spinners</span><span class="p">.</span><span class="nx">add</span><span class="p">(</span><span class="k">this</span><span class="p">);</span></div><div class='line' id='LC260'><span class="p">}</span></div><div class='line' id='LC261'><br/></div><div class='line' id='LC262'><span class="nx">$B</span><span class="p">.</span><span class="nb">Object</span><span class="p">.</span><span class="nx">extend</span><span class="p">(</span><span class="nx">Spinner</span><span class="p">.</span><span class="nx">prototype</span><span class="p">,</span> <span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC263'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">remove</span><span class="p">()</span> <span class="p">{</span> </div><div class='line' id='LC264'>	<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="k">this</span><span class="p">.</span><span class="nx">wrapper</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span></div><div class='line' id='LC265'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC266'>	<span class="k">this</span><span class="p">.</span><span class="nx">stop</span><span class="p">();</span></div><div class='line' id='LC267'><br/></div><div class='line' id='LC268'>	<span class="k">this</span><span class="p">.</span><span class="nx">canvas</span><span class="p">.</span><span class="nx">remove</span><span class="p">();</span></div><div class='line' id='LC269'>	<span class="k">this</span><span class="p">.</span><span class="nx">wrapper</span><span class="p">.</span><span class="nx">remove</span><span class="p">();</span></div><div class='line' id='LC270'><br/></div><div class='line' id='LC271'>	<span class="k">this</span><span class="p">.</span><span class="nx">canvas</span> <span class="o">=</span> <span class="kc">null</span><span class="p">;</span></div><div class='line' id='LC272'>	<span class="k">this</span><span class="p">.</span><span class="nx">ctx</span> <span class="o">=</span> <span class="kc">null</span><span class="p">;</span></div><div class='line' id='LC273'>	<span class="k">this</span><span class="p">.</span><span class="nx">wrapper</span> <span class="o">=</span> <span class="kc">null</span><span class="p">;</span></div><div class='line' id='LC274'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC275'>&nbsp;&nbsp;</div><div class='line' id='LC276'>&nbsp;&nbsp;</div><div class='line' id='LC277'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">build</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC278'>	<span class="k">this</span><span class="p">.</span><span class="nx">remove</span><span class="p">();</span></div><div class='line' id='LC279'><br/></div><div class='line' id='LC280'>	<span class="kd">var</span> <span class="nx">layout</span>            <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">getLayout</span><span class="p">(),</span></div><div class='line' id='LC281'>	    <span class="nx">workspaceDiameter</span> <span class="o">=</span> <span class="nx">layout</span><span class="p">.</span><span class="nx">workspace</span><span class="p">.</span><span class="nx">radius</span> <span class="o">*</span> <span class="mi">2</span><span class="p">;</span></div><div class='line' id='LC282'><br/></div><div class='line' id='LC283'>	<span class="nx">$B</span><span class="p">.</span><span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">element</span><span class="p">).</span><span class="nx">insert</span><span class="p">(</span></div><div class='line' id='LC284'>	  <span class="k">this</span><span class="p">.</span><span class="nx">wrapper</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">$B</span><span class="p">.</span><span class="nx">Element</span><span class="p">(</span><span class="s1">&#39;div&#39;</span><span class="p">)</span></div><div class='line' id='LC285'>	  <span class="p">.</span><span class="nx">setStyle</span><span class="p">({</span></div><div class='line' id='LC286'>		<span class="nx">height</span><span class="o">:</span> <span class="nx">workspaceDiameter</span> <span class="o">+</span> <span class="s1">&#39;px&#39;</span><span class="p">,</span></div><div class='line' id='LC287'>	  	<span class="nx">width</span><span class="o">:</span>  <span class="nx">workspaceDiameter</span> <span class="o">+</span> <span class="s1">&#39;px&#39;</span></div><div class='line' id='LC288'>&nbsp;&nbsp;	  <span class="p">})</span></div><div class='line' id='LC289'>	  <span class="p">.</span><span class="nx">insert</span><span class="p">(</span></div><div class='line' id='LC290'>	    <span class="k">this</span><span class="p">.</span><span class="nx">canvas</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">$B</span><span class="p">.</span><span class="nx">Element</span><span class="p">(</span><span class="s1">&#39;canvas&#39;</span><span class="p">,</span> <span class="p">{</span></div><div class='line' id='LC291'>	      <span class="nx">height</span><span class="o">:</span> <span class="nx">workspaceDiameter</span><span class="p">,</span></div><div class='line' id='LC292'>	  	  <span class="nx">width</span><span class="o">:</span>  <span class="nx">workspaceDiameter</span></div><div class='line' id='LC293'>&nbsp;&nbsp;&nbsp;&nbsp;	<span class="p">})</span></div><div class='line' id='LC294'>	  <span class="p">)</span></div><div class='line' id='LC295'>	<span class="p">);</span></div><div class='line' id='LC296'><br/></div><div class='line' id='LC297'>	<span class="c1">// init canvas</span></div><div class='line' id='LC298'>	<span class="k">if</span> <span class="p">(</span><span class="nb">window</span><span class="p">.</span><span class="nx">G_vmlCanvasManager</span><span class="p">)</span></div><div class='line' id='LC299'>	  <span class="nx">G_vmlCanvasManager</span><span class="p">.</span><span class="nx">initElement</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">canvas</span><span class="p">.</span><span class="nx">source</span><span class="p">);</span></div><div class='line' id='LC300'><br/></div><div class='line' id='LC301'>&nbsp;&nbsp;	<span class="k">this</span><span class="p">.</span><span class="nx">ctx</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">canvas</span><span class="p">.</span><span class="nx">source</span><span class="p">.</span><span class="nx">getContext</span><span class="p">(</span><span class="s1">&#39;2d&#39;</span><span class="p">);</span></div><div class='line' id='LC302'>	<span class="k">this</span><span class="p">.</span><span class="nx">ctx</span><span class="p">.</span><span class="nx">globalAlpha</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">opacity</span><span class="p">;</span></div><div class='line' id='LC303'><br/></div><div class='line' id='LC304'>	<span class="kd">var</span> <span class="nx">workspaceRadius</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">getLayout</span><span class="p">().</span><span class="nx">workspace</span><span class="p">.</span><span class="nx">radius</span><span class="p">;</span></div><div class='line' id='LC305'>	<span class="k">this</span><span class="p">.</span><span class="nx">ctx</span><span class="p">.</span><span class="nx">translate</span><span class="p">(</span><span class="nx">workspaceRadius</span><span class="p">,</span> <span class="nx">workspaceRadius</span><span class="p">);</span></div><div class='line' id='LC306'>	<span class="k">this</span><span class="p">.</span><span class="nx">drawPosition</span><span class="p">(</span><span class="mi">0</span><span class="p">);</span></div><div class='line' id='LC307'><br/></div><div class='line' id='LC308'>	<span class="k">return</span> <span class="k">this</span><span class="p">;</span></div><div class='line' id='LC309'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC310'>&nbsp;&nbsp;</div><div class='line' id='LC311'>&nbsp;&nbsp;<span class="cm">/*</span></div><div class='line' id='LC312'><span class="cm">   * Draw</span></div><div class='line' id='LC313'><span class="cm">   */</span></div><div class='line' id='LC314'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">drawPosition</span><span class="p">(</span><span class="nx">position</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC315'>	<span class="kd">var</span> <span class="nx">workspace</span>          <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">getLayout</span><span class="p">().</span><span class="nx">workspace</span><span class="p">,</span></div><div class='line' id='LC316'>		<span class="nx">workspaceDiameter</span>  <span class="o">=</span> <span class="nx">workspace</span><span class="p">.</span><span class="nx">radius</span> <span class="o">*</span> <span class="mi">2</span><span class="p">,</span></div><div class='line' id='LC317'>		<span class="nx">workspaceNegRadius</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span> <span class="o">*</span> <span class="nx">workspace</span><span class="p">.</span><span class="nx">radius</span><span class="p">,</span></div><div class='line' id='LC318'>		<span class="nx">dashes</span>             <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">dashes</span><span class="p">;</span></div><div class='line' id='LC319'><br/></div><div class='line' id='LC320'>	<span class="k">this</span><span class="p">.</span><span class="nx">ctx</span><span class="p">.</span><span class="nx">clearRect</span><span class="p">(</span><span class="nx">workspaceNegRadius</span><span class="p">,</span> <span class="nx">workspaceNegRadius</span><span class="p">,</span> <span class="nx">workspaceDiameter</span><span class="p">,</span> <span class="nx">workspaceDiameter</span><span class="p">);</span></div><div class='line' id='LC321'><br/></div><div class='line' id='LC322'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">rotation</span>  <span class="o">=</span> <span class="nx">radian</span><span class="p">(</span><span class="mi">360</span> <span class="o">/</span> <span class="nx">dashes</span><span class="p">),</span></div><div class='line' id='LC323'>	    <span class="nx">opacities</span> <span class="o">=</span> <span class="nx">scrollArray</span><span class="p">(</span><span class="nx">workspace</span><span class="p">.</span><span class="nx">opacities</span><span class="p">,</span> <span class="nx">position</span> <span class="o">*</span> <span class="o">-</span><span class="mi">1</span><span class="p">),</span></div><div class='line' id='LC324'>	    <span class="nx">color</span>     <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">dash</span><span class="p">.</span><span class="nx">color</span><span class="p">;</span></div><div class='line' id='LC325'><br/></div><div class='line' id='LC326'>	<span class="k">for</span> <span class="p">(</span><span class="kd">var</span> <span class="nx">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">,</span> <span class="nx">len</span> <span class="o">=</span> <span class="nx">dashes</span><span class="p">;</span> <span class="nx">i</span> <span class="o">&lt;</span> <span class="nx">len</span><span class="p">;</span> <span class="nx">i</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC327'>&nbsp;&nbsp;	  <span class="k">this</span><span class="p">.</span><span class="nx">drawDash</span><span class="p">(</span><span class="nx">opacities</span><span class="p">[</span><span class="nx">i</span><span class="p">],</span> <span class="nx">color</span><span class="p">);</span></div><div class='line' id='LC328'>&nbsp;&nbsp;	  <span class="k">this</span><span class="p">.</span><span class="nx">ctx</span><span class="p">.</span><span class="nx">rotate</span><span class="p">(</span><span class="nx">rotation</span><span class="p">);</span></div><div class='line' id='LC329'>	<span class="p">}</span></div><div class='line' id='LC330'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC331'>&nbsp;&nbsp;</div><div class='line' id='LC332'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">drawDash</span><span class="p">(</span><span class="nx">opacity</span><span class="p">,</span> <span class="nx">color</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC333'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">ctx</span><span class="p">.</span><span class="nx">fillStyle</span> <span class="o">=</span> <span class="nx">Color</span><span class="p">.</span><span class="nx">hex2fill</span><span class="p">(</span><span class="nx">color</span><span class="p">,</span> <span class="nx">opacity</span><span class="p">);</span></div><div class='line' id='LC334'><br/></div><div class='line' id='LC335'>	<span class="kd">var</span> <span class="nx">layout</span>          <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">getLayout</span><span class="p">(),</span></div><div class='line' id='LC336'>	   	<span class="nx">workspaceRadius</span> <span class="o">=</span> <span class="nx">layout</span><span class="p">.</span><span class="nx">workspace</span><span class="p">.</span><span class="nx">radius</span><span class="p">,</span></div><div class='line' id='LC337'>	   	<span class="nx">dashPosition</span>    <span class="o">=</span> <span class="nx">layout</span><span class="p">.</span><span class="nx">dash</span><span class="p">.</span><span class="nx">position</span><span class="p">,</span></div><div class='line' id='LC338'>	   	<span class="nx">dashDimensions</span>  <span class="o">=</span> <span class="nx">layout</span><span class="p">.</span><span class="nx">dash</span><span class="p">.</span><span class="nx">dimensions</span><span class="p">;</span></div><div class='line' id='LC339'><br/></div><div class='line' id='LC340'>	<span class="nx">Canvas</span><span class="p">.</span><span class="nx">drawRoundedRectangle</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">ctx</span><span class="p">,</span> <span class="p">{</span></div><div class='line' id='LC341'>	  <span class="nx">top</span><span class="o">:</span>    <span class="nx">dashPosition</span><span class="p">.</span><span class="nx">top</span> <span class="o">-</span> <span class="nx">workspaceRadius</span><span class="p">,</span></div><div class='line' id='LC342'>	  <span class="nx">left</span><span class="o">:</span>   <span class="nx">dashPosition</span><span class="p">.</span><span class="nx">left</span> <span class="o">-</span> <span class="nx">workspaceRadius</span><span class="p">,</span></div><div class='line' id='LC343'>	  <span class="nx">width</span><span class="o">:</span>  <span class="nx">dashDimensions</span><span class="p">.</span><span class="nx">width</span><span class="p">,</span></div><div class='line' id='LC344'>	  <span class="nx">height</span><span class="o">:</span> <span class="nx">dashDimensions</span><span class="p">.</span><span class="nx">height</span><span class="p">,</span></div><div class='line' id='LC345'>	  <span class="nx">radius</span><span class="o">:</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">min</span><span class="p">(</span><span class="nx">dashDimensions</span><span class="p">.</span><span class="nx">height</span><span class="p">,</span> <span class="nx">dashDimensions</span><span class="p">.</span><span class="nx">width</span><span class="p">)</span> <span class="o">/</span> <span class="mi">2</span></div><div class='line' id='LC346'>	<span class="p">});</span></div><div class='line' id='LC347'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC348'>&nbsp;&nbsp;</div><div class='line' id='LC349'>&nbsp;&nbsp;</div><div class='line' id='LC350'>&nbsp;&nbsp;<span class="cm">/*</span></div><div class='line' id='LC351'><span class="cm">   * Position</span></div><div class='line' id='LC352'><span class="cm">   */</span></div><div class='line' id='LC353'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">_nextPosition</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC354'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">ms</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">speed</span> <span class="o">*</span> <span class="mi">1000</span> <span class="o">/</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">dashes</span><span class="p">;</span></div><div class='line' id='LC355'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">nextPosition</span><span class="p">();</span></div><div class='line' id='LC356'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">this</span><span class="p">.</span><span class="nx">_playTimer</span> <span class="o">=</span> <span class="nb">window</span><span class="p">.</span><span class="nx">setTimeout</span><span class="p">(</span><span class="nx">$B</span><span class="p">.</span><span class="nb">Function</span><span class="p">.</span><span class="nx">bind</span><span class="p">(</span><span class="nx">_nextPosition</span><span class="p">,</span> <span class="k">this</span><span class="p">),</span> <span class="nx">ms</span><span class="p">);</span></div><div class='line' id='LC357'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC358'>&nbsp;&nbsp;</div><div class='line' id='LC359'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">nextPosition</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC360'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">_position</span> <span class="o">==</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">dashes</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span></div><div class='line' id='LC361'>	<span class="k">this</span><span class="p">.</span><span class="nx">_position</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span><span class="p">;</span></div><div class='line' id='LC362'>	<span class="k">this</span><span class="p">.</span><span class="nx">_position</span><span class="o">++</span><span class="p">;</span></div><div class='line' id='LC363'>	<span class="k">this</span><span class="p">.</span><span class="nx">drawPosition</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">_position</span><span class="p">);</span> </div><div class='line' id='LC364'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC365'><br/></div><div class='line' id='LC366'><br/></div><div class='line' id='LC367'>&nbsp;&nbsp;<span class="cm">/*</span></div><div class='line' id='LC368'><span class="cm">   * State</span></div><div class='line' id='LC369'><span class="cm">   */</span></div><div class='line' id='LC370'>&nbsp;&nbsp;</div><div class='line' id='LC371'>&nbsp;&nbsp;<span class="cm">/*</span></div><div class='line' id='LC372'><span class="cm">   * Controls</span></div><div class='line' id='LC373'><span class="cm">   * play, pause, stop</span></div><div class='line' id='LC374'><span class="cm">   */</span></div><div class='line' id='LC375'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">play</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC376'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">_state</span> <span class="o">==</span> <span class="s1">&#39;playing&#39;</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span></div><div class='line' id='LC377'><br/></div><div class='line' id='LC378'>	<span class="k">this</span><span class="p">.</span><span class="nx">_state</span> <span class="o">=</span> <span class="s1">&#39;playing&#39;</span><span class="p">;</span></div><div class='line' id='LC379'><br/></div><div class='line' id='LC380'>	<span class="kd">var</span> <span class="nx">ms</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">speed</span> <span class="o">*</span> <span class="mi">1000</span> <span class="o">/</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">.</span><span class="nx">dashes</span><span class="p">;</span></div><div class='line' id='LC381'>	<span class="k">this</span><span class="p">.</span><span class="nx">_playTimer</span> <span class="o">=</span> <span class="nb">window</span><span class="p">.</span><span class="nx">setTimeout</span><span class="p">(</span><span class="nx">$B</span><span class="p">.</span><span class="nb">Function</span><span class="p">.</span><span class="nx">bind</span><span class="p">(</span><span class="nx">_nextPosition</span><span class="p">,</span> <span class="k">this</span><span class="p">),</span> <span class="nx">ms</span><span class="p">);</span></div><div class='line' id='LC382'>	<span class="k">return</span> <span class="k">this</span><span class="p">;</span></div><div class='line' id='LC383'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC384'>&nbsp;&nbsp;</div><div class='line' id='LC385'><br/></div><div class='line' id='LC386'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">pause</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC387'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">_state</span> <span class="o">==</span> <span class="s1">&#39;paused&#39;</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span></div><div class='line' id='LC388'><br/></div><div class='line' id='LC389'>	<span class="k">this</span><span class="p">.</span><span class="nx">_pause</span><span class="p">();</span></div><div class='line' id='LC390'><br/></div><div class='line' id='LC391'>	<span class="k">this</span><span class="p">.</span><span class="nx">_state</span> <span class="o">=</span> <span class="s1">&#39;paused&#39;</span><span class="p">;</span></div><div class='line' id='LC392'>	<span class="k">return</span> <span class="k">this</span><span class="p">;</span></div><div class='line' id='LC393'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC394'><br/></div><div class='line' id='LC395'>&nbsp;&nbsp;</div><div class='line' id='LC396'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">_pause</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC397'>	<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="k">this</span><span class="p">.</span><span class="nx">_playTimer</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span></div><div class='line' id='LC398'>	<span class="nb">window</span><span class="p">.</span><span class="nx">clearTimeout</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">_playTimer</span><span class="p">);</span></div><div class='line' id='LC399'>	<span class="k">this</span><span class="p">.</span><span class="nx">_playTimer</span> <span class="o">=</span> <span class="kc">null</span><span class="p">;</span></div><div class='line' id='LC400'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC401'>&nbsp;&nbsp;</div><div class='line' id='LC402'>&nbsp;&nbsp;</div><div class='line' id='LC403'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">stop</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC404'>	<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">_state</span> <span class="o">==</span> <span class="s1">&#39;stopped&#39;</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span></div><div class='line' id='LC405'><br/></div><div class='line' id='LC406'>	<span class="k">this</span><span class="p">.</span><span class="nx">_pause</span><span class="p">();</span></div><div class='line' id='LC407'><br/></div><div class='line' id='LC408'>	<span class="c1">// TODO: position weer naar 0 en 0 tekenen</span></div><div class='line' id='LC409'>	<span class="k">this</span><span class="p">.</span><span class="nx">_position</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span></div><div class='line' id='LC410'>	<span class="k">this</span><span class="p">.</span><span class="nx">drawPosition</span><span class="p">(</span><span class="mi">0</span><span class="p">);</span></div><div class='line' id='LC411'><br/></div><div class='line' id='LC412'>	<span class="k">this</span><span class="p">.</span><span class="nx">_state</span> <span class="o">=</span> <span class="s1">&#39;stopped&#39;</span><span class="p">;</span></div><div class='line' id='LC413'>	<span class="k">return</span> <span class="k">this</span><span class="p">;</span></div><div class='line' id='LC414'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC415'>&nbsp;&nbsp;</div><div class='line' id='LC416'>&nbsp;&nbsp;</div><div class='line' id='LC417'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">toggle</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC418'>	<span class="k">this</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">_state</span> <span class="o">==</span> <span class="s1">&#39;playing&#39;</span> <span class="o">?</span> <span class="s1">&#39;pause&#39;</span> <span class="o">:</span> <span class="s1">&#39;play&#39;</span><span class="p">]();</span></div><div class='line' id='LC419'>	<span class="k">return</span> <span class="k">this</span><span class="p">;</span></div><div class='line' id='LC420'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC421'>&nbsp;&nbsp;</div><div class='line' id='LC422'><br/></div><div class='line' id='LC423'>&nbsp;&nbsp;<span class="cm">/*</span></div><div class='line' id='LC424'><span class="cm">   * Layout</span></div><div class='line' id='LC425'><span class="cm">   */</span></div><div class='line' id='LC426'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">getOpacityArray</span><span class="p">(</span><span class="nx">dashes</span><span class="p">)</span> <span class="p">{</span></div><div class='line' id='LC427'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="kd">var</span> <span class="nx">step</span>  <span class="o">=</span> <span class="mi">1</span> <span class="o">/</span> <span class="nx">dashes</span><span class="p">,</span> <span class="nx">array</span> <span class="o">=</span> <span class="p">[];</span></div><div class='line' id='LC428'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="p">(</span><span class="kd">var</span> <span class="nx">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span><span class="nx">i</span><span class="o">&lt;</span><span class="nx">dashes</span><span class="p">;</span><span class="nx">i</span><span class="o">++</span><span class="p">)</span></div><div class='line' id='LC429'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">array</span><span class="p">.</span><span class="nx">push</span><span class="p">((</span><span class="nx">i</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span> <span class="o">*</span> <span class="nx">step</span><span class="p">);</span></div><div class='line' id='LC430'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nx">array</span><span class="p">;</span></div><div class='line' id='LC431'>&nbsp;&nbsp;<span class="p">}</span></div><div class='line' id='LC432'>&nbsp;&nbsp;</div><div class='line' id='LC433'>&nbsp;&nbsp;<span class="kd">function</span> <span class="nx">getLayout</span><span class="p">()</span> <span class="p">{</span></div><div class='line' id='LC434'>	<span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">_layout</span><span class="p">)</span> <span class="k">return</span> <span class="k">this</span><span class="p">.</span><span class="nx">_layout</span><span class="p">;</span></div><div class='line' id='LC435'><br/></div><div class='line' id='LC436'>	<span class="kd">var</span> <span class="nx">options</span>   <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">options</span><span class="p">,</span></div><div class='line' id='LC437'>	    <span class="nx">dashes</span>    <span class="o">=</span> <span class="nx">options</span><span class="p">.</span><span class="nx">dashes</span><span class="p">,</span></div><div class='line' id='LC438'>	   	<span class="nx">radii</span>     <span class="o">=</span> <span class="nx">options</span><span class="p">.</span><span class="nx">radii</span><span class="p">,</span></div><div class='line' id='LC439'>		<span class="nx">dashWidth</span> <span class="o">=</span> <span class="nx">options</span><span class="p">.</span><span class="nx">dash</span><span class="p">.</span><span class="nx">width</span><span class="p">,</span></div><div class='line' id='LC440'>	    <span class="nx">minRadius</span> <span class="o">=</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">min</span><span class="p">(</span><span class="nx">radii</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nx">radii</span><span class="p">[</span><span class="mi">1</span><span class="p">]),</span></div><div class='line' id='LC441'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">maxRadius</span> <span class="o">=</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">max</span><span class="p">(</span><span class="nx">radii</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nx">radii</span><span class="p">[</span><span class="mi">1</span><span class="p">]),</span></div><div class='line' id='LC442'><br/></div><div class='line' id='LC443'>		<span class="nx">maxWorkspaceRadius</span> <span class="o">=</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">max</span><span class="p">(</span><span class="nx">dashWidth</span><span class="p">,</span> <span class="nx">maxRadius</span><span class="p">),</span></div><div class='line' id='LC444'>		<span class="nx">workspaceRadius</span> <span class="o">=</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">ceil</span><span class="p">(</span><span class="nb">Math</span><span class="p">.</span><span class="nx">max</span><span class="p">(</span></div><div class='line' id='LC445'>		  <span class="nx">maxWorkspaceRadius</span><span class="p">,</span></div><div class='line' id='LC446'>		  <span class="c1">// the hook created by dashWidth</span></div><div class='line' id='LC447'>		  <span class="c1">// could give a bigger radius</span></div><div class='line' id='LC448'>		  <span class="nx">pyth</span><span class="p">(</span><span class="nx">maxRadius</span><span class="p">,</span> <span class="nx">dashWidth</span><span class="o">/</span><span class="mi">2</span><span class="p">)</span></div><div class='line' id='LC449'>		<span class="p">)),</span></div><div class='line' id='LC450'><br/></div><div class='line' id='LC451'><br/></div><div class='line' id='LC452'>	    <span class="nx">halfWorkspace</span>   <span class="o">=</span> <span class="nx">workspaceRadius</span> <span class="o">/</span> <span class="mi">2</span><span class="p">,</span></div><div class='line' id='LC453'>	    <span class="nx">innerPositionZ</span>  <span class="o">=</span> <span class="nx">halfWorkspace</span> <span class="o">-</span> <span class="nx">minRadius</span> <span class="o">/</span> <span class="mi">2</span><span class="p">,</span></div><div class='line' id='LC454'>		<span class="nx">outerPositionZ</span>  <span class="o">=</span> <span class="nx">halfWorkspace</span> <span class="o">-</span> <span class="nx">maxRadius</span> <span class="o">/</span> <span class="mi">2</span><span class="p">;</span></div><div class='line' id='LC455'><br/></div><div class='line' id='LC456'>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='line' id='LC457'>	<span class="kd">var</span> <span class="nx">layout</span> <span class="o">=</span> <span class="p">{</span></div><div class='line' id='LC458'>	  <span class="nx">workspace</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC459'>	    <span class="nx">radius</span><span class="o">:</span> <span class="nx">workspaceRadius</span><span class="p">,</span></div><div class='line' id='LC460'>	    <span class="nx">opacities</span><span class="o">:</span> <span class="nx">getOpacityArray</span><span class="p">(</span><span class="nx">dashes</span><span class="p">)</span></div><div class='line' id='LC461'>	  <span class="p">},</span></div><div class='line' id='LC462'>	  <span class="nx">inner</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC463'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">position</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC464'>	      <span class="nx">top</span><span class="o">:</span>  <span class="nx">innerPositionZ</span><span class="p">,</span></div><div class='line' id='LC465'>	      <span class="nx">left</span><span class="o">:</span> <span class="nx">innerPositionZ</span></div><div class='line' id='LC466'>	    <span class="p">},</span></div><div class='line' id='LC467'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nx">radius</span><span class="o">:</span> <span class="nx">minRadius</span></div><div class='line' id='LC468'>	  <span class="p">},</span></div><div class='line' id='LC469'>	  <span class="nx">outer</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC470'>		<span class="nx">position</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC471'>		  <span class="nx">top</span><span class="o">:</span>  <span class="nx">outerPositionZ</span><span class="p">,</span></div><div class='line' id='LC472'>		  <span class="nx">left</span><span class="o">:</span> <span class="nx">outerPositionZ</span></div><div class='line' id='LC473'>		<span class="p">},</span></div><div class='line' id='LC474'>		<span class="nx">radius</span><span class="o">:</span> <span class="nx">maxRadius</span></div><div class='line' id='LC475'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="p">},</span></div><div class='line' id='LC476'>	  <span class="nx">dash</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC477'>		<span class="nx">position</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC478'>		  <span class="nx">top</span><span class="o">:</span>  <span class="nx">outerPositionZ</span><span class="p">,</span></div><div class='line' id='LC479'>		  <span class="nx">left</span><span class="o">:</span> <span class="nx">workspaceRadius</span> <span class="o">-</span> <span class="nx">dashWidth</span> <span class="o">/</span> <span class="mi">2</span></div><div class='line' id='LC480'>		<span class="p">},</span></div><div class='line' id='LC481'>		<span class="nx">dimensions</span><span class="o">:</span> <span class="p">{</span></div><div class='line' id='LC482'>		  <span class="nx">width</span><span class="o">:</span> <span class="nx">dashWidth</span><span class="p">,</span></div><div class='line' id='LC483'>		  <span class="nx">height</span><span class="o">:</span> <span class="nx">maxRadius</span> <span class="o">-</span> <span class="nx">minRadius</span></div><div class='line' id='LC484'>		<span class="p">}</span></div><div class='line' id='LC485'>	  <span class="p">}</span></div><div class='line' id='LC486'>	<span class="p">};</span></div><div class='line' id='LC487'><br/></div><div class='line' id='LC488'>	<span class="c1">// cache</span></div><div class='line' id='LC489'>	<span class="k">this</span><span class="p">.</span><span class="nx">_layout</span> <span class="o">=</span> <span class="nx">layout</span><span class="p">;</span></div><div class='line' id='LC490'><br/></div><div class='line' id='LC491'>	<span class="k">return</span> <span class="nx">layout</span><span class="p">;</span></div><div class='line' id='LC492'>&nbsp;&nbsp;<span class="p">}</span> </div><div class='line' id='LC493'>&nbsp;&nbsp;</div><div class='line' id='LC494'>&nbsp;&nbsp;<span class="k">return</span> <span class="p">{</span></div><div class='line' id='LC495'>	<span class="nx">remove</span><span class="o">:</span>        <span class="nx">remove</span><span class="p">,</span></div><div class='line' id='LC496'>	<span class="nx">build</span><span class="o">:</span>         <span class="nx">build</span><span class="p">,</span></div><div class='line' id='LC497'>	<span class="nx">getLayout</span><span class="o">:</span>     <span class="nx">getLayout</span><span class="p">,</span></div><div class='line' id='LC498'>	<span class="nx">_nextPosition</span><span class="o">:</span> <span class="nx">_nextPosition</span><span class="p">,</span></div><div class='line' id='LC499'>	<span class="nx">nextPosition</span><span class="o">:</span>  <span class="nx">nextPosition</span><span class="p">,</span></div><div class='line' id='LC500'>	<span class="nx">drawPosition</span><span class="o">:</span>  <span class="nx">drawPosition</span><span class="p">,</span></div><div class='line' id='LC501'>	<span class="nx">drawDash</span><span class="o">:</span>      <span class="nx">drawDash</span><span class="p">,</span></div><div class='line' id='LC502'>	<span class="nx">play</span><span class="o">:</span>          <span class="nx">play</span><span class="p">,</span></div><div class='line' id='LC503'>	<span class="nx">pause</span><span class="o">:</span>         <span class="nx">pause</span><span class="p">,</span></div><div class='line' id='LC504'>	<span class="nx">_pause</span><span class="o">:</span>        <span class="nx">_pause</span><span class="p">,</span></div><div class='line' id='LC505'>	<span class="nx">stop</span><span class="o">:</span>          <span class="nx">stop</span><span class="p">,</span></div><div class='line' id='LC506'>	<span class="nx">toggle</span><span class="o">:</span>        <span class="nx">toggle</span></div><div class='line' id='LC507'>&nbsp;&nbsp;<span class="p">};</span></div><div class='line' id='LC508'><span class="p">})());</span></div><div class='line' id='LC509'><br/></div><div class='line' id='LC510'><span class="c1">// expose</span></div><div class='line' id='LC511'><span class="nb">window</span><span class="p">.</span><span class="nx">Spinner</span> <span class="o">=</span> <span class="nx">Spinner</span><span class="p">;</span></div><div class='line' id='LC512'><br/></div><div class='line' id='LC513'><span class="nx">Spinners</span><span class="p">.</span><span class="nx">start</span><span class="p">();</span></div><div class='line' id='LC514'><span class="p">})(</span><span class="nx">Bridge</span><span class="p">);</span></div></pre></div>
              
            
          </td>
        </tr>
      </table>
    
  </div>


      </div>
    </div>
  


    </div>
  
      
    </div>

    <div id="footer" class="clearfix">
      <div class="site">
        <div class="sponsor">
          <a href="http://www.rackspace.com" class="logo">
            <img alt="Dedicated Server" src="https://assets3.github.com/images/modules/footer/rackspace_logo.png?v2?9cca70593ea5e402012810a9233fc52d8f97cb13" />
          </a>
          Powered by the <a href="http://www.rackspace.com ">Dedicated
          Servers</a> and<br/> <a href="http://www.rackspacecloud.com">Cloud
          Computing</a> of Rackspace Hosting<span>&reg;</span>
        </div>

        <ul class="links">
          <li class="blog"><a href="https://github.com/blog">Blog</a></li>
          <li><a href="http://support.github.com">Support</a></li>
          <li><a href="https://github.com/training">Training</a></li>
          <li><a href="http://jobs.github.com">Job Board</a></li>
          <li><a href="http://shop.github.com">Shop</a></li>
          <li><a href="https://github.com/contact">Contact</a></li>
          <li><a href="http://develop.github.com">API</a></li>
          <li><a href="http://status.github.com">Status</a></li>
        </ul>
        <ul class="sosueme">
          <li class="main">&copy; 2010 <span id="_rrt" title="0.11882s from fe6.rs.github.com">GitHub</span> Inc. All rights reserved.</li>
          <li><a href="/site/terms">Terms of Service</a></li>
          <li><a href="/site/privacy">Privacy</a></li>
          <li><a href="https://github.com/security">Security</a></li>
        </ul>
      </div>
    </div><!-- /#footer -->

    
      
      
        <!-- current locale:  -->
        <div class="locales">
          <div class="site">

            <ul class="choices clearfix limited-locales">
              <li><span class="current">English</span></li>
              
                  <li><a rel="nofollow" href="?locale=de">Deutsch</a></li>
              
                  <li><a rel="nofollow" href="?locale=fr">Français</a></li>
              
                  <li><a rel="nofollow" href="?locale=ja">日本語</a></li>
              
                  <li><a rel="nofollow" href="?locale=pt-BR">Português (BR)</a></li>
              
                  <li><a rel="nofollow" href="?locale=ru">Русский</a></li>
              
                  <li><a rel="nofollow" href="?locale=zh">中文</a></li>
              
              <li class="all"><a href="#" class="minibutton btn-forward js-all-locales"><span><span class="icon"></span>See all available languages</span></a></li>
            </ul>

            <div class="all-locales clearfix">
              <h3>Your current locale selection: <strong>English</strong>. Choose another?</h3>
              
              
                <ul class="choices">
                  
                      <li><a rel="nofollow" href="?locale=en">English</a></li>
                  
                      <li><a rel="nofollow" href="?locale=af">Afrikaans</a></li>
                  
                      <li><a rel="nofollow" href="?locale=ca">Català</a></li>
                  
                      <li><a rel="nofollow" href="?locale=cs">Čeština</a></li>
                  
                </ul>
              
                <ul class="choices">
                  
                      <li><a rel="nofollow" href="?locale=de">Deutsch</a></li>
                  
                      <li><a rel="nofollow" href="?locale=es">Español</a></li>
                  
                      <li><a rel="nofollow" href="?locale=fr">Français</a></li>
                  
                      <li><a rel="nofollow" href="?locale=hr">Hrvatski</a></li>
                  
                </ul>
              
                <ul class="choices">
                  
                      <li><a rel="nofollow" href="?locale=id">Indonesia</a></li>
                  
                      <li><a rel="nofollow" href="?locale=it">Italiano</a></li>
                  
                      <li><a rel="nofollow" href="?locale=ja">日本語</a></li>
                  
                      <li><a rel="nofollow" href="?locale=nl">Nederlands</a></li>
                  
                </ul>
              
                <ul class="choices">
                  
                      <li><a rel="nofollow" href="?locale=no">Norsk</a></li>
                  
                      <li><a rel="nofollow" href="?locale=pl">Polski</a></li>
                  
                      <li><a rel="nofollow" href="?locale=pt-BR">Português (BR)</a></li>
                  
                      <li><a rel="nofollow" href="?locale=ru">Русский</a></li>
                  
                </ul>
              
                <ul class="choices">
                  
                      <li><a rel="nofollow" href="?locale=sr">Српски</a></li>
                  
                      <li><a rel="nofollow" href="?locale=sv">Svenska</a></li>
                  
                      <li><a rel="nofollow" href="?locale=zh">中文</a></li>
                  
                </ul>
              
            </div>

          </div>
          <div class="fade"></div>
        </div>
      
    

    <script>window._auth_token = "7ed14d1a6644ac2eca49f7be6b7072ba1f41afa5"</script>
    <div id="keyboard_shortcuts_pane" style="display:none">
  <h2>Keyboard Shortcuts</h2>

  <div class="columns threecols">
    <div class="column first">
      <h3>Site wide shortcuts</h3>
      <dl class="keyboard-mappings">
        <dt>s</dt>
        <dd>Focus site search</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>?</dt>
        <dd>Bring up this help dialog</dd>
      </dl>
    </div><!-- /.column.first -->
    <div class="column middle">
      <h3>Commit list</h3>
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selected down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selected up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>t</dt>
        <dd>Open tree</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>p</dt>
        <dd>Open parent</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>c <em>or</em> o <em>or</em> enter</dt>
        <dd>Open commit</dd>
      </dl>
    </div><!-- /.column.first -->
    <div class="column last">
      <h3>Pull request list</h3>
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selected down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selected up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>o <em>or</em> enter</dt>
        <dd>Open issue</dd>
      </dl>
    </div><!-- /.columns.last -->
  </div><!-- /.columns.equacols -->

  <div class="rule"></div>

  <h3>Issues</h3>

  <div class="columns threecols">
    <div class="column first">
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selected down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selected up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>x</dt>
        <dd>Toggle select target</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>o <em>or</em> enter</dt>
        <dd>Open issue</dd>
      </dl>
    </div><!-- /.column.first -->
    <div class="column middle">
      <dl class="keyboard-mappings">
        <dt>I</dt>
        <dd>Mark selected as read</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>U</dt>
        <dd>Mark selected as unread</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>e</dt>
        <dd>Close selected</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>y</dt>
        <dd>Remove selected from view</dd>
      </dl>
    </div><!-- /.column.middle -->
    <div class="column last">
      <dl class="keyboard-mappings">
        <dt>c</dt>
        <dd>Create issue</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>l</dt>
        <dd>Create label</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>i</dt>
        <dd>Back to inbox</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>u</dt>
        <dd>Back to issues</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>/</dt>
        <dd>Focus issues search</dd>
      </dl>
    </div>
  </div>

  <div class="rule"></div>

  <h3>Network Graph</h3>
  <div class="columns equacols">
    <div class="column first">
      <dl class="keyboard-mappings">
        <dt>← <em>or</em> h</dt>
        <dd>Scroll left</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>→ <em>or</em> l</dt>
        <dd>Scroll right</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>↑ <em>or</em> k</dt>
        <dd>Scroll up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>↓ <em>or</em> j</dt>
        <dd>Scroll down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>t</dt>
        <dd>Toggle visibility of head labels</dd>
      </dl>
    </div><!-- /.column.first -->
    <div class="column last">
      <dl class="keyboard-mappings">
        <dt>shift ← <em>or</em> shift h</dt>
        <dd>Scroll all the way left</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>shift → <em>or</em> shift l</dt>
        <dd>Scroll all the way right</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>shift ↑ <em>or</em> shift k</dt>
        <dd>Scroll all the way up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>shift ↓ <em>or</em> shift j</dt>
        <dd>Scroll all the way down</dd>
      </dl>
    </div><!-- /.column.last -->
  </div>

</div>
    

    <!--[if IE 8]>
    <script type="text/javascript" charset="utf-8">
      $(document.body).addClass("ie8")
    </script>
    <![endif]-->

    <!--[if IE 7]>
    <script type="text/javascript" charset="utf-8">
      $(document.body).addClass("ie7")
    </script>
    <![endif]-->

    <script type="text/javascript">
      _kmq.push(['trackClick', 'entice-signup-button', 'Entice banner clicked']);
      
    </script>
    
  </body>
</html>

