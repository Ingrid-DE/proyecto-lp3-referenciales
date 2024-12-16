from flask import Blueprint,render_template

ocumod = Blueprint('ocupacion', __name__, template_folder='templates')

@ocumod.route('/ocupacion-index')
def ocupacionIndex():
    return render_template('ocupacion-index.html')