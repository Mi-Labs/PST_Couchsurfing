
from flask import Flask, render_template, request
from pathlib import Path
import os
from flask_dropzone import Dropzone
import contact_handler as ch
import main

app = Flask(__name__,template_folder='template')
app.static_folder = 'static'
start_Website = "index.html"
uploade_website ="uploade.html"

app.config.update(
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=2024,  # maximale file größe
    DROPZONE_TIMEOUT=5 * 60 * 1000,  # maximale uploade dauer (hier 5 min)
    DROPZONE_UPLOAD_ACTION='uploade',
    DROPZONE_UPLOAD_MULTIPLE=True,#erlaubt parallele uploads
    DROPZONE_PARALLEL_UPLOADS=3#erlaubt bis zu drei uploads gleichzeitig
)
app.static_folder = 'static'
dropzone = Dropzone(app)
@app.route("/",methods=['GET','POST'])
def index():
    print('hallöle')
    if request.method == "POST":
        if request.form.get("home") == "home":
            return render_template(start_Website,start_screen_visibility= "visible")
    return render_template(start_Website)
@app.route("/start_screen", methods=['GET', 'POST'])
def start_screen():
    if request.method == 'POST':
        if request.form.get('New_Kontakts') == 'new Kontakt':
            return render_template(uploade_website)
        elif request.form.get('berechnen') == 'suchen':
            parameter = request.form.getlist('checkbox_parameter')
            main.main(parameter)
            return render_template('map.html')
        else:
            print('start Website')
            return render_template(start_Website)
    else:
        print('start  Website')
        return render_template(start_Website)
@app.route("/upload_kontakte",methods=['POST','GET'])
def uploade():
    print('uploade Website')
    f = request.files.get('file')  # empfängt neuen file
    if f:
        file_path = Path(os.path.abspath("."), 'kontakte.vcf')
        f.save(file_path)
    ch.vcf_read()
    return render_template(uploade_website)




if __name__ == '__main__':
    app.run()

