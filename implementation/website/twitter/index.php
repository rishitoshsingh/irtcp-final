
<?php
ini_set('display_errors', 1);
require_once('TwitterAPIExchange.php');

//   $servername = "127.0.0.1";
  //  $username = "root";
   // $password = "root";
   // $database = "twitter";

  //  $conn = new mysqli($servername, $username, $password,$database);
   // if ($conn->connect_error) {
    //    die("Connection failed: " . $conn->connect_error);
   // } 


$settings = array(
    'oauth_access_token' => "Insert your key",
    'oauth_access_token_secret' => "Insert your key",
   'consumer_key' => "Insert your key",
    'consumer_secret' => "Insert your key"
);
$twitter = new TwitterAPIExchange($settings);

$status_id = urldecode($_GET['tweet_id']);
$m = urldecode($_GET['tweet_reply']);
$screen = urldecode($_GET['screen_name']);

$message="@".$screen." ".$m;
$postfields = array( 
    'status' => $message,
    'in_reply_to_status_id'=> $status_id,
);

$url = 'https://api.twitter.com/1.1/statuses/update.json';
$requestMethod = 'POST';
if($twitter->buildOauth($url, $requestMethod)
             ->setPostfields($postfields)
             ->performRequest())
{
    $postData = array(
        'tweet_id' => urldecode($_GET['tweet_id']),
        'reply' => urldecode($_GET['tweet_reply']),
    );
    
    $ch = curl_init('https://webhooks.mongodb-stitch.com/api/client/v2.0/app/irtcp-qsdyo/service/replyTweet/incoming_webhook/webhoot_test?secret=passkey');
    curl_setopt_array($ch, array(
        CURLOPT_POST => TRUE,
        CURLOPT_RETURNTRANSFER => TRUE,
        CURLOPT_HTTPHEADER => array(
            'Content-Type: application/json'
        ),
        CURLOPT_POSTFIELDS => json_encode($postData)
    ));
    $response = curl_exec($ch);
    
}
else
    echo "400";
?>
