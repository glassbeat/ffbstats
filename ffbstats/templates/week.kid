<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>DFL Stats - Week View</title>
</head>
<body>
    <span py:if="num" py:strip="">
        <h1>Week #${num}</h1>
        <div py:replace="datagrid(data)"/>
    </span>
    <span py:if="num is None" py:strip="">
        <h1>Select a Week</h1>
        <p py:if="weeks.count() == 0">Sorry, no data has been entered yet.</p>
        <ul py:if="weeks.count() > 0">
            <li py:for="week in weeks">
                <a href="${tg.url('week', num=week.week_num)}">Week $week.week_num</a></li>
        </ul>
    </span>
</body>
</html>