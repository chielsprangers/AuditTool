<?php
    include 'header.php';
?>

<h1>WebScan</h1>
<hr/>
<form action="webscanResult.php" method="post">
	<div class=" ">
		<div class="flexcontainer">
			<div class="d-flex">
				<h6>URL</h6>
			</div>
			<div class="form-group d-flex">
				<input class="form-control" type="text" name="URL" placeholder="URL - Please specify http or https. End the url with a trailing /"><br/>
			</div>
			<hr/>
		</div>
		<div class="flexcontainer">
			<div class="d-flex">
				<h6>Login</h6>
			</div>
			<div class="d-flex mg-b-20">
				<input class="form-control" type="text" name="URLLogin" placeholder="URL to login page - If applicable and only use test accounts."><br/>
			</div>
			<div class="form-group d-flex">
				<input class="form-control" type="text" name="Username" placeholder="Username"><br/>
				<input class="form-control mg-l-20" type="password" name="Password" placeholder="Password"><br/>
			</div>
			<hr/>
		</div>
	</div>
	<button class="btn btn-primary" type="submit">Scan</button>
</form>

<?php
    include 'footer.php';
?>

<script language="javascript">
    document.title = "Auditing Tool - WebScan";
</script>