<?php
$link=mysql_connect("localhost","root","root");
mysql_select_db("mcm",$link);
mysql_query("set names utf8");
$sql="SELECT * FROM `outfile`";
$res=mysql_query($sql);
while($end=mysql_fetch_array($res)){
    //var_dump($end);
    //if($end['CURROPER']==0){
    //if($end['DISTANCEONLY']==1){
    if($end['stnu']<100){
        $sql2="delete from `outfile` where `id`=".$end['id'];
        $res2=mysql_query($sql2);
        echo $end['UNITID'];
        echo "<br/>";
    }
}