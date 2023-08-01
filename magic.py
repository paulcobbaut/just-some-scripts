#!/usr/bin/python3
import cgi
import datetime
import mysql.connector

def write_html_header():
  html = []
  html.append('<!DOCTYPE html>')
  html.append('<html>')
  html.append('<head>')
  html.append('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
  html.append('<title>Wereldkampioenschap Magic The Gathering</title>')
  html.append('</head>')
  html.append('<body>')
  html.append('<a href="http://raspberrypi/magic.py">Magic</a>')
  html.append('<br/>')
  return "\n".join(html)

def write_html_footer():
  html = []
  html.append('<p>PC</p></body></html>')
  return "\n".join(html)

###############################################################################
#                                   FORM                                      #
###############################################################################
def write_html_form(teams):
  html = []
  html.append('<form method="get">')
  html.append('<label>Uitslag(thuis-uit):</label>')
  html.append('<select name="thuisploeg" id="thuisploeg">')
  for i in range(len(teams)):
    html.append('  <option value="' + teams[i] + '">' + teams[i] + '</option>')
  html.append('</select>')
  html.append('<input type="number" id="thuisscore" name="thuisscore" value="0" style="width: 4em">')
  html.append('<select name="uitploeg" id="uitploeg">')
  for i in range(len(teams)):
    html.append('  <option value="' + teams[i] + '">' + teams[i] + '</option>')
  html.append('</select>')
  html.append('<input type="number" id="uitscore" name="uitscore" value="0" style="width: 4em">')
  html.append('<input type="submit" value="Submit">')
  html.append('</form>')
  return "\n".join(html)

def write_html_uitslagen(sqltablename, sqltabledesc):
  with mysql.connector.connect( host="127.0.0.1", user="root", password="hunter2", database="magic"
  ) as mydb:
    mycursor = mydb.cursor()
    query = "SELECT thuisploeg, thuisscore, uitploeg, uitscore FROM " + sqltablename
    mycursor.execute(query)
    myresult = mycursor.fetchall()
  html = []
  html.append('<table><td>') # layout table
  html.append('<table border=1>')
  html.append('<tr><th colspan=7>' + sqltabledesc + ' Uitslagen</th></tr>')
  html.append('<tr><th>Thuisploeg</th><th>Thuisscore</th><th>Uitploeg</th><th>Uitscore</th></tr>')
  for record in myresult:
    thuisploeg, thuisscore, uitploeg, uitscore = record
    html.append( f'<tr>')
    html.append( f'<td>{thuisploeg}</td><td>{thuisscore}</td><td>{uitploeg}</td><td>{uitscore}</td>')
    html.append( f'</tr>')
  html.append('</table>')
  html.append('</td>') # layout table
  return "\n".join(html)

def add_to_table(sqltablename, thuisploeg, thuisscore, uitploeg, uitscore):
  with mysql.connector.connect( host="127.0.0.1", user="root", password="hunter2", database="magic"
  ) as mydb:
    mycursor = mydb.cursor()
    today = datetime.datetime.now()
    query = "INSERT INTO " + sqltablename + " VALUES ('" + thuisploeg + "', " + thuisscore + ", '" + uitploeg + "', " + uitscore +  ")"
    mycursor.execute(query)
    mydb.commit()
    mydb.close()

def write_html_stand(sqltablename, sqltabledesc, teams):
  with mysql.connector.connect( host="127.0.0.1", user="root", password="hunter2", database="magic"
  ) as mydb:
    mycursor = mydb.cursor()
    query = "SELECT thuisploeg, thuisscore, uitploeg, uitscore FROM " + sqltablename
    mycursor.execute(query)
    myresult = mycursor.fetchall()
  wins       = [0,0,0,0,0,0,0,0]
  lost       = [0,0,0,0,0,0,0,0]
  winspoints = [0,0,0,0,0,0,0,0]
  lostpoints = [0,0,0,0,0,0,0,0]
  gamecount  = [0,0,0,0,0,0,0,0]
  for record in myresult:
    thuisploeg, thuisscore, uitploeg, uitscore = record
    if int(thuisscore) > 0:
        gamecount[teams.index(thuisploeg)] += 1
        gamecount[teams.index(uitploeg)] += 1
        wins[teams.index(thuisploeg)] += 1
        lost[teams.index(uitploeg)] += 1
        winspoints[teams.index(thuisploeg)] += thuisscore
        lostpoints[teams.index(uitploeg)] += thuisscore
    if int(uitscore) > 0:
        gamecount[teams.index(uitploeg)] += 1
        gamecount[teams.index(thuisploeg)] += 1
        wins[teams.index(uitploeg)] += 1
        lost[teams.index(thuisploeg)] += 1
        winspoints[teams.index(uitploeg)] += uitscore
        lostpoints[teams.index(thuisploeg)] += uitscore
  # punten en leven overschot en leven tegenstand
  ranking_list = []
  for i in range(len(teams)):
    ranking_list.append((teams[i],wins[i],lost[i],winspoints[i],lostpoints[i],gamecount[i]))
  # sorteer op wins, dan op winspoints, dan op lostpoints
  sorted_data = sorted(ranking_list, key=lambda x: (x[1], x[2], x[3]), reverse=True)
  # zet in HTML tabel
  html = []
  html.append('<td>&nbsp</td><td>') # layout table
  html.append('<table border=1>')
  html.append('<tr><th colspan=7>' + sqltabledesc + ' Stand</th></tr>')
  html.append('<tr><th>Deck</th><th>AW</th><th>WG</th><th>WV</th><th>EL</th><th>AL</th><th>SL</th></tr>')
  for item in sorted_data:
    html.append( f'<tr>')
    html.append( f'<td>' + str(item[0]) + '</td><td>' + str(item[5]) + '</td><td>' + str(item[1]) + '</td><td>' + str(item[2]) + '</td><td>' + str(item[3]) + '</td><td>' + str(item[4]) + '</td><td>' + str(item[3] - item[4]) + '</td>')
    html.append( f'</tr>')
  html.append('</table>')
  html.append('<br/>AW = Aantal wedstrijden afgewerkt')
  html.append('<br/>WG = Aantal wedstrijden gewonnen')
  html.append('<br/>WV = Aantal wedstrijden verloren')
  html.append('<br/>EL = Eigen Leven bij winst opgeteld')
  html.append('<br/>AL = Andere hun leven bij verlies opgeteld')
  html.append('<br/>SL = Saldo leven bij winst - leven bij verlies')
  html.append('</td></table>') # layout table
  html.append('<br/>')
  return "\n".join(html)


################################################################################
#                                    START                                     #
################################################################################
print('Content-type: text/html\n')
form = cgi.FieldStorage()
print(write_html_header())

sqltablename = "eersteklasse2023"
sqltabledesc = "Eerste Klasse 2023"
teams = ["Boemboem" ,"Cocktail" ,"Disrespect" ,"Goblin" ,"Mana Sliver" ,"Merfolk" ,"Shady" ,"Unexpected Alliance"]
if "thuisploeg" in form:
  if form["thuisploeg"].value in teams:
    add_to_table(sqltablename, form["thuisploeg"].value, form["thuisscore"].value, form["uitploeg"].value, form["uitscore"].value)
print(write_html_form(teams))
print(write_html_uitslagen(sqltablename, sqltabledesc))
print(write_html_stand(sqltablename, sqltabledesc, teams))


sqltablename = "tweedeklasse2023"
sqltabledesc = "Tweede Klasse 2023"
teams = ["Black Life" ,"Counter Sliver" ,"False One" ,"Olifant" ,"Pestilence" ,"Prisma" ,"Taptap" ,"Taken"]
if "thuisploeg" in form:
  if form["thuisploeg"].value in teams:
    add_to_table(sqltablename, form["thuisploeg"].value, form["thuisscore"].value, form["uitploeg"].value, form["uitscore"].value)
print(write_html_form(teams))
print(write_html_uitslagen(sqltablename, sqltabledesc))
print(write_html_stand(sqltablename, sqltabledesc, teams))


sqltablename = "derdeklasseA2023"
sqltabledesc = "Derde Klasse A 2023"
teams = ["BOB" ,"Creapy Crawly" ,"Blacky" ,"Natures Revolt" ,"Ratten" ,"UnUn"]
if "thuisploeg" in form:
  if form["thuisploeg"].value in teams:
    add_to_table(sqltablename, form["thuisploeg"].value, form["thuisscore"].value, form["uitploeg"].value, form["uitscore"].value)
print(write_html_form(teams))
print(write_html_uitslagen(sqltablename, sqltabledesc))
print(write_html_stand(sqltablename, sqltabledesc, teams))


sqltablename = "derdeklasseB2023"
sqltabledesc = "Derde Klasse B 2023"
teams = ["Black Arts" ,"Rebels" ,"Recycle" ,"Swampwalk" ,"Sunny" ,"Two Battle"]
if "thuisploeg" in form:
  if form["thuisploeg"].value in teams:
    add_to_table(sqltablename, form["thuisploeg"].value, form["thuisscore"].value, form["uitploeg"].value, form["uitscore"].value)
print(write_html_form(teams))
print(write_html_uitslagen(sqltablename, sqltabledesc))
print(write_html_stand(sqltablename, sqltabledesc, teams))


sqltablename = "derdeklasseC2023"
sqltabledesc = "Derde Klasse C 2023"
teams = ["42" ,"Disyarded" ,"KZB" ,"Life Sliver" ,"Teamwork" ,"Tisonolle"]
if "thuisploeg" in form:
  if form["thuisploeg"].value in teams:
    add_to_table(sqltablename, form["thuisploeg"].value, form["thuisscore"].value, form["uitploeg"].value, form["uitscore"].value)
print(write_html_form(teams))
print(write_html_uitslagen(sqltablename, sqltabledesc))
print(write_html_stand(sqltablename, sqltabledesc, teams))


print(write_html_footer())


