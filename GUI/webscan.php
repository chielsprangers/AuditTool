<?php
    include 'header.php';
?>

<h1>WebScan</h1>
<hr/>
<form action="webscanResult.php" method="post">
    <input class="form-control" type="text" name="URL" placeholder="URL - Please specify http or https."><br/>
    <button class="btn btn-primary" type="submit">Scan</button>
</form>

<?php
    include 'footer.php';
?>

<script language="javascript">
    document.title = "Auditing Tool - WebScan";
</script>