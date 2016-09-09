#!/usr/bin/env python3
# coding=utf-8
from jinja2 import Template

head = '''<!doctype html>
<html>
<head>
    <title>Campgrounds Searching</title>
</head>
<body>'''

body = '''
<h2>{% block title %}{{ header1 }}{% endblock %}</h2>
<table>
   <col width="330">
   <col width="580">
   <thead>
       <tr><th>Campground Name</th><th>Avaliable Sites</th></tr>
   </thead>
   <tbody>
       {% for link, name, maplink, col2 in lines %}
       <tr><td><a href={{ link }} target="_blank">{{ name }}</a> [<a href={{ maplink }} target="_blank">Map</a>]</td><td>{{ col2 }}</td></tr>
       {% endfor %}
   </tbody>
</table>'''

tail = '''
</body>
</html>'''

if __name__ == "__main__":
  t = Template(c)

  lines = [("http://www.reserveamerica.com/", "Mono Hot Spring", "http://localhost", "21"), ("http://reserve.america.com", "Pincrest", "http://www.google.com", "14 16 27")]
  with open('results.html', 'w') as f:
    f.write(t.render(header1="Test", lines=lines))
