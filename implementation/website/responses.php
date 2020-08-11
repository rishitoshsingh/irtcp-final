<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
.accordion {
    background-color: #eee;
    color: #444;
    cursor: pointer;
    padding: 18px;
    width: 100%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 15px;
    transition: 0.4s;
}

.active, .accordion:hover {
    background-color: #ccc;
}

.accordion:after {
    content: '\002B';
    color: #777;
    font-weight: bold;
    float: right;
    margin-left: 5px;
}

.active:after {
    content: "\2212";
}

.panel {
    padding: 0 18px;
    background-color: white;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.2s ease-out;
}
</style>
</head>
<body>

<h1 style="text-align:center">Addressed Complaints</h1>
<hr>


<?php
    $servername = "127.0.0.1";
    $username = "rishi";
    $password = "";
    $database = "project";

    $conn = new mysqli($servername, $username, $password,$database);
	    mysqli_query("SET TEXTSIZE 2147483647");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
	mysqli_query("SET TEXTSIZE 2147483647");


     $query = "SELECT * FROM tweets,reply WHERE tweets.reply_status=1 and tweets.tweet_id=reply.tweet_id";
     $res = mysqli_query($conn,$query);
	if(mysqli_num_rows($res)>0){
		while($r = mysqli_fetch_array($res)){
			echo "<button class='accordion'>".$r['tweet']."</button>";
 			echo "<div class='panel'><p style='text-align:center;'>".$r['ans']."</p>";
			echo "<hr width='80%'><div style='width:45%;float:left;'><p style='margin-left:50%;'> Category :";
			if($r['prediction']==0)
				echo "Feedback";
			else
				echo "Emergency";
			echo "</div>";
			echo "<div style='width:45%;float:left;'><p style='margin-left:50%;'> Tweeted By :".$r['username']."</div>";
			echo "<div style='clear:both'></div>";
			echo "</div>";

	}
}

?>
<!--

<h1 style="text-align:center">Addressed Complaints</h1>
<hr>
<button class="accordion">Section 1</button>
<div class="panel">
  <p style="text-align:center;">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
  <hr width="80%">
  <div style="width:45%;float:left;">
    <p style="margin-left:50%;"> Category :
  </div>
  <div style="width:45%;float:left;">
    <p style="margin-left:50%;"> Tweeted By :
  </div>
  <div style="clear:both"></div>
</div>

<button class="accordion">Section 2</button>
<div class="panel">
  <p style="text-align:center;">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
  <hr width="80%">
  <div style="width:45%;float:left;">
    <p style="margin-left:50%;"> Category :
  </div>
  <div style="width:45%;float:left;">
    <p style="margin-left:50%;"> Tweeted By :
  </div>
  <div style="clear:both"></div>
</div>
-->
<script>
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}
</script>

</body>
</html>
