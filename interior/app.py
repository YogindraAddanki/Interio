from flask import Flask, session, render_template, request, redirect, url_for,session
from flaskext.mysql import MySQL
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Interio'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/add', methods=['POST'])
def add_product_to_cart():
 cursor = None
 try:
  _quantity = int(request.form['quantity'])
  _code = request.form['code']
  if _quantity and _code and request.method == 'POST':
   conn = mysql.connect()
   cursor = conn.cursor(pymysql.cursors.DictCursor)
   cursor.execute("SELECT * FROM product WHERE code=%s", _code)
   row = cursor.fetchone()
    
   itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'image' : row['image'], 'total_price': _quantity * row['price']}}
    
   all_total_price = 0
   all_total_quantity = 0
   session.modified = True
   if 'cart_item' in session:
    if row['code'] in session['cart_item']:
     for key, value in session['cart_item'].items():
      if row['code'] == key:
       old_quantity = session['cart_item'][key]['quantity']
       total_quantity = old_quantity + _quantity
       session['cart_item'][key]['quantity'] = total_quantity
       session['cart_item'][key]['total_price'] = total_quantity * row['price']
    else:
     session['cart_item'] = array_merge(session['cart_item'], itemArray)
 
    for key, value in session['cart_item'].items():
     individual_quantity = int(session['cart_item'][key]['quantity'])
     individual_price = float(session['cart_item'][key]['total_price'])
     all_total_quantity = all_total_quantity + individual_quantity
     all_total_price = all_total_price + individual_price
   else:
    session['cart_item'] = itemArray
    all_total_quantity = all_total_quantity + _quantity
    all_total_price = all_total_price + _quantity * row['price']
    
   session['all_total_quantity'] = all_total_quantity
   session['all_total_price'] = all_total_price
    
   return redirect(url_for('.products'))
  else:
   return 'Error while adding item to cart'

 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()




#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/bathroom')
def products():
 conn = mysql.connect()
 cursor = conn.cursor(pymysql.cursors.DictCursor)
 try:
  
  cursor.execute("SELECT * FROM product")
  rows = cursor.fetchall()
  return render_template('products.html', products=rows)
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()

@app.route('/empty')
def empty_cart():
 try:
  session.clear()
  return redirect(url_for('.products'))
 except Exception as e:
  print(e)
@app.route('/delete/<string:code>')
def delete_product(code):
 try:
  all_total_price = 0
  all_total_quantity = 0
  session.modified = True
   
  for item in session['cart_item'].items():
   if item[0] == code:    
    session['cart_item'].pop(item[0], None)
    if 'cart_item' in session:
     for key, value in session['cart_item'].items():
      individual_quantity = int(session['cart_item'][key]['quantity'])
      individual_price = float(session['cart_item'][key]['total_price'])
      all_total_quantity = all_total_quantity + individual_quantity
      all_total_price = all_total_price + individual_price
    break
   
  if all_total_quantity == 0:
   session.clear()
  else:
   session['all_total_quantity'] = all_total_quantity
   session['all_total_price'] = all_total_price
   
  return redirect(url_for('.products'))
 except Exception as e:
  print(e)


def array_merge( first_array , second_array ):
 if isinstance( first_array , list ) and isinstance( second_array , list ):
  return first_array + second_array
 elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
  return dict( list( first_array.items() ) + list( second_array.items() ) )
 elif isinstance( first_array , set ) and isinstance( second_array , set ):
  return first_array.union( second_array )
 return False

def sql_connector():
    conn = pymysql.connect(user='root',password='',db='Interio',host='127.0.0.1',port=3306)
    c=conn.cursor()
    return conn,c

@app.route('/',methods=['GET','POST'])
def fu():
    if request.method=='POST':
      user=request.form.get('user')
      psw=request.form.get('psw')
      conn,c=sql_connector()
      c.execute('SELECT * FROM Users WHERE user = %s AND psw = %s',(user,psw) )
      account = c.fetchone()
      if account:
           return render_template('interior/main.html')

      
    return render_template('interior/s.html')


@app.route('/register',methods=['GET','POST'])
def funcc():
    if request.method=='POST':
        firstname=request.form.get('users')
        lastname=request.form.get('Emails')
        email=request.form.get('pswss')
        conn,c = sql_connector()
        c.execute("INSERT INTO Users VALUES ('{}','{}','{}')".format(firstname,lastname,email))
        conn.commit()
        conn.close()
        c.close()
        return render_template('interior/s.html')

@app.route('/ab',methods=['GET','POST'])
def func():
    if request.method=='POST':
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        message=request.form.get('message')
        conn,c = sql_connector()
        c.execute("INSERT INTO Form VALUES ('{}','{}','{}','{}')".format(firstname,lastname,email,message))
        conn.commit()
        conn.close()
        c.close()
    return render_template('interior/main.html')


@app.route('/bathroom')
def bathroom():
    return render_template('/interior/bathroom_.html')

@app.route('/bedroom')
def bedroom():
    return render_template('/interior/bedroom_.html')

@app.route('/hall')
def hall():
    return render_template('/interior/hall_.html')

@app.route('/kitchen')
def kitchen():
    return render_template('/interior/kitchen_.html')

@app.route('/furniture')
def furniture():
    return render_template('/interior/furniture_.html')



@app.route('/painting')
def  painting():
    return render_template('/interior/painting_.html')

@app.route('/login')
def login():
    return render_template('/interior/s.html')

@app.route('/signup')
def signup():
    return render_template('/interior/signup.html')






if __name__ == "__main__":
    app.run(debug=True)