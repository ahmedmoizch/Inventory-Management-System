from flask import Flask, render_template, url_for, request, redirect, session
import mysql.connector
import pandas as pd

app = Flask(__name__)
app.secret_key = "$$"

# Data Base Configration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'inventory'
}


@app.route("/home")
def home():
    
    return render_template('home.html')

@app.route('/reg', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #r_name = request.form.get('r_name')
        r_email = request.form.get('r_email')
        r_pass = request.form.get('r_pass')

        if r_email and r_pass:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            try:
                cursor.execute("insert into login values (%s, %s)", (r_email, r_pass))
                connection.commit()
                print("Data Saved Sucessfully")

            except:
                print(f"Error saving to database: {r_email}")
                connection.rollback()

            finally:
                cursor.close()
                connection.close()

        return redirect(url_for('home'))

    return render_template('reg.html')

@app.route ("/", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        item_id = request.form.get('item_id')
        item_name = request.form.get('item_name')
        item_price = request.form.get('item_price')
        item_wp = request.form.get('item_wp')

        if item_id and item_name and item_price and item_wp:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            
            try:
                cursor.execute("INSERT INTO products (id, item_name, price, wholesale_price) values (%s, %s, %s, %s)",(item_id, item_name, item_price, item_wp))
                connection.commit()
                print(f"Data saved Sucessfully id:{item_id}")

            except Exception as e:
                print(f"Error saving to database: {item_id}")
                connection.rollback()

            finally:
                cursor.close()
                connection.close()
                
        return redirect(url_for('add'))
    

    return render_template('addinv.html')


@app.route("/add", methods=['GET', 'POST'])
def record():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Query
    cursor.execute("Select * from products")
    data = cursor.fetchall()

    qurey = "select * from products"
    # Column Names
    column_names = [desc[0] for desc in cursor.description]

    #df = pd.read_sql_query(qurey, connection)
    #profit = df['Profit'] = df['price'] - df['wholesale_price']
    # Close Connection
    cursor.close()
    connection.close()

    #print(df)

    return render_template("invrecord.html", data=data, columns=column_names)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_email = request.form.get('login_email')
        login_pass = request.form.get('login_pass')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("select exists ( select 1 from login where email = (%s) AND pass = (%s) ) AS is_valid", (login_email ,login_pass))
        #print(sql_data)

        result = cursor.fetchone()
        is_valid = result[0]

        cursor.close()
        connection.close()

        if is_valid == 1:
            print("Login Sucessfull")
            return(redirect(url_for('add')))
        
        else:
            print("Login Unsucessfull")
            return redirect(url_for('login'))

    return render_template('login.html')


if __name__ =="__main__":
    app.run()