<?php
	function connect(){
	//basic SQL functionsf
		$conn=mysqli_connect('localhost','root','123','123');
		return($conn?(mysqli_set_charset($conn,'utf8')?$conn:false):false);
	}
	function insert($tname,$cname,$cvalue){
		$conn=connect();
		if($conn==false){return(false);}
		$sql='INSERT INTO `'.$tname.'`(`';
		for($i=0;$i<count($cname);$i++){
			if($i!=0){$sql.='`,`';}
			$sql.=$cname[$i];
		}
		$sql.='`) VALUES ';
		for($j=0;$j<count($cvalue);$j++){
			if($j!=0){$sql.=',';}
			$sql.='(';
			for($i=0;$i<count($cname);$i++){
				if($i!=0){$sql.=',';}
				$sql.='"'.$cvalue[$j][$i].'"';
			}
			$sql.=')';
		}
		$sql.=';';
		echo $sql;
		$result=mysqli_query($conn,$sql);
		mysqli_close($conn);
		return($result);
	}
	function check_table($tname){
		$conn=connect();
		$sql="SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='".$tname."'";
		$result=mysqli_query($conn,$sql);
		$result=mysqli_fetch_row($result);
		if($result[0]!='0'){mysqli_close($conn);return;}
		else{
			$sql="CREATE TABLE `".$tname."` (`code` varchar(20) NOT NULL,`type_` varchar(10) NOT NULL,`date` varchar(10) NOT NULL,`start`  varchar(10) NOT NULL,`end` varchar(10) NOT NULL,`place` varchar(30) NOT NULL,`people` varchar(30) NOT NULL,`group_` INT,`subgroup` INT)";
			$result=mysqli_query($conn,$sql);
			$sql="ALTER TABLE `".$tname."` ADD PRIMARY KEY (`code`,`type_`,`date`,`start`,`end`,`place`,`people`);";
			$result=mysqli_query($conn,$sql);
		}
		mysqli_close($conn);
	}
	function select_max($tname){
		$conn=connect();
		if($conn==false){return(false);}
		//select * from xxx where 1
		if(true){
			$sql='SELECT MAX(`group`) FROM `'.$tname.'` WHERE 1;';
			$result=mysqli_query($conn,$sql);
			if($result=='false'){return(0);}
			$record=array();
			$count=mysqli_num_rows($result);
			for($i=0;$i<$count;$i++){$record[$i]=mysqli_fetch_row($result);}
			mysqli_close($conn);
			return($record[0][0]);
		}
	}
	function add_course($content){
		$conn=connect();
		insert('course',array('code','title','unit','req','des'),array(array($content[0],$content[1],$content[2],$content[3],$content[4])));
	}
	function add_section($content){
		$conn=connect();
		$tname=substr($content[0],0,4);
		//check_table($tname);
		for($i=0;$i<count($content[5]);$i++){
			for($j=0;$j<count($content[5][$i][0]);$j++){
				if($content[5][$i][0][$j][0]==''){break;}
				insert('schedule',array('code','subcode','place','session','person'),array(array($content[0],$content[5][$i][0][$j][0],$content[5][$i][0][$j][1],$content[5][$i][0][$j][2],$content[5][$i][0][$j][3])));
			}
			for($j=0;$j<count($content[5][$i][1]);$j++){
				if($content[5][$i][1][$j][0]==''){break;}
				insert('schedule',array('code','subcode','place','session','person'),array(array($content[0],$content[5][$i][1][$j][0],$content[5][$i][1][$j][1],$content[5][$i][1][$j][2],$content[5][$i][1][$j][3])));
			}
			$num++;
		}
	}
	if($_SERVER["REQUEST_METHOD"]=="POST"){
		//$file = fopen("data/".time().".txt","w+");
		$temp1=file_get_contents('php://input');
		$temp=json_decode($temp1, true);
		add_course($temp);
		add_section($temp);
	}
?>