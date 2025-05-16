# from scenedetect import AdaptiveDetector, detect
# # from math import floor
# import subprocess
# from joblib import Parallel, delayed
# # from text_extraction import VideoToTextExtractor

# video_path = r'static\video\Macbook Air Review.mp4'

# # video_path = r'static\video\Macbook Air Review.mp4'

# scene_list = detect(video_path, AdaptiveDetector())

# extractor = VideoToTextExtractor()
# extractor.scene_extractor(video_path=video_path, output_dir='video_segments')




# def extract_scene(start_time,end_time,scene_number,video_path):
#     output_pattern = f'video_segments/-Scene-{scene_number}.mp4'

#     subprocess.run([
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
#                     ],
#                     stdout=subprocess.DEVNULL,
#                     stderr=subprocess.DEVNULL)  #remove this for showing out and errors




# if scene_list:
#     numbered_scene_list = []
#     for i,scene in enumerate(scene_list):
#         start_time = scene[0].get_timecode()
#         end_time = scene[1].get_timecode()
#         scene_number = i

#         numbered_scene_list.append((start_time,end_time,scene_number, video_path))







    # for i,scene in enumerate(scene_list):
    #     start_time = scene[0].get_timecode()
    #     end_time = scene[1].get_timecode()
    #     output_pattern = f'video_segments/-Scene-{i}.mp4'

        
    #     subprocess.run([
    #                     'ffmpeg',
    #                     '-i', video_path,
    #                     '-ss', str(start_time),
    #                     '-to', str(end_time),
    #                     '-c:v', 'libx264',
    #                     '-preset', 'fast',
    #                     '-crf', '23',
    #                     '-c:a', 'libvo_aacenc',
    #                     '-b:a', '192k',
    #                     output_pattern
    #                 ])

# if __name__ == '__main__':

#      result = Parallel(n_jobs=-1, backend='threading',batch_size = 20)(
#         delayed(extract_scene)(start_time,end_time,scene_number,video_path) for start_time, end_time, scene_number,video_path in numbered_scene_list
#     )

    # from multiprocessing import Pool
    # pool = Pool(processes=3)
    # pool.starmap(extract_scene,numbered_scene_list)

