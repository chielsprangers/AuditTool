<?php
    include 'header.php';
?>

<?php
    $URL;

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        if (!empty($_POST["URL"])) {
            $URL = test_input($_POST["URL"]);
            if (!empty($_POST["URLLogin"])) {
                $URLLogin = test_input($_POST["URLLogin"]);
            }

            $command = sprintf('export LC_ALL=C.UTF-8 && export LANG=C.UTF-8 && sudo /usr/bin/python3 ../Scripts/main.py webscan -h "%s" 2>&1', $URL);
            $output = shell_exec($command);
        } else {
            echo("<h3>No URL found, Please try again.</h3>");
            die;
        }
    }
?>


<h1>WebScan - Result</h1>
<br/>
<?php echo(print_r($output)); ?>


<?php
    function test_input($data)
    {
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }
?>

<?php
    include 'footer.php';
?>

<script language="javascript">
    document.title = "Auditing Tool - WebScan";
</script>