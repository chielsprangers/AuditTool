<?php
    include 'header.php';
?>

<h1>NetScan</h1>
<hr/>
<form action="netscanResult.php" method="post">
    <input class="form-control" type="text" name="ips" placeholder="IPs - Separate IP's with semicolon(;). Ranges not yet supported."><br/>
    <button class="btn btn-primary" type="submit">Scan</button>
</form>

<?php
    include 'footer.php';
?>

<script language="javascript">
    document.title = "Auditing Tool - NetScan";
</script>