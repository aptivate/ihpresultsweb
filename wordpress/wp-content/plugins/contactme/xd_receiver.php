<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>ContactMe</title>
</head>
<body>
<?php
	if (isset($_GET) && count($_GET) > 0) {
	  if (isset($_GET['button_src'])) $_GET['button_src'] = base64_decode($_GET['button_src']);
	  if (isset($_GET['embed_src'])) $_GET['embed_src'] = base64_decode($_GET['embed_src']);
?>
<script type="text/javascript">parent.xd_callback({data:'<?php echo serialize($_GET) ?>'});</script>
<?php
	} 
?>
</body>
</html>