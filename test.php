<?php
    $fp = fopen('itinerary.json', 'w');
    fwrite($fp, json_encode($_POST));
    fclose($fp);
?>