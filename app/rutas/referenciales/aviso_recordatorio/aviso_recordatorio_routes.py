from flask import Blueprint, render_template
aviso_mod = Blueprint('aviso_recordatorio', __name__, template_folder='templates')
@aviso_mod.route('/aviso_recordatorio-index')
def aviso_recordatorioIndex():
    return render_template('aviso_recordatorio-index.html')
 