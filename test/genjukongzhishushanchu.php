<?php
$link=mysql_connect("localhost","root","root");
mysql_select_db("mcm",$link);
mysql_query("set names utf8");
$sql="SELECT * FROM `maindata`";
$res=mysql_query($sql);
while($end=mysql_fetch_array($res)){
    //var_dump($end);
    $all=0;
    $count=0;
    foreach ($end as $value){
        if($value=="NULL"||$value=="PrivacySuppressed"){
            $count++;
        }
        $all++;
    }

    if($count*2>$all){
        $sql2="delete from `maindata` where `UNITID`=".$end['UNITID'];
        $res2=mysql_query($sql2);
        echo $end['UNITID'];
        echo "<br/>";
    }
}