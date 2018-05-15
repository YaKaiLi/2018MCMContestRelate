<?php
$link=mysql_connect("localhost","root","root");
mysql_select_db("mcm",$link);
mysql_query("set names utf8");
$sql="SELECT * FROM `seseds`";
$res=mysql_query($sql);
while($end=mysql_fetch_array($res)){
    //var_dump($end);exit;
    if(($end[0]=="SOTCB")||($end[0]=="NUETB")||($end[0]=="HYTCP")||($end[0]=="WYTCB")||($end[0]=="GETCB")||($end[0]=="WWTCB")||($end[0]=="FFTCB")) {
        $sql2 = "INSERT INTO `sesedsneed` VALUES ('$end[0]','$end[1]','$end[2]','$end[3]')";
        $res2 = mysql_query($sql2);
        var_dump($sql2);
        echo "</br>";
    }
}