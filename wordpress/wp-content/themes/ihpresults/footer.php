</div>
<!-- end wrapper-inner -->
</div>
<!-- end wrapper -->
<div id="footer">
<div id="footer-inner">
	<div id="footer-left">
		<div class="copyright">
			<?php ob_start("qtrans_useCurrentLanguageIfNotFoundUseDefaultLanguage"); ?>
			<a href="http://www.re-action.co.za"><img style="width: 100px;"
				src="/wp-content/uploads/2011/02/logo21.jpg"
				alt="Re-Action Logo"></a>
			<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/"><img
			 	alt="Creative Commons License" style="border-width:0"
			 	src="http://i.creativecommons.org/l/by-nc/3.0/88x31.png" /></a>
			<br />
			<!--:en-->
			<span xmlns:dct="http://purl.org/dc/terms/"
			 	href="http://purl.org/dc/dcmitype/Text" property="dct:title"
			 	rel="dct:type">IHP+Results Performance Monitoring and
			 	Accountability Mechanism for the International Health
			 	Partnership	(IHP+)</span> by <a
			 	xmlns:cc="http://creativecommons.org/ns#"
				href="http://www.re-action.co.za" property="cc:attributionName"
				rel="cc:attributionURL">Re-Action! (UK) Ltd</a> is licensed
				under a	<a rel="license"
				href="http://creativecommons.org/licenses/by-nc/3.0/">Creative
				Commons Attribution-NonCommercial 3.0 Unported License</a>.
				Based on a work at <a xmlns:dct="http://purl.org/dc/terms/"
				href="http://www.ihpresults.net"
				rel="dct:source">www.ihpresults.net</a>.
			<!--:--><!--:fr-->
			<span xmlns:dct="http://purl.org/dc/terms/"
				href="http://purl.org/dc/dcmitype/Text" property="dct:title"
				rel="dct:type">IHP+Results Performance Monitoring and
				Accountability Mechanism for the International Health
				Partnership	(IHP+)</span> de <a
				xmlns:cc="http://creativecommons.org/ns#"
				href="http://www.re-action.co.za" property="cc:attributionName"
				rel="cc:attributionURL">Re-Action! (UK) Ltd</a> est mis à
				disposition selon les termes de la <a rel="license"
				href="http://creativecommons.org/licenses/by-nc/3.0/">licence
				Creative Commons Paternité - Pas d'Utilisation Commerciale 3.0
				Unported</a>. Basé(e) sur une oeuvre à <a
				xmlns:dct="http://purl.org/dc/terms/"
				href="http://www.ihpresults.net"
				rel="dct:source">www.ihpresults.net</a>.
			<!--:-->
			<?php ob_end_flush(); ?>
		</div>
		<?php wp_nav_menu( array('theme_location' => 'tertiary' ) ); ?>
	</div><!-- end footer-left -->
  	<div id="footer-right">
  		<div id="logins"><?php wp_loginout( $redirect ); ?> | <a href="/wp-admin">admin</a> | <a href="http://www.google.com/analytics">stats</a></div>
		<div class="siteinfo"><a href="http://www.aptivate.org">site by Aptivate</a></div>
		</div><!-- end footer-right -->
  
  </div><!-- end footer-inner -->
</div>
<!-- end footer -->

<?php wp_footer(); ?>
</body>
</html>
