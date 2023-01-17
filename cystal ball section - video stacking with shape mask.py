# important reference https://github.com/Zulko/moviepy/issues/1547 视频叠视频的重要参考

import moviepy.editor as mp

working_dir = r"C:\Users\blues\Documents\GitHub\UltmanVid\爱莎\Resources 内容素材" 
	
clip = mp.VideoFileClip(r"empty_crys_ball.mp4") #底片，空白的水晶球
childs_vid=mp.VideoFileClip("childs_vid.mp4") #叠在底片上的视频，小孩的视频，从下往上第二层

third_bubble=("third_bubble-1.png") #从下往上第三层，彩色气泡
top_shine=("balltoppic-white.png") #从下往上第四层，白色光晕

duration=(clip.duration) #以底片的时长为基准时长

mask=mp.ImageClip("whitecircle.png").set_duration(duration) #蒙版，白色圆形
mask1=mask.to_mask() #蒙版转换为mask

mask_clip=childs_vid.set_mask(mask1) #小孩视频加上圆形蒙版，只露出圆形部分，黑色部分被遮挡

third_layer=(mp.ImageClip(third_bubble)
             .set_duration(duration)
             .set_position((626,232)))


top_layer=(mp.ImageClip(top_shine)
             .resize(0.96)
             .set_duration(2.5)
             .set_position((677,216)))

final_clip = mp.CompositeVideoClip([clip,mask_clip,third_layer,top_layer.set_start(0).crossfadeout(1)])

final_clip.write_videofile('final_clip-d.mp4')#, threads = 16, fps=24, codec = 'h264_nvenc'

