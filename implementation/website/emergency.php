<?php
    function callAPI($collection){
        $url = "https://webhooks.mongodb-stitch.com/api/client/v2.0/app/irtcp-qsdyo/service/getData/incoming_webhook/webhook0?collection=".$collection;
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        $result = curl_exec($curl);
        if(!$result){die("Connection Failure");}
        curl_close($curl);
        return $result;
    }
    $get_data = callAPI("emergency");
    $response = json_decode($get_data,true);
     
    $data = $response['documents'];
    foreach ($data as $tweet) {
        echo $tweet["tweet"] . "\n";
    }	

    foreach ($data as $tweet) {
        echo "<tr><td style='color:black' width='180%'>";
        echo $tweet["tweet"];
        echo "</td><td width='20%'><button type='button' class='btn btn-info add'><b>Reply</b></button></td>";
        echo "<td class='value'><input type='hidden' id='tweet_value' class='myval' name='tweet_value' value=".$tweet["tweet_id"]."></td></tr>";
        $i++;
    }
?>
