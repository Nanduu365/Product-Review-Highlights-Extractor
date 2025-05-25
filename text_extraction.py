from scenedetect import detect, AdaptiveDetector
import ffmpeg

import os
import subprocess
from joblib import Parallel, delayed
from math import floor

from faster_whisper import WhisperModel
from natsort import natsorted  #natural sorting




def video_name_from_path(path:str):
    video_name = path.split(r'\\')[-1]
    video_name = video_name.split('.')[0]

    return video_name



class VideoToTextExtractor():
    def __init__(self,event):
        self.flag = None
        self.event = event

    def scene_extractor(self,video_path:str, output_dir:str,segment_time:int = 10):

        print('Extracting Scenes.....')
        scene_list = detect(video_path, AdaptiveDetector())
        print(scene_list)

        def extract_scene(start_time,end_time,scene_number,video_path,event):
            output_pattern = f'video_segments/-Scene-{scene_number}.mp4'
            if not event.is_set():
                subprocess.run([
                                    'ffmpeg',
                                    '-i', video_path,
                                    '-ss', str(start_time),
                                    '-to', str(end_time),
                                    '-c:v', 'libx264',
                                    '-preset', 'fast',
                                    '-crf', '23',
                                    '-c:a', 'libvo_aacenc',
                                    '-b:a', '192k',
                                    output_pattern
                                ],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)  #remove this for showing out and errors


        if scene_list:
            numbered_scene_list = []
            for i,scene in enumerate(scene_list):
                start_time = scene[0].get_timecode()
                end_time = scene[1].get_timecode()
                scene_number = i

                numbered_scene_list.append((start_time,end_time,scene_number, video_path))
        
            result = Parallel(n_jobs=3, backend='threading',batch_size = 10)(
            delayed(extract_scene)(start_time,end_time,scene_number,video_path, self.event) for start_time, end_time, scene_number,video_path in numbered_scene_list
            )

            return True

        else :
            #Add in future ----
            #extracting the scenes based on the equl tije intervals if scene lists is empty
            # print("No scenes detected in the video,Segmenting on a constant period...")

            #     video_name = video_name_from_path(video_path)
            #     output_pattern = f'video_segments/{video_name}-Scene-%d.mp4'

            #     subprocess.run([
            #         'ffmpeg','-i',video_path,'-c','copy', 
            #         '-f','segment','segment_time',str(segment_time),'-f','mp4',output_pattern
            #     ])
            return False

            
        

        #     for i,scene in enumerate(scene_list):
        #         start_time = scene[0].get_timecode()
        #         end_time = scene[1].get_timecode()
        #         output_pattern = f'video_segments/-Scene-{i}.mp4'

                
        #         subprocess.run([
        #                         'ffmpeg',
        #                         '-i', video_path,
        #                         '-ss', str(start_time),
        #                         '-to', str(end_time),
        #                         '-c:v', 'libx264',
        #                         '-preset', 'fast',
        #                         '-crf', '23',
        #                         '-c:a', 'libvo_aacenc',
        #                         '-b:a', '192k',
        #                         output_pattern
        #                     ])



        #     self.flag = True #setting true to indicate that we successfully extracted scenes
        
        self.flag = False #setting flag to false , indicating we have used video segmantation and the scene extraction failed


    def audio_extractor(self,video_dir = 'video_segments',audio_dir = 'audio_segments'):
        '''Extracting audio for each video in video_dir and saving it to audio_dir'''

        print('Extracting audios.....')

        if not self.event.is_set():
            for video_scene_name in os.listdir(video_dir):
                video_path = os.path.join(video_dir,video_scene_name)

                out_audio_name = video_scene_name.replace('.mp4','.mp3')

                output_audio_path = os.path.join(audio_dir,out_audio_name)

                ffmpeg.input(video_path).output(output_audio_path).run(quiet= True)
    

    def text_from_audio(self,audio_dir = 'audio_segments'):
        '''Creates a txt file with each line in txt represents the text 
        from each segment of the video'''
        print('Extracting Text.....')
        model = WhisperModel('tiny', compute_type='int8')
        text_segments_file = 'text_segments.txt'

        audio_names = natsorted(os.listdir(audio_dir))

        # if not os.path.exists(text_segments_file):
        #         with open(text_segments_file,'w') as f:
        #             pass
        
        print(audio_names)

        def extract_text(index, audio_name, event):
            if not self.event.is_set():
                audio_path = os.path.join(audio_dir,audio_name)
                segments,_ = model.transcribe(audio_path)
                text = " ".join(segment.text for segment in segments)
                text = f'scene {index}: {text}'
            return text
        
        results = Parallel(n_jobs=4, backend='threading',batch_size=10)(
            delayed(extract_text)(index,audio_name,self.event) for index,audio_name in enumerate(audio_names)
        )

        results = natsorted(results)
        
        # for i,audio in enumerate(sorted_audio_names):
        #     audio_path = os.path.join(audio_dir,audio)
        #     segments,_ = model.transcribe(audio_path)
        #     text = " ".join(segment.text for segment in segments)   #this is a generator object, it is usually put in (), but it can be given without () if it is the only argument to a function

            
        with open(text_segments_file,'w') as f:
            for text in results:
                f.write(text + '\n')

            # print(f'\rCompleted audio {i}', end = '')
        print("Finished Text extraction from video")
    
    
        


# extractor = VideoToTextExtractor()
# extractor.scene_extractor(video_path=video_path, output_dir=video_segments_folder)
# # extractor.rename_extracted_scenes(video_segments_folder)
# extractor.audio_extractor(audio_dir=audio_segments_folder, video_dir=video_segments_folder)
# extractor.text_from_audio(audio_dir= audio_segments_folder)

