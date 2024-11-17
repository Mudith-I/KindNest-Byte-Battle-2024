from flask import Flask, render_template, request, redirect  # Import 'request'
import subs

app = Flask(__name__)

@app.route("/")
def redirect_to_login():
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login-fail")
def loginFail():
    return render_template("login-failed.html")

@app.route("/login-process", methods=["POST"])
def authenticate_user():
    username = request.form["Username"]  # Access the value directly
    password = request.form["Password"]
    userType = request.form["type"]

    returnedVal = str(subs.checkUsers(username, password, userType))

    if returnedVal == "userIn":
        return redirect("/user")
    elif returnedVal == "hostIn":
        return redirect("/host")
    elif returnedVal == "False":
        return redirect("/login-fail")
    else:
        return returnedVal
    
@app.route("/user")
def userDashboard():

    return render_template("user.html")

@app.route("/user-process", methods=["POST"])
def userProcess():
    # Accessing form data correctly
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    ranges = int(request.form.get("ranges"))
    
    # You can now use latitude and longitude as needed
    # For example, you might want to log them or process them further
    print(f"Latitude: {latitude}, Longitude: {longitude}")

    # Call your subs.userIn() function if needed
    subs.userIn(latitude , longitude , ranges)  # Make sure this function does not require any arguments or handle accordingly

    return redirect("/user")  # Redirecting after processing

@app.route("/host")
def hostDashboard():
    return render_template("host.html")

@app.route("/host-proccess", methods=["POST"])  # Changed to POST
def hostProccess():
    data = request.form  # Access form data correctly for POST

    subs.addCamps(data["eventLatitude"],data["eventLongitude"],data["eventName"],data["eventDate"],data["eventStartTime"],data["eventDetails"])
    return redirect("/host")

if __name__ == "__main__":
    app.run(debug=True)