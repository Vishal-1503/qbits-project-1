import pandas as pd
import numpy as np
import sqlite3
import uuid
import plotly.express as px
from datetime import datetime



conn = sqlite3.connect('crm.db')
cursor = conn.cursor()
print("=====================================")
print("Database connected successfully")

def login():
  while True:
    print("Enter your name: ")
    name = input()
    user = cursor.execute('SELECT * FROM bda WHERE name = \'{}\''.format(name)).fetchone()
    if user == None:
      print()
      print("Wrong name, try again")
      print()
    else:
      print()
      print("User found..")
      print("Welcome", name, "to the CRM panel")
      break
  return None if user == None else user[0]

def getData(bda_id):
  return cursor.execute('SELECT * FROM sales WHERE bda_id = \'{}\';'.format(bda_id)).fetchall()

def divideLeads(data):
  handled_leads = []
  unhandled_leads = []
  for i in data:
    if i[5] == "0":
      unhandled_leads.append(i)
    else:
      handled_leads.append(i)
  return handled_leads, unhandled_leads

def analyze(bda_id):
  data = getData(bda_id)
  df = pd.DataFrame([i[4] for i in data ], columns=['sales'])
  values = df['sales'].value_counts().to_list()
  names=df['sales'].value_counts().index
  colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', 'red']
  fig = px.pie(df, values=values, names=names, title="Lead Results")
  fig.update_traces(
    textposition='inside', textinfo='percent+label', marker=dict(colors=colors, line=dict(color='#000000', width=1))
  )
  fig.write_html('lead_results.html', auto_open=True)
  print("Analysis done, opening the results in browser....")

def checkout(bda_id):
  today = datetime.now().strftime('%Y-%m-%d')
  results = cursor.execute('SELECT lead_result FROM sales WHERE bda_id = \'{}\' AND lead_status = 1'.format(bda_id)).fetchall()
  rate = 2000
  total_leads = cursor.execute('SELECT COUNT(*) FROM sales WHERE bda_id = \'{}\''.format(bda_id)).fetchone()
  handled = cursor.execute('SELECT COUNT(*) FROM sales WHERE bda_id = \'{}\' AND lead_status = 1'.format(bda_id)).fetchone()
  unhandled = cursor.execute('SELECT COUNT(*) FROM sales WHERE bda_id = \'{}\' AND lead_status = 0'.format(bda_id)).fetchone()
  print("Total leads: ", total_leads[0])
  print("Handled leads: ", handled[0])
  print("Unhandled leads: ", unhandled[0])
  print('Rate per conversion: ', rate)
  counter = 0
  for i in results:
    if i[0] == "Interested":
      counter += 1
  print("Total interested leads: ", counter)
  payout = counter * rate
  print('-----------------------------------------------------------------------------------------------')
  print("Payout: ", payout)
  print('-----------------------------------------------------------------------------------------------')
  cursor.execute('INSERT into bda_payouts VALUES ( ? , ? , ? , ? , ?)', (str(uuid.uuid4()), bda_id, today, 'Salary Paid', payout))
  conn.commit()
  print("Payout done successfully")

bda_id = login()

while True:
  data = getData(bda_id)
  results = divideLeads(data)
  print('-----------------------------------------------------------------------------------------------')
  print("Remaining Leads: {}".format(len(results[1])))
  print("Handled leads: {}".format(len(results[0])))
  print()
  print('-----------------------------------------------------------------------------------------------')
  print()
  print("1. Handle next lead")
  print("2. Show remaining leads")
  print("3. Show handled leads")
  print("4. Analyze")
  print("5. Checkout")
  print("0. Exit")
  print()
  ch = int(input("Enter your choice: "))
  print()
  if ch == 0:
    print("Thank you")
    break
  elif ch == 1:
    current_lead = cursor.execute('SELECT * FROM sales WHERE bda_id = \'{}\' AND lead_status = 0;'.format(bda_id)).fetchone()
    if current_lead == None:
      print("No more leads to handle! Congratulations")
      break
    print()
    print(" Name: {} | Phone number: {}".format(current_lead[2], current_lead[3]))
    print()
    print(" Make the call and enter the result from the options: ")
    print()
    print(" 1. Interested")
    print(" 2. Not Interested")
    print(" 3. Call Back Later")
    print(" 4. DNP (Did Not pick)")
    print(" 5. Junk Lead/Wrong Number")
    res = int(input("Enter the result:"))
    match(res):
      case 1:
        print("Lead is interested")
        answer = "Interested"
      case 2:
        print("Lead is not interested")
        answer = "Not Interested"
      case 3:
        print("Lead asked to Call back later")
        answer = "Call Back Later"
      case 4:
        print("Lead Did Not pick the call")
        answer = "DNP (Did Not pick)"
      case 5:
        print("Lead is junk/wrong number")
        answer = "Junk Lead/Wrong Number"
      case _:
        print("Invalid Option")
        answer = "N/A"
    cursor.execute('UPDATE sales SET lead_status = 1, lead_result = \'{}\' WHERE id = \'{}\';'.format(answer, current_lead[0]))
    conn.commit()
    print()
    print("Lead updated")
  elif ch == 2:
    print('-----------------------------------------------------------------------------------------------')
    print(" ---- Remaining Leads ----")
    print("  Names  | Phone Numbers  ")
    for i in results[1]:
      print(" {} | {} ".format(i[2], i[3]))
    print('-----------------------------------------------------------------------------------------------')
  elif ch == 3:
    print('-----------------------------------------------------------------------------------------------')
    print(" ---- Handled Leads ----")
    print("  Names  | Phone Numbers  ")
    for i in results[0]:
      print(" {} | {} ".format(i[2], i[3]))
    print('-----------------------------------------------------------------------------------------------')
  elif ch == 4:
    analyze(bda_id)
  elif ch == 5:
    checkout(bda_id)
    break
  else:
    print("Wrong option, Try again")