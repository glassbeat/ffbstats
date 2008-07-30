<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>DFL Stats - Team View</title>
</head>
<body>
    <h1>Team List</h1>
    <div py:replace="datagrid(data)"/>
    <div class="legend"><p>P=Total Points, OP=Total Optimum Points, W=Wins,
        L=Losses, OW=Optimal Lineup Wins, OL=Optimal Lineup Losses</p></div>
    
</body>
</html>
