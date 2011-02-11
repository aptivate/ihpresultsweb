<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>ContactMe</title>
</head>
<body>
<?php
	if (isset($_GET) && count($_GET) > 0) {
?>
<script type="text/javascript">parent.xd_resize({width:'<?php echo $_GET["width"] ?>', height:'<?php echo $_GET["height"] ?>'});</script>
<?php
	} 
?>
</body>
</html>