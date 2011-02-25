</div>
<!-- end wrapper-inner -->
</div>
<!-- end wrapper -->
<div id="footer">
<div id="footer-inner">
	<div id="footer-left">
		 <div class="copyright">statement about this website and any rights associated with it</div>
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