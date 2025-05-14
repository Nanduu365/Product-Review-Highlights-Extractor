from flask import Flask, render_template,redirect,request, send_from_directory, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from threading import Thread
import time
from text_extraction import create_and_delete_folders, delete_files, VideoToTextExtractor
from model import system_prompt, preprocess_prompt, generate_response, merge_videos


app = Flask(__name__)
UPLOAD_FOLDER = 'static/video'
RESULT_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER



#create upload folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
text_segments_file = 'text_segments.txt'

create_and_delete_folders(['video_segments','audio_segments'])
delete_files(['text_segments.txt'])

bar = 0


def complete_process():
    global bar
    bar = 0

    video_names = os.listdir('static/video')
    video_path = rf"{app.config['UPLOAD_FOLDER']}\\{video_names[0]}"
    video_segments_folder = r'video_segments'
    audio_segments_folder = r'audio_segments'
    bar = 10

    extractor = VideoToTextExtractor()
    extractor.scene_extractor(video_path=video_path, output_dir=video_segments_folder)
    bar = 25

    extractor.audio_extractor(audio_dir=audio_segments_folder, video_dir=video_segments_folder)
    bar = 40
    extractor.text_from_audio(audio_dir= audio_segments_folder)
    bar = 70


    query = preprocess_prompt(system_prompt, text_segments_file)
    bar = 75
    json_response = generate_response(query)
    bar = 85
    merge_videos(video_segments_folder,json_response)
    bar = 100

@app.route('/', methods = ['POST','GET'])
def home():
    clean_up()


    if request.method == 'POST':
        video = request.files['video']

        filename = secure_filename(video.filename)
        filepath = 'static/video/' + filename
        video.save(filepath)
        flag = True
        

        return render_template('home.html', tasks = [flag,filename])
    
    else:
        return render_template('home.html', tasks=[False,None])



@app.route('/results/<filename>')
def load_results(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)


@app.route('/loading')
def loading():
    thread = Thread(target= complete_process)
    thread.start()
    filename = os.listdir('static/video')[0]

    create_and_delete_folders(['video_segments','audio_segments'])
    delete_files(['text_segments.txt'])

    return render_template('home.html', tasks = [True, filename])


@app.route('/update_value')
def update_progress_bar():
    global bar
    return jsonify({'value' : bar})





@app.route('/highlights/')
def highlights():
    # time.sleep(5)
    # return render_template('loaded.html')

    
    filenames = os.listdir(app.config['RESULT_FOLDER'])
    if os.listdir(app.config['RESULT_FOLDER']) == []:
        time.sleep(5)
        return "NO EXTRACTION POSSIBLE"
    else:

        filenames = {}
        for filename in os.listdir(app.config['RESULT_FOLDER']):
            if filename.endswith('.mp4') and filename != 'none_of_the_above.mp4':
                name = filename.split('.mp4')[0]
                name = name.upper().replace('_', ' ')
                source = url_for('load_results', filename=filename)

                filenames[name] = source

        
        names = list(filenames.keys())

        # names = [name.split('.mp4')[0] for name in filenames if name.endswith('.mp4')]
        # names = create_titles(names)
        # sources = [url_for('load_results', filename=name) for name in filenames]
        

        return render_template('highlights.html', filenames = filenames, names = names)

# def check_upload_status():
#     global load
#     while load != 1:
#         names = os.listdir(app.config['UPLOAD_FOLDER'])
#         if len(names) >0:
#             load = 1
#         time.sleep(0.1)

# def show_upload_progress():
#     thread_1 = Thread(target= check_upload_status)
#     thread_1.start()

def clean_up():
    global load
    load = 0

    folders = [app.config['UPLOAD_FOLDER'],app.config['RESULT_FOLDER']]

    for folder in folders:
        files = os.listdir(folder)

        for file in files:
            os.remove(os.path.join(folder,file))
    

def create_titles(names):
    result = []
    for name in names:
        if name == 'feature_demonstration':
            result.append('FEATURE DEMONSTRATION')
        if name == 'final_verdict':
            result.append('FINAL VERDICT')
        if name == 'product_unboxing':
            result.append('PRODUCT UNBOXING')
    return result
        


if __name__ == '__main__':
    app.run(debug=True)