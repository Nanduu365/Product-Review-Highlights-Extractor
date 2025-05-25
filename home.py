from flask import Flask, render_template,redirect,request, send_from_directory, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from threading import Thread, Event
import time
from pytubefix import YouTube

import io
from text_extraction import VideoToTextExtractor
from model import system_prompt, preprocess_prompt, generate_response, merge_videos



app = Flask(__name__)

UPLOAD_FOLDER = 'static/video'
RESULT_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
video_segments_folder = r'video_segments'
audio_segments_folder = r'audio_segments'
os.makedirs(video_segments_folder, exist_ok=True)
os.makedirs(audio_segments_folder, exist_ok=True)
text_segments_file = 'text_segments.txt'


#Defining Global Variables
bar = 0
main_event = Event()
error_statement = 'An Unexpected error occured, Try again Later'


#create upload folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)



#Defining Functions needed

def clean_up(folders = [app.config['UPLOAD_FOLDER'],app.config['RESULT_FOLDER']]):
    '''Clean up the existing upload and result folder while the website is loading'''
   
    for folder in folders:
        files = os.listdir(folder)

        for file in files:
            os.remove(os.path.join(folder,file))

def download_video(url, output_path):

    #creating a buffer
    try:
        # Create a YouTube object with additional configuration
        yt = YouTube(
            url,
            # use_oauth=True,
            # allow_oauth_cache=True
        )
        # Get the lowest resolution stream
        video_stream = yt.streams.get_by_resolution("360p")

        # Download the video
        # print(f"Downloading: {yt.title}")
        video_stream.download(output_path=output_path)
        # print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")


def complete_process():
    global bar
    global main_event
    global error_statement

    bar = 0

    video_names = os.listdir('static/video')
    video_path = rf"{app.config['UPLOAD_FOLDER']}\\{video_names[0]}"

    bar = 10

    if not main_event.is_set():
        extractor = VideoToTextExtractor(main_event)
        scenes_extracted = extractor.scene_extractor(video_path=video_path, output_dir=video_segments_folder)

        #Change this while adding manual scene extraction in the future
        if not scenes_extracted:
            main_event.set()
            error_statement = 'Extraction of Scenes not possible as an internal error occured'

        bar = 35
    
    if not main_event.is_set():
        extractor.audio_extractor(audio_dir=audio_segments_folder, video_dir=video_segments_folder)
        bar = 45
        extractor.text_from_audio(audio_dir= audio_segments_folder)
        bar = 70

    if not main_event.is_set():
        query = preprocess_prompt(system_prompt, text_segments_file, main_event)
        bar = 75

    if not main_event.is_set():
        json_response = generate_response(query, main_event)
        print(json_response)
        bar = 85
    if not main_event.is_set():
        merge_videos(video_segments_folder,json_response, main_event)
        bar = 100

clean_up()

@app.route('/', methods = ['POST','GET'])
def home():
    global main_event
    main_event.set()
    
    if request.method == 'POST':
        video = request.files['video']

        filename = secure_filename(video.filename)
        filepath = 'static/video/' + filename
        video.save(filepath)
        
        

        return render_template('home.html', tasks = [True,filename])
    
    elif os.listdir('static/video'):
        filename = os.listdir('static/video')[0]
        return render_template('home.html', tasks = [True,filename])  #True and False indicate whether to show image or to show video in the home page

    
    else:
        return render_template('home.html', tasks=[False,None])



@app.route('/results/<filename>')
def load_results(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)


@app.route('/loading')
def loading():
    global main_event
    main_event.clear()

    thread = Thread(target= complete_process, daemon=True)
    thread.start()

    clean_up(folders=['video_segments','audio_segments'])

    filename = os.listdir('static/video')[0]

    return render_template('home.html',tasks = [True,filename])


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


@app.route("/submit-url",methods = ['POST'])
def submit_url():
    if request.method == 'POST':
        url = request.form['url']
        download_video(url,output_path='static/video')

        while os.listdir('static/video') == []:
            time.sleep(2)

    return redirect('/')


@app.errorhandler(500)
def internal_error():
    return error_statement, 500
        


if __name__ == '__main__':
    app.run(debug=True)
