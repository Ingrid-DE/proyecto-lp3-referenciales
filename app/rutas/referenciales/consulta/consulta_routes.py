from flask import Blueprint,render_template

consmod = Blueprint('consulta', __name__, template_folder='templates')

@consmod.route('/consulta-index')
def consultaIndex():
    return render_template('consulta-index.html')