<?php
    include 'header.php';
?>

<?php
    $ips;

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        if (!empty($_POST["ips"])) {
            $ips = test_input($_POST["ips"]);
            #print_r($ipArray);

            shell_exec("export LC_ALL=C.UTF-8");
            shell_exec("export LANG=C.UTF-8");
            # sudo python3 ../Scripts/main.py netscan -h 127.0.0.1 2>&1
            $command = sprintf('export LC_ALL=C.UTF-8 && export LANG=C.UTF-8 && sudo /usr/bin/python3 ../Scripts/main.py netscan -h "%s" 2>&1', $ips);
            $output = shell_exec($command);

            #$output = json_encode($output);

            #echo("<br/>");
            
            //call python script and process output.
        } else {
            echo("<h3>No IP found, Please try again.</h3>");
            die;
        }
    }
?>


<h1>NetScan - Result</h1>
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
    document.title = "Auditing Tool - NetScan";
</script>