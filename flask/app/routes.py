from app import app
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb.cursors
import config,random

app.secret_key = config.Config.SECRET_KEY
app.config['MYSQL_DB']='bank'
mysql = MySQL(app)
@app.route("/")
@app.route('/login', methods=['GET','POST'])
def login():
    logout()
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM login WHERE id = %s AND pass = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id']=account['cid']
            if account['type']=='e':
                session['e_login'] = True
            elif account['type']=='c':
                session['c_login'] = True
            # Redirect to home page
            return redirect(url_for('welcome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template("includes/login.html", msg=msg)
    
# @app.route("/login")
# def login():
#     return render_template("includes/login.html", e_login=e_login, c_login=c_login)

# @app.route("/index")
# def index():
#     return render_template("index.html")

@app.route("/welcome")
def welcome():
    return render_template("includes/welcome.html")

@app.route("/addCustomer", methods=['GET','POST'])
def addCustomer():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and request.form.get('ssn'):
        ssn = int(request.form['ssn'])
        name = request.form['name']
        age = int(request.form['age'])
        address = request.form['address']
        cid = int(random.randint(100000000, 999999999))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(
                "INSERT INTO customer values(%s,%s,%s,%s,%s)", (ssn, cid, name, address, age))
            mysql.connection.commit()
            msg = "Customer creation initiated successfully"
        except:
            msg="Failed to add Customer. Please try again with different field values!"
            return render_template("includes/addCustomer.html",msg=msg)
        finally:
            cursor.close()
    return render_template("includes/addCustomer.html", msg=msg)


@app.route("/updateCustomer",methods=['GET','POST'])
def updateCustomer():
    msg=''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST" or request.form.get('ssn') or request.form.get('cid'):
        ssn=request.form.get('ssn')
        cid=request.form.get('cid')
        if len(ssn)==0 and len(cid)==0:
            msg="Please enter either SSN or Customer ID"
            return render_template("includes/updateCustomer.html",msg=msg)
        elif ssn and cid:
            cursor.execute("select * from customer where ws_ssn=%s",[ssn])
            res=cursor.fetchone()            
            newName = request.form['newName']
            newAddress = request.form['newAddress']
            newAge = request.form['newAge']
            if len(newName)==0 or len(newAddress)==0 or len(newAge)==0:
                msg="Please enter values in all the fields"
                return render_template("includes/updateCustomer.html",msg=msg,cid=cid,ssn=ssn,name=res['ws_name'], oldAddress=res['ws_adrs'],age=res['ws_age'])
        elif ssn:
            try:
                cursor.execute("select * from customer where ws_ssn=%s",[ssn])
                res=cursor.fetchone()
                return render_template("includes/updateCustomer.html", cid=res['ws_cust_id'], ssn=res['ws_ssn'], name=res['ws_name'], oldAddress=res['ws_adrs'], age=res['ws_age'], msg=msg)
            except:
                msg="SSN not found"
                return render_template("includes/updateCustomer.html",msg=msg)
        elif cid:
            try:
                cursor.execute("select * from customer where ws_cust_id=%s", [cid])
                res = cursor.fetchone()
                return render_template("includes/updateCustomer.html", cid=res['ws_cust_id'], ssn=res['ws_ssn'], name=res['ws_name'], oldAddress=res['ws_adrs'], age=res['ws_age'], msg=msg)
            except:
                msg = "Customer ID not found"
                return render_template("includes/updateCustomer.html", msg=msg)
        try:
            cursor.execute("update customer set ws_adrs=%s,ws_name=%s,ws_age=%s where ws_cust_id=%s",(newAddress,newName,newAge,cid))
            mysql.connection.commit()
            msg = "Customer update initiated successfully"
        except:
            msg = "Failed to update details. Please try again with different field values!"
            return render_template("includes/updateCustomer.html",msg=msg)
        finally:
            cursor.close()
    return render_template("includes/updateCustomer.html",msg=msg)


@app.route("/delCustomer",methods=['GET','POST'])
def delCustomer():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST" or request.form.get('ssn') or request.form.get('custid'):
        ssn = request.form.get('ssn')
        cid = request.form.get('custid')
        if len(ssn) == 0 and len(cid) == 0:
            msg = "Please enter either SSN or Customer ID"
            return render_template("includes/delCustomer.html", msg=msg)
        elif ssn and cid:
            cursor.execute("select * from customer where ws_ssn=%s", [ssn])
            res = cursor.fetchone()
        elif ssn:
            try:
                cursor.execute("select * from customer where ws_ssn=%s", [ssn])
                res = cursor.fetchone()
                return render_template("includes/delCustomer.html", cid=res['ws_cust_id'], ssn=res['ws_ssn'], name=res['ws_name'], age=res['ws_age'], addr=res['ws_adrs'], msg=msg)
            except:
                msg = "SSN not found"
                return render_template("includes/delCustomer.html", msg=msg)
        elif cid:
            try:
                cursor.execute(
                    "select * from customer where ws_cust_id=%s", [cid])
                res = cursor.fetchone()
                return render_template("includes/delCustomer.html", cid=res['ws_cust_id'], ssn=res['ws_ssn'], name=res['ws_name'], age=res['ws_age'], addr=res['ws_adrs'], msg=msg)
            except:
                msg = "Customer ID not found"
                return render_template("includes/delCustomer.html", msg=msg)
        try:
            cursor.execute("delete from customer where ws_cust_id=%s",
                           [res['ws_cust_id']])
            cursor.execute("delete from account where ws_cust_id=%s",[res['ws_cust_id']])
            mysql.connection.commit()
            msg = "Customer deletion initiated successfully"
        except:
            msg = "Failed to delete Customer. Please try again later!"
            return render_template("includes/delCustomer.html", msg=msg)
        finally:
            cursor.close()
    return render_template("includes/delCustomer.html", msg=msg)
    
    
    
    # msg=''
    # cursor= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # if request.method=="POST" and request.form.get('ssn'):
    #     ssn=request.form['ssn']
    #     cid=request.form['custid']
    #     name=request.form['name']
    #     age=request.form['age']
    #     addr=request.form['addr']
    #     try:
    #         cursor.execute("select * from customer where ws_ssn=%s and ws_cust_id=%s and ws_name=%s and ws_adrs=%s and ws_age=%s",
    #                        (ssn, cid, name, addr, age))
    #         res=cursor.fetchone()
    #         print(res)
    #         if res:
    #             cursor.execute("delete from customer where ws_ssn=%s",(ssn,))
    #             mysql.connection.commit()
    #             msg = "Customer deletion initiated successfully"
    #         else:
    #             msg = "No customer found with the entered details. Delete operation failed!"
    #             return render_template("includes/delCustomer.html",msg=msg)
    #     except:
    #         msg="System under maintenance. Try again later."
    #         return render_template("includes/delCustomer.html", msg=msg)
    #     finally:
    #         cursor.close()
    # return render_template("includes/delCustomer.html",msg=msg)


@app.route("/crAccount",methods=['GET','POST'])
def crAccount():
    msg=''
    if request.method == "POST" and request.form.get('cid'):
        cid=request.form['cid']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from customer where ws_cust_id=%s",[cid])
            res=cursor.fetchone()
            if res:
                cust_id=res['ws_cust_id']
                accnt_id=int(random.randint(100000000, 999999999))
                acnt_type=request.form['type']
                amt=request.form['amount']
                # print(cust_id,accnt_id,acnt_type,amt)
                cursor.execute("INSERT INTO account(ws_cust_id,ws_acct_id,ws_acct_type,ws_acct_balance) values(%s,%s,%s,%s)", (cust_id, accnt_id, acnt_type, amt))
                mysql.connection.commit()
                msg = "Account creation initiated successfully"
                return render_template("includes/crAccount.html",msg=msg)
            else:
                msg="Customer not registered. Cannot create Account"
                return render_template("includes/crAccount.html",msg=msg)
        except Exception as e:
            msg=e
            # msg="Something went wrong. Please try again later!"
    return render_template("includes/crAccount.html",msg=msg)


@app.route("/delAccount",methods=['GET','POST'])
def delAccount():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST" or request.form.get('ssn') or request.form.get('cid'):
        ssn = request.form.get('ssn')
        cid = request.form.get('cid')
        if len(ssn) == 0 and len(cid) == 0:
            msg = "Please enter either SSN or Customer ID"
            return render_template("includes/delAccount.html", msg=msg)
        elif ssn and cid:
            cursor.execute("select * from account where ws_cust_id=%s", [cid])
            res = cursor.fetchone()
        elif ssn:
            try:
                cursor.execute("select * from customer where ws_ssn=%s", [ssn])
                res = cursor.fetchone()
                cursor.execute("select * from account where ws_cust_id=%s",[res['ws_cust_id']])
                res1=cursor.fetchone()
                return render_template("includes/delAccount.html", cid=res['ws_cust_id'], ssn=res['ws_ssn'],accnt_id=res1['ws_acct_id'],accnt_type=res1['ws_acct_type'], msg=msg)
            except:
                msg = "SSN not found"
                return render_template("includes/delAccount.html", msg=msg)
        elif cid:
            try:
                cursor.execute(
                    "select * from customer where ws_cust_id=%s", [cid])
                res = cursor.fetchone()
                cursor.execute(
                    "select * from account where ws_cust_id=%s", [cid])
                res1 = cursor.fetchone()
                return render_template("includes/delAccount.html", cid=res['ws_cust_id'], ssn=res['ws_ssn'],accnt_id=res1['ws_acct_id'],accnt_type=res1['ws_acct_type'], msg=msg)
            except:
                msg = "Customer ID not found"
                return render_template("includes/delAccount.html", msg=msg)
        try:
            cursor.execute("delete from account where ws_cust_id=%s",
                           [res['ws_cust_id']])
            mysql.connection.commit()
            msg = "Account deletion initiated successfully"
        except:
            msg = "Failed to delete Account. Please try again later!"
            return render_template("includes/delAccount.html", msg=msg)
        finally:
            cursor.close()
    return render_template("includes/delAccount.html",msg=msg)


@app.route("/cStatus",methods=['GET','POST'])
def cStatus():
    return render_template("includes/cStatus.html")


@app.route("/aStatus")
def aStatus():
    return render_template("includes/aStatus.html")


@app.route("/cSearch",methods=['GET','POST'])
def cSearch():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST" or request.form.get('ssn') or request.form.get('cid'):
        ssn = request.form.get('ssn')
        cid = request.form.get('cid')
        if len(ssn) == 0 and len(cid) == 0:
            msg = "Please enter either SSN or Customer ID"
            return render_template("includes/cSearch.html", msg=msg)
        elif ssn and cid:
            cursor.execute("select * from customer where ws_cust_id=%s", [cid])
            res = cursor.fetchone()
            cursor.execute(
                "select * from account where ws_cust_id=%s", [res['ws_cust_id']])
            res1 = cursor.fetchone()
            msg="Customer Found"
            return render_template("includes/cSearch.html", name=res['ws_name'], cid=res['ws_cust_id'], ssn=res['ws_ssn'], accnt_id=res1['ws_acct_id'], accnt_type=res1['ws_acct_type'], msg=msg)
        elif ssn:
            try:
                cursor.execute("select * from customer where ws_ssn=%s", [ssn])
                res = cursor.fetchone()
                cursor.execute(
                    "select * from account where ws_cust_id=%s", [res['ws_cust_id']])
                res1 = cursor.fetchone()
                return render_template("includes/cSearch.html", name=res['ws_name'],cid=res['ws_cust_id'], ssn=res['ws_ssn'], accnt_id=res1['ws_acct_id'], accnt_type=res1['ws_acct_type'], msg=msg)
            except:
                msg = "SSN not found"
                return render_template("includes/cSearch.html", msg=msg)
        elif cid:
            try:
                cursor.execute(
                    "select * from customer where ws_cust_id=%s", [cid])
                res = cursor.fetchone()
                cursor.execute(
                    "select * from account where ws_cust_id=%s", [cid])
                res1 = cursor.fetchone()
                return render_template("includes/cSearch.html", name=res['ws_name'], cid=res['ws_cust_id'], ssn=res['ws_ssn'], accnt_id=res1['ws_acct_id'], accnt_type=res1['ws_acct_type'], msg=msg)
            except:
                msg = "Customer ID not found"
                return render_template("includes/cSearch.html", msg=msg)
        
    return render_template("includes/cSearch.html", msg=msg)


@app.route("/aSearch", methods=['GET', 'POST'])
def aSearch():
    msg = ''
    found=False
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST" or request.form.get('aid') or request.form.get('cid'):
        aid = request.form.get('aid')
        cid = request.form.get('cid')
        typ=request.form.get('type')
        if len(aid) == 0 and len(cid) == 0:
            msg = "Please enter either Account ID or Customer ID"
            return render_template("includes/aSearch.html", msg=msg)
        elif aid and cid:
            cursor.execute(
                "select * from account where ws_acct_id=%s", [aid])
            res = cursor.fetchone()
            cursor.execute(
                "select * from customer where ws_cust_id=%s", [res['ws_cust_id']])
            res1 = cursor.fetchone()
            msg = "Account Found"
            found=True
            session['aid']=aid
            session['lstbalance']=res['ws_acct_balance']
            return render_template("includes/aSearch.html", cid=res['ws_cust_id'], aid=res['ws_acct_id'], accnt_type=res['ws_acct_type'], msg=msg, balance=res['ws_acct_balance'],found=found)
                
        elif aid:
            try:
                cursor.execute(
                    "select * from account where ws_acct_id=%s", [aid])
                res = cursor.fetchone()
                found=True
                session['lstbalance']=res['ws_acct_balance']
                session['aid']=aid
                return render_template("includes/aSearch.html", cid=res['ws_cust_id'], aid=res['ws_acct_id'], accnt_type=res['ws_acct_type'],balance=res['ws_acct_balance'], msg=msg,found=found)
            except:
                msg = "Account ID not found"
                return render_template("includes/aSearch.html", msg=msg)
        elif cid:
            try:
                cursor.execute(
                    "select * from account where ws_cust_id=%s", [cid])
                res = cursor.fetchall()
                if len(res)==2:
                    typ_list=[res[0]['ws_acct_type'], res[1]['ws_acct_type']]
                    if typ_list[0]=="Savings":
                        msg="Found 2 Accounts. Savings=%s and Current=%s. Select one." % (res[0]['ws_acct_id'],res[1]['ws_acct_id'])
                    else:
                        msg = "Found 2 Accounts. Savings=%s and Current=%s. Select one.", (
                            res[1]['ws_acct_id'], res[0]['ws_acct_id'])
                    return render_template("includes/aSearch.html",cid=cid,msg=msg)
                else:
                    found=True
                    session['aid']=res[0]['ws_acct_id']
                    session['lstbalance']=res[0]['ws_acct_balance']
                    return render_template("includes/aSearch.html", cid=res[0]['ws_cust_id'], aid=res[0]['ws_acct_id'], accnt_type=res[0]['ws_acct_type'], balance=res[0]['ws_acct_balance'], msg=msg, found=found)
            except:
                msg = "Customer ID not found"
                return render_template("includes/aSearch.html", msg=msg)

    return render_template("includes/aSearch.html", msg=msg)


@app.route("/deposit",methods=['GET','POST'])
def deposit():
    msg = ''
    done = False
    prevBal=session['lstbalance']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST" and request.form.get('amount'):
        amount=request.form['amount']
        try:
            cursor.execute("select * from account where ws_acct_id=%s",[session['aid']])
            bal= cursor.fetchone()
            prevBal=bal['ws_acct_balance']
            cursor.execute("update account set ws_acct_balance = ws_acct_balance + %s where ws_acct_id = %s",(amount,session['aid']))
            mysql.connection.commit()
            cursor.execute("select * from account where ws_acct_id=%s",[session['aid']])
            res= cursor.fetchone()
            msg = "Amount deposited successfully"
            done=True
            prevBal+=int(amount)
            return render_template("includes/deposit.html", aid=res['ws_acct_id'], cid=res['ws_cust_id'], balance=prevBal-int(amount),latest_bal=res['ws_acct_balance'],msg=msg,done=done)
        except:
            msg="Deposit Failed. Try again later!"
            return render_template("includes/deposit.html",msg=msg, done=done)
    else:    
        cursor.execute("select * from account where ws_acct_id=%s",[session['aid']])
        res = cursor.fetchone()
        return render_template("includes/deposit.html", aid=res['ws_acct_id'], cid=res['ws_cust_id'], balance=prevBal, msg=msg, done=done)


@app.route("/withdraw",methods=['GET','POST'])
def withdraw():
    msg = ''
    done = False
    prevBal = session['lstbalance']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST" and request.form.get('amount'):
        amount = request.form['amount']
        try:
            cursor.execute(
                "select * from account where ws_acct_id=%s", [session['aid']])
            bal = cursor.fetchone()
            prevBal = bal['ws_acct_balance']
            if prevBal-int(amount)>0:
                cursor.execute(
                    "update account set ws_acct_balance = ws_acct_balance - %s where ws_acct_id = %s", (amount, session['aid']))
                mysql.connection.commit()
                cursor.execute(
                    "select * from account where ws_acct_id=%s", [session['aid']])
                res = cursor.fetchone()
                msg = "Amount withdrawn successfully"
                done = True
                prevBal -= int(amount)
                return render_template("includes/withdraw.html", aid=res['ws_acct_id'], balance=prevBal+int(amount), latest_bal=res['ws_acct_balance'], msg=msg, done=done)
            else:
                msg = "Withdraw not allowed, please choose smaller amount"
                return render_template("includes/withdraw.html", aid=session['aid'], balance=prevBal, msg=msg, done=done)
        except Exception as msg:
            # msg="Deposit Failed. Try again later!"
            return render_template("includes/withdraw.html", msg=msg, done=done)
    else:
        cursor.execute(
            "select * from account where ws_acct_id=%s", [session['aid']])
        res = cursor.fetchone()
        return render_template("includes/withdraw.html", aid=res['ws_acct_id'], cid=res['ws_cust_id'], balance=prevBal, msg=msg, done=done)
    

@app.route("/transfer",methods=['GET','POST'])
def transfer():
    msg = ''
    done = False
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST" and request.form['amount'] and request.form['source'] and request.form['target']:
        amount = request.form['amount']
        source = request.form['source']
        target = request.form['target']
        #Fetch prev Balance
        try:
            cursor.execute("select * from account where ws_acct_id=%s",[source])
            res= cursor.fetchone()
            s_prevBal=res['ws_acct_balance']
            cursor.execute(
                "select * from account where ws_acct_id=%s", [target])
            res = cursor.fetchone()
            t_prevBal = res['ws_acct_balance']
        except Exception as msg:
            return render_template("includes/transfer.html",msg=msg,done=done)
        if s_prevBal-int(amount)>0:
            try:
                cursor.execute("update account set ws_acct_balance = ws_acct_balance - %s where ws_acct_id = %s", (amount, source))
                cursor.execute(
                    "update account set ws_acct_balance = ws_acct_balance + %s where ws_acct_id = %s", (amount, target))
                mysql.connection.commit()
                # Fetch Latest Balance
                cursor.execute("select * from account where ws_acct_id=%s",[source])
                res= cursor.fetchone()
                s_curBal=res['ws_acct_balance']
                cursor.execute(
                    "select * from account where ws_acct_id=%s", [target])
                res = cursor.fetchone()
                t_curBal = res['ws_acct_balance']
                done=True
                msg = "Amount transfer completed successfully"
                return render_template("includes/transfer.html",s_curBal=s_curBal,t_curBal=t_curBal,s_prevBal=s_prevBal,t_prevBal=t_prevBal,msg=msg,done=done,amount=amount,source=source,target=target)
            except Exception as msg:
                return render_template("includes/transfer.html",msg=msg,done=done)
            finally:
                cursor.close()
        else:
            msg="Transfer not allowed, please choose smaller amount"
            return render_template("includes/transfer.html",msg=msg,done=done,source=source,target=target)
    else:
        msg="Please enter Amount, Source and Target Account ID"
        return render_template("includes/transfer.html",msg=msg,done=done)


@app.route("/transacList")
def transacList():
    return render_template("includes/transacList.html")


@app.route("/transacDate")
def transacDate():
    return render_template("includes/transacDate.html")


@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('e_login', False)
   session.pop('c_login', False)
   return redirect(url_for('login'))
