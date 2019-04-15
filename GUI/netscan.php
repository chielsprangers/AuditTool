<?php
    include 'header.php';
?>

<h1>NetScan</h1>
<hr/>
<form action="netscanResult.php" method="post">
    <div class=" ">
		<div class="flexcontainer">
			<div class="d-flex">
				<h6>IPs</h6>
			</div>
			<div class="form-group d-flex">
                <input class="form-control" type="text" name="ips" placeholder="IPs - Separate IP's with semicolon(;). Ranges not yet supported."><br/> 
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
    document.title = "Auditing Tool - NetScan";
</script>