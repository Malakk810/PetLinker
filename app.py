# from flask import Flask, send_from_directory
# from routes.adoptionQuiz import adoption_bp

# app = Flask(__name__)

# # Register Blueprints
# app.register_blueprint(adoption_bp)

# # Serve static files (HTML, CSS, JavaScript)
# @app.route("/")
# def index():
#     return send_from_directory("static", "quiz.html")

# @app.route("/static/<path:filename>")
# def static_files(filename):
#     return send_from_directory("static", filename)

# if __name__ == "__main__":
#     app.run(debug=True)
###################################################################################################################

# from flask import Flask, send_from_directory
# from routes.user import user_bp  

# app = Flask(__name__)

# # Register the blueprint for user-related routes
# app.register_blueprint(user_bp)

# # Route to serve the HTML front-end
# @app.route("/user.html")
# def user_management():
#     return send_from_directory("static", "user.html")

# # Route to serve CSS and other static files (JS, images, etc.)
# @app.route("/static/<path:filename>")
# def static_files(filename):
#     return send_from_directory("static", filename)

# if __name__ == "__main__":
#     app.run(debug=True)
###################################################################################################################


# from flask import Flask
# from adoption import adoption_bp

# app = Flask(__name__)

# # Register the adoption blueprint
# app.register_blueprint(adoption_bp)

# # Route to serve the HTML file
# @app.route('/home')
# def home():
#     return app.send_static_file('adoption.html')

# if __name__ == '__main__':
#     app.run(debug=True)


###################################################################################################################

from flask import Flask
from marketPlace import marketplace_bp  
# from routes.petActivity import pet_activity_bp  

app = Flask(__name__)

# # Register the marketplace routes blueprint
app.register_blueprint(marketplace_bp, url_prefix='/api/marketplace')

# Register the pet activity routes blueprint
# app.register_blueprint(pet_activity_bp, url_prefix='/api/activities')

if __name__ == "__main__":
    app.run(debug=True)
###################################################################################################################
