from flask import Blueprint,render_template

enfmod = Blueprint('enfermedad', __name__, template_folder='templates')

@enfmod.route('/enfermedad-index')
def enfermedadIndex():
    return render_template('enfermedad-index.html')