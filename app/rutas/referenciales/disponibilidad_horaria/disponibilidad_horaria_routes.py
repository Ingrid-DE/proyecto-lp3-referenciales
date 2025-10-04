from flask import Blueprint, render_template

disponibilidad_horariamod = Blueprint('disponibilidad_horaria', __name__, template_folder='templates')

@disponibilidad_horariamod.route('/disponibilidad-horaria-index')
def disponibilidad_horariaIndex():
    return render_template('disponibilidad_horaria-index.html')