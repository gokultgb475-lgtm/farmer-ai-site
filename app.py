from flask import Flask, render_template, request, redirect, url_for, session
import os
import bcrypt

app = Flask(__name__)
app.secret_key = "adminsecret"

ADMIN_USER = "gokul"
ADMIN_PASS = bcrypt.hashpw(b"gokul", bcrypt.gensalt())

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# NORMAL LOGIN PAGE
@app.route('/login')
def login():
    return render_template('login.html')

# DASHBOARD (USER VIEW)
@app.route('/dashboard')
def dashboard():
    farmers = []
    total_land = 0
    crops = {}

    try:
        with open("data.csv", "r") as f:
            for line in f:
                row = line.strip().split(",")
                farmers.append(row)
                total_land += float(row[3])
                crop = row[2]
                crops[crop] = crops.get(crop, 0) + 1
    except:
        pass

    top_crop = max(crops, key=crops.get) if crops else "None"

    return render_template(
        'dashboard.html',
        farmers=farmers,
        total=len(farmers),
        land=round(total_land,2),
        top=top_crop
    )

# FORM PAGE
@app.route('/form')
def form():
    return render_template('form.html')

# FORM SUBMIT
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    location = request.form['location']
    crop = request.form['crop']
    land = request.form['land']

    with open("data.csv","a") as f:
        f.write(f"{name},{location},{crop},{land}\n")

    return redirect(url_for('dashboard'))

# ---------------- ADMIN SECTION ---------------- #

# ADMIN LOGIN
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        if user == ADMIN_USER and bcrypt.checkpw(pwd.encode(), ADMIN_PASS):

            session['admin'] = True
            return redirect('/admin/dashboard')

    return render_template('admin_login.html')

# ADMIN DASHBOARD
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    farmers = []
    try:
        with open("data.csv") as f:
            for line in f:
                farmers.append(line.strip().split(","))
    except:
        pass

    return render_template("admin.html", farmers=farmers)

# DELETE ENTRY
@app.route('/delete/<int:index>')
def delete(index):
    if not session.get('admin'):
        return redirect('/admin')

    lines = []

    with open("data.csv") as f:
        lines = f.readlines()

    if index < len(lines):
        lines.pop(index)

    with open("data.csv","w") as f:
        f.writelines(lines)

    return redirect('/admin/dashboard')


# -------- LOGOUT ROUTE --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# RUN APP (RENDER + LOCAL)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

