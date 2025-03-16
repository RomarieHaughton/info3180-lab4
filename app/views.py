import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.models import UserProfile
from app.forms import LoginForm, UploadForm



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/upload', methods=['POST', 'GET'])
@login_required  # Ensures only logged-in users can access this route
def upload():
    form = UploadForm()  # Instantiate the form

    if form.validate_on_submit():  # Validate form submission
        file = form.file.data  # Get file from form
        filename = secure_filename(file.filename)  # Secure filename

        # Ensure the file is an image
        if filename.endswith(('.jpg', '.png')):  
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save file
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('upload'))  # Stay on upload page
        else:
            flash('Invalid file type. Please upload a JPG or PNG.', 'danger')

    return render_template('upload.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Validate entire form submission
        username = form.username.data
        password = form.password.data  # Get the password entered

        # Query database for the user by username
        user = UserProfile.query.filter_by(username=username).first()

        # Check if user exists and if the password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)  # Log in the user
            flash('Login successful!', 'success')
            return redirect(url_for("upload"))  # Redirect to upload route
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template("login.html", form=form)

#retrieve uploaded images
def get_uploaded_images():
    """Retrieve list of uploaded images from the upload folder."""
    image_list = []
    upload_folder = app.config['UPLOAD_FOLDER']
    for _, _, files in os.walk(upload_folder):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                image_list.append(file)
    return image_list

# Route to serve uploaded images
@app.route('/uploads/<filename>')
def get_image(filename):
    """Serve uploaded image files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Route to display uploaded files
@app.route('/files')
@login_required  
def files():
    """Display a list of uploaded images."""
    images = get_uploaded_images()
    return render_template('files.html', images=images)





# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
