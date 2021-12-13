#!/usr/bin/python37all

import cgi
import json
from urllib.request import urlopen
from urllib.parse import urlencode

api = "74W76Q5E82V1O8GG"          # Thingspeak API key

data = cgi.FieldStorage()         # get CGI POST data
angle = data.getvalue('angle')    # extract angle value
speed = data.getvalue('speed')    # extract angle value

# write angle to the file:
with open('stepper_control.txt', 'w') as f:
  if "zero" in data:                     # zero button pressed, so
    data = {"angle":-1, "speed":speed}   # set angle to -1
    angle = "0"
  else:
    data = {"angle":angle, "speed":speed}
  json.dump(data,f)

# send data to Thingspeak:
params = urlencode({"api_key":api, 1: int(angle)})
url = "https://api.thingspeak.com/update?" + params
response = urlopen(url)      # open the URL to send the request

# generate new web page:
print("Content-type: text/html\n\n")
print("""
<html>
<form action="/cgi-bin/stepper_control.cgi" method="POST">
<b>Angle:</b>
<input type="range" name="angle" min ="0" max="360" value =\"""",end='')

print(angle, end='')    # display range element with current angle

print("""\"><br>

<b>Speed:</b>
<input type="range" name="angle" min ="0" max="100" value =\"""",end='')

print(speed, end='')    # display range element with current speed

print("""\"><br>

<input type="submit" name="go" value="Go to angle">
<input type="submit" name="zero" value="Zero system">
</form>
<br>
<iframe width="450" height="260" style="border: 1px solid #cccccc;" 
src="https://thingspeak.com/channels/1226469/charts/1?bgcolor=%23ffffff&
color=%23d62020&dynamic=true&title=Field+1+Line+Chart&type=line"></iframe>
<br>
<iframe width="450" height="260" style="border: 1px solid #cccccc;" 
src="https://thingspeak.com/channels/1226469/widgets/238278"></iframe>
</html>
""")