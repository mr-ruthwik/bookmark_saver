from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# In-memory storage for the application data
users = {} 
bookmarks = {}  
folders = {}  
favorites = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "User already exists! Please sign in."

        users[username] = {"name": name, "password": password}
        bookmarks[username] = []
        folders[username] = {}
        favorites[username] = [] 
        return redirect(url_for("signin"))
    return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username not in users or users[username]["password"] != password:
            return "Invalid username or password!"

        session["username"] = username
        return redirect(url_for("dashboard"))
    return render_template("signin.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("signin"))
    username = session["username"]

    favorite_msg = session.pop("favorite_msg", None)
    
    # For fast membership checking in the template
    favorite_urls = {fav['url'] for fav in favorites.get(username, [])}

    return render_template(
        "dashboard.html",
        name=users[username]["name"],
        bookmarks=bookmarks[username],
        folders=folders[username],
        favorites=favorites[username],
        favorite_urls=favorite_urls,
        favorite_msg=favorite_msg
    )

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

# Add bookmark
@app.route("/add_bookmark", methods=["POST"])
def add_bookmark():
    if "username" not in session:
        return redirect(url_for("signin"))
    username = session["username"]
    title = request.form["title"]
    url = request.form["url"]
    bookmarks[username].append({"title": title, "url": url})
    return redirect(url_for("dashboard"))

# Edit bookmark
@app.route("/edit_bookmark", methods=["POST"])
def edit_bookmark():
    if "username" not in session:
        return redirect(url_for("signin"))
    username = session["username"]
    old_url = request.form["old_url"]
    new_title = request.form["new_title"]
    new_url = request.form["new_url"]

    for b in bookmarks[username]:
        if b["url"] == old_url:
            b["title"] = new_title
            b["url"] = new_url
            break

    return redirect(url_for("dashboard"))

# Add folder
@app.route("/add_folder", methods=["POST"])
def add_folder():
    if "username" not in session:
        return redirect(url_for("signin"))
    username = session["username"]
    folder_name = request.form["folder_name"]
    bookmarks_to_add = request.form.getlist("bookmarks_to_add")

    if folder_name not in folders[username]:
        folders[username][folder_name] = []
    
    for url in bookmarks_to_add:
        bookmark = next((b for b in bookmarks[username] if b["url"] == url), None)
        if bookmark and bookmark not in folders[username][folder_name]:
            folders[username][folder_name].append(bookmark)

    return redirect(url_for("dashboard"))

# Delete folder
@app.route("/delete_folder/<folder_name>", methods=["POST"])
def delete_folder(folder_name):
    if "username" not in session:
        return redirect(url_for("signin"))
    username = session["username"]
    if folder_name in folders[username]:
        del folders[username][folder_name]
    return redirect(url_for("dashboard"))

# Add bookmark to favorites
@app.route("/add_to_favorites", methods=["POST"])
def add_to_favorites():
    if "username" not in session:
        return redirect(url_for("signin"))
    username = session["username"]
    url = request.form.get("url")

    # Check if the bookmark is already in favorites
    if any(b['url'] == url for b in favorites[username]):
        session["favorite_msg"] = "Bookmark is already in favorites."
    else:
        bookmark = next((b for b in bookmarks[username] if b["url"] == url), None)
        if bookmark:
            favorites[username].append(bookmark)
            session["favorite_msg"] = f"{bookmark['title']} added to favorites successfully"
        else:
            session["favorite_msg"] = "Bookmark not found."

    # Redirect back to the page the user came from
    return redirect(request.referrer or url_for("dashboard"))

# Delete from favorites
@app.route("/delete_favorite", methods=["POST"])
def delete_favorite():
    if "username" not in session:
        return redirect(url_for("signin"))
    username = session["username"]
    url = request.form.get("url")
    
    # Check if the bookmark is in favorites and remove it
    if username in favorites:
        favorites[username] = [b for b in favorites[username] if b['url'] != url]
    
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)