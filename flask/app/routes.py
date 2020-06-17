from app import app
from flask import render_template

e_login=True
c_login=False
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",e_login=e_login,c_login=c_login)


@app.route("/addCustomer")
def addCustomer():
    return render_template("includes/addCustomer.html", e_login=e_login, c_login=c_login)


@app.route("/updateCustomer")
def updateCustomer():
    return render_template("includes/updateCustomer.html", e_login=e_login, c_login=c_login)


@app.route("/delCustomer")
def delCustomer():
    return render_template("includes/delCustomer.html", e_login=e_login, c_login=c_login)


@app.route("/crAccount")
def crAccount():
    return render_template("includes/crAccount.html", e_login=e_login, c_login=c_login)


@app.route("/delAccount")
def delAccount():
    return render_template("includes/delAccount.html", e_login=e_login, c_login=c_login)


@app.route("/cStatus")
def cStatus():
    return render_template("includes/cStatus.html", e_login=e_login, c_login=c_login)


@app.route("/aStatus")
def aStatus():
    return render_template("includes/aStatus.html", e_login=e_login, c_login=c_login)


@app.route("/cSearch")
def cSearch():
    return render_template("includes/cSearch.html", e_login=e_login, c_login=c_login)


@app.route("/deposit")
def deposit():
    return render_template("includes/deposit.html", e_login=e_login, c_login=c_login)


@app.route("/withdraw")
def withdraw():
    return render_template("includes/withdraw.html", e_login=e_login, c_login=c_login)


@app.route("/transfer")
def transfer():
    return render_template("includes/transfer.html", e_login=e_login, c_login=c_login)


@app.route("/transacList")
def transacList():
    return render_template("includes/transacList.html", e_login=e_login, c_login=c_login)


@app.route("/transacDate")
def transacDate():
    return render_template("includes/transacDate.html", e_login=e_login, c_login=c_login)


@app.route("/aSearch")
def aSearch():
    return render_template("includes/aSearch.html", e_login=e_login, c_login=c_login)


@app.route("/logout")
def logout():
    # Write code to end session
    pass
    # return render_template("includes/aSearch.html")
