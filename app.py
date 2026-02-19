from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# LOGIN PAGE
@app.route('/login')
def login():
    return render_template('login.html')

# DASHBOARD PAGE WITH STATS
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

                # LAND TOTAL
                total_land += float(row[3])

                # CROP COUNT
                crop = row[2]
                crops[crop] = crops.get(crop, 0) + 1
    except:
        pass

    # TOP CROP
    top_crop = max(crops, key=crops.get) if crops else "None"

    return render_template(
        'dashboard.html',
        farmers=farmers,
        total=len(farmers),
        land=round(total_land, 2),
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
    land = float(request.form['land'])

    # SAVE DATA
    with open("data.csv", "a") as f:
        f.write(f"{name},{location},{crop},{land}\n")

    # SIMPLE AI LOGIC
    if land < 2:
        suggestion = "Vegetables or Greens"
    elif land < 5:
        suggestion = "Tomato or Groundnut"
    else:
        suggestion = "Rice or Wheat"

    return render_template("result.html", suggestion=suggestion)

if __name__ == '__main__':
    import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

