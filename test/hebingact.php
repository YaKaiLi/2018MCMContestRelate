<?php
$link=mysql_connect("localhost","root","root");
mysql_select_db("mcm",$link);
mysql_query("set names utf8");
$sql="SELECT * FROM `chazhiqian`";
$res=mysql_query($sql);
while($end=mysql_fetch_array($res)){
    //var_dump($end);
    $avg = $end['ACTCMMID']+$end['ACTENMID']+$end['ACTMTMID'];
    $avg = $avg/3;
        $sql2="UPDATE chazhiqian SET ACT = '$avg' WHERE `UNITID` = ".$end['UNITID'];
        $res2=mysql_query($sql2);
        var_dump($sql2);
        echo "</br>";
}