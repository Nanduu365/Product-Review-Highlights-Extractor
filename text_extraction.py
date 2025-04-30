from scenedetect import detect, AdaptiveDetector,split_video_ffmpeg
import ffmpeg

import os
import subprocess
import re

from faster_whisper import WhisperModel

import json
from math import log10
import shutil

# import logging
# logging.basicConfig(level= logging.DEBUG)


def create_and_delete_folders(folder_names:list):
    for folder_name in folder_names:
        #delete folder if it exists
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
    
        #make a new folder after deleting, or entirely make a new one
        os.makedirs(folder_name)

def delete_files(file_names:list):
    for file in file_names:
        os.remove(file)


# def edited_number(num:int):
#     '''Returns a str number format specfic for this project'''
#     if num == 0:
#         num = '000'
#     else:
#         digits = int(log10(num)) +1 #formula to count the number of digits

#         if digits == 1:
#             num = f'00{num}'
#         elif digits == 2:
#             num = f'0{num}'
#         elif digits == 3:
#             num = f'{num}'

#     return num


def video_name_from_path(path:str):
    video_name = path.split(r'\\')[-1]
    video_name = video_name.split('.')[0]

    return video_name


create_and_delete_folders(['video_segments','audio_segments'])
delete_files(['text_segments.txt'])


video_path = r"user_uploaded_video\\Macbook Air Review.mp4"
video_segments_folder = r'video_segments'
audio_segments_folder = r'audio_segments'


#extracting the scenes based on the cuts--- if the cuts are too smooth, scenes will not be detected



class VideoToTextExtractor():
    def __init__(self):
        self.flag = None

    def scene_extractor(self,video_path:str, output_dir:str,segment_time:int = 10):

        print('Extracting Scenes.....')
        scene_list = detect(video_path, AdaptiveDetector())
        
        if scene_list:
            for i,scene in enumerate(scene_list):
                start_time = scene[0].get_timecode()
                end_time = scene[1].get_timecode()
                output_pattern = f'video_segments/-Scene-{i}.mp4'

                subprocess.run([
                    'ffmpeg','-loglevel', 'error','-i', video_path,'-ss',str(start_time),
                    '-to',str(end_time),'-c','copy',output_pattern
                ])
            self.flag = True #setting true to indicate that we successfully extracted scenes
        else:
            print("No scenes detected in the video,Segmenting on a constant period...")

            video_name = 'Macbook Air Review'
            output_pattern = f'video_segments/{video_name}-Scene-%d.mp4'

            subprocess.run([
                'ffmpeg','-i',video_path,'-c','copy', 
                '-f','segment','segment_time',str(segment_time),output_pattern
            ])
            self.flag = False #setting flag to false , indicating we have used video segmantation and the scene extraction failed

    # def rename_extracted_scenes(self,video_dir = video_segments_folder):
    #     '''Rename the videos in video segments folder 
    #     only and only if video segmentation is used instead of video extraction'''
    #     if self.flag== False:
    #         print('Renaming files....')
    #         video_names = sorted(os.listdir(video_dir))
    #         pattern = r'\d{3}' #pattern for finding 3 digit numbers
    #         bias_term = len(video_names) #for renaming all the files, bias term is addded to ensure that same file names are not replaced

    #         #first renaming
    #         for name in video_names:
    #             number = re.findall(pattern,name)[-1] #find the last occuring pattern
    #             new_number = edited_number(int(number) + bias_term)

    #             index = name.rfind(number) #index of last occurence
    #             new_name = name[:index] + new_number + name[index+3:]

    #             old_path = os.path.join(video_dir,name)
    #             new_path = os.path.join(video_dir,new_name)
    #             os.rename(old_path,new_path)


    #         video_names = sorted(os.listdir(video_dir))
    #         pattern = r'\d{3}' #pattern for finding 3 digit numbers
    #         bias_term = len(video_names) -1

    #         for name in video_names:
    #             number = re.findall(pattern,name)[-1] #find the last occuring pattern
    #             new_number = edited_number(int(number) - bias_term)

    #             index = name.rfind(number)
    #             new_name = name[:index] + new_number + name[index:]
    #             old_path = os.path.join(video_dir,name)
    #             new_path = os.path.join(video_dir,new_name)
    #             os.rename(old_path,new_path)



    def audio_extractor(self,video_dir = video_segments_folder,audio_dir = audio_segments_folder):
        '''Extracting audio for each video in video_dir and saving it to audio_dir'''

        print('Extracting audios.....')
        for video_scene_name in os.listdir(video_dir):
            video_path = os.path.join(video_dir,video_scene_name)

            out_audio_name = video_scene_name.replace('.mp4','.mp3')

            output_audio_path = os.path.join(audio_dir,out_audio_name)

            ffmpeg.input(video_path).output(output_audio_path).run(quiet= True)
    

    def text_from_audio(self,audio_dir = audio_segments_folder):
        '''Creates a txt file with each line in txt represents the text 
        from each segment of the video'''
        print('Extracting Text.....')
        model = WhisperModel('tiny', compute_type='int8')
        text_segments_file = 'text_segments.txt'

        sorted_audio_names = sorted(os.listdir(audio_dir))

        for i,audio in enumerate(sorted_audio_names):
            audio_path = os.path.join(audio_dir,audio)
            segments,_ = model.transcribe(audio_path)
            text = " ".join(segment.text for segment in segments)   #this is a generator object, it is usually put in (), but it can be given without () if it is the only argument to a function

            with open(text_segments_file,'a') as f:
                f.write(text + '\n')

            print(f'\rCompleted audio {i}', end = '')
        print("Finished Text extraction from video")
    
    
        


extractor = VideoToTextExtractor()
extractor.scene_extractor(video_path=video_path, output_dir=video_segments_folder)
# extractor.rename_extracted_scenes(video_segments_folder)
extractor.audio_extractor(audio_dir=audio_segments_folder, video_dir=video_segments_folder)
extractor.text_from_audio(audio_dir= audio_segments_folder)

