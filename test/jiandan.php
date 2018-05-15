<?php
$link=mysql_connect("localhost","root","root");
mysql_select_db("mcm",$link);
mysql_query("set names utf8");
$sql="SELECT * FROM `outfile` order by f desc limit 10 ";
$res=mysql_query($sql);
echo "quanzhong ---- f------- stnu---roi<br/>";
while($end=mysql_fetch_array($res)){
    /*
    $sql3 = "SELECT * FROM `chazhiqian` WHERE `UNITID` = ".$end['unitid'];
    $res3=mysql_query($sql3);
    $end3=mysql_fetch_array($res3);
    //var_dump($end);
    //var_dump($end3);exit;
    $sql2="UPDATE `outfile` SET stnu = ".($end3['UGDS']/4)." WHERE `UNITID` = ".$end['unitid'];
    //var_dump($sql2);exit;
    $res2=mysql_query($sql2);
    */
    /*echo $end['QUANZHONg']."--";
    $roi = 0.4*10000000*$end['QUANZHONg']/($end['stnu']*50000);
    $f = 0.5*$roi+0.5*$end['QUANZHONg'];
    echo $f."--";
    echo $end['stnu']."--";
    echo $roi."<br/>";
    */
    $quanzhong = (($end['QUANZHONg'] * (1+$end['roi']))* (1+$end['roi']))* (1+$end['roi']);
    echo $quanzhong."<br/>";
    //$sql2="UPDATE `outfile` SET f = ".$f." WHERE `unitid` = ".$end['unitid'];
    //var_dump($sql2);exit;
    //$res2=mysql_query($sql2);
}