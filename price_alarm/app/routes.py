import sys
from utils import *
from flask import Flask, render_template, request, flash, redirect, url_for
from forms import *
from flask_bootstrap import Bootstrap

app = Flask(__name__) 
Bootstrap(app)

app.secret_key = 'development key'
g_db_file = './data.db'

@app.route("/", methods=['GET','POST'])
def settings():

  form = SettingsForm(request.form)




  
  if request.method == 'POST' : #or request.method == 'GET':

    rate = request.form ['cny_rate']
    print (rate)
    if form.validate() == False:
      flash('All fields are required.')
      print ("validate failed")
      return render_template('settings.html', form=form)
    else:
      print ('validate ok')
      data = (
          form.cny_rate.data,
          form.price_diff_on.data,
          form.price_diff_value.data,
          form.price_minus_diff_value.data,
        )
      print (data)
      conn = open_db (g_db_file)
      update_settings_table (
        conn,
        data
       )
      close_db (conn)
      redirect('settings')
      return render_template('settings.html', form=form)

 
  elif request.method == 'GET':
    conn = open_db (g_db_file)
    settings = read_settings_table(conn)
    close_db(conn)
    rate = settings[0] [0]
    db_price_diff_on = settings[0] [1]
    db_price_diff_value = settings[0] [2]
    db_price_minus_diff_value = settings[0] [3]
    form.setValue (rate, db_price_diff_on, db_price_diff_value, db_price_minus_diff_value)
    return render_template('settings.html', form=form)
  

if __name__ == '__main__':
  if len (sys.argv) == 2:
    g_db_file = sys.argv [1]

  create_db (g_db_file)    
  app.run(host='0.0.0.0', port='80')
