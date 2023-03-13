import os
from os import listdir
import numpy as np
from PIL import Image,ImageFont,ImageDraw
import moviepy.editor as mp

nameofchild=input('寿星名字? Name of the child?: ')
age=input('几岁生日? Age of the child?: ')
peiyinfile=input('配音文件名(不需要要后缀)? File name of the TTS audio (exclude .mp3)?:')

path = os.getcwd()
print (path)

x=list()
files = os.listdir(path)
print (files)

targetlist=['Q5','Q6','Q7','Q8','Q9','Q10'] #assuming Q5-Q10 photos have been collected and saved in current dict

#find all file in targetlist and add to list X
for f in files:
    if f.endswith(".jpeg" or ".jpg" ):
        image=Image.open(f)
        fname=f.split('-')
        f1name=fname[1]
        if f1name in (targetlist):
            image.save(f1name+'.jpg')
            x.append(f1name+'.jpg')
            image.close()
        else:continue
    else:continue

x.pop(0)
x.append('Q10.jpg')
print(x)

index=0

for img in x:
    print(img)
    # Open the input image as numpy array, convert to RGB
    img=Image.open(img).convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save(targetlist[index]+'.png')
    index+=1

    img.close()

print("Circle cut done")

##制作片头和PS主图 Process PS(combied image with kids) and PT(1st image in video)

ps=Image.open("Frozen\ps.png")
pt=Image.open("Frozen\Piantou.png")
im=Image.open('Q5.png')
base=Image.open("base.png")

newsize=(760,760)
im=im.resize(newsize)

#make PianTou Pt photo
base.paste(im,(1133,-14),im)
base.paste(pt,(0,0),pt)
base.save('pt1.png')

#make PS photo and add texts
base.paste(im,(1133,-14),im)
base.paste(ps,(0,0),ps)
base.save('ps1.png')

#add age-number ballon
balimg=Image.open('b'+age+'.png')
imgb=Image.open('ps1.png')
imgb.paste(balimg,(0,0),balimg)
imgb.save('ps1b.png')

#add text with chi font
fontchi=ImageFont.truetype("ZCOOLKuaiLe-Regular.ttf",152)
imgt=Image.open('ps1b.png')
draw=ImageDraw.Draw(imgt)
draw.text((696,338),nameofchild,(255,255,255),font=fontchi)
imgt.save('ps1tchi.png')

#add text with eng font
fonteng=ImageFont.truetype("love.ttf",164)
imgt=Image.open('ps1b.png')
draw=ImageDraw.Draw(imgt)
draw.text((696,332),nameofchild,(255,255,255),font=fonteng)
imgt.save('ps1teng.png')

print('片头和PS图完成 PS and PT done')

ps.close()
pt.close()
im.close()
base.close()

##制作片尾 Process PT(Ending scene)
c=mp.VideoFileClip(r"C:\Users\blues\Documents\AUTOMATION\Frozen\片尾\base1.mp4")
endtime=c.end
print(endtime)

pianweitext=("祝"+nameofchild+"小公主生日快乐！") #wish the child a happy b-day in Chinese

bgsize=(1920,1080)
        
ptext=mp.TextClip(pianweitext,font="ZCOOLXiaoWei-Regular.ttf",size=(1300,0),color="white").set_duration(c.duration)
       
final=mp.CompositeVideoClip([c,ptext.set_duration(endtime-17)\
                             .set_start(17).crossfadein(3)\
                             .set_position('center')])

final.write_videofile("片尾.mp4", threads = 16, fps=24, codec = "h264_nvenc")
c.close()
print('片尾完成 Ending part done')

##制作后段 Process Main scene

peiyin=mp.AudioFileClip(peiyinfile+'.mp3')
v1=mp.VideoFileClip("Frozen1-1.mp4")
v2=mp.VideoFileClip("Frozen3-1.mp4")
v2r=mp.VideoFileClip("Frozen_rev_3-1.mp4")
vend=mp.VideoFileClip("Frozen6-1.mp4")
toaddaudio=mp.AudioFileClip("Frozen_extra1.mp3")

#start calculating suitable duration
vit=(v1.end)
v2t=(v2.end)
v2rt=(v2r.end)
vet=(vend.end)
vidur=(vit+v2t+v2rt+vet)
print(vit)

audiodur=peiyin.end
print(audiodur)

lengv=(audiodur-vit-v2t-v2rt-vet)
lengmiv=(audiodur-vit-v2t-vet)

print (lengv)
print (lengmiv)

v2sub=v2.subclip(0,lengv)

v2misub=v2r.subclip(0,lengmiv)

if audiodur<(vit+vet):
    if input('Want to add the extra recording 再长一岁？:')== 'y' or 'Y':
        outaudio=mp.concatenate_audioclips([peiyin,toaddaudio])
        outaudio.write_audiofile('11-1.mp3')
        peiyin=mp.AudioFileClip("11-1.mp3")
        audiodur=peiyin.end
        print(audiodur)
    else: print('Peiyin too short!')
else:pass


if audiodur==(vit+vet):
    combi=mp.concatenate_videoclips([v1,vend])
    print(combi.end)

elif (vit+vet)<audiodur<(vit+v2t+vet):
    v2=v2.subclip(0,(audiodur-vit-vet))
    combi=mp.concatenate_videoclips([v1,v2,vend])
    print(combi.end)

elif (vit+v2t+vet)<audiodur<=vidur:
    v2r=v2r.subclip(0,(vidur-audiodur))
    combi=mp.concatenate_videoclips([v1,v2,v2r,vend])
    print(combi.end)

elif (vidur+v2t)>audiodur>vidur:
    combi=mp.concatenate_videoclips([v1,v2,v2r,v2sub,vend])
    print(combi.end)

elif (vidur+v2t*2)>audiodur>(vidur+v2t):
    v2sub=v2.subclip(0,(audiodur-vidur-v2t))
    combi=mp.concatenate_videoclips([v1,v2,v2r,v2,v2sub,vend])
    print(combi.end)

else:
    combi=mp.concatenate_videoclips([v1,v2,v2r,v2,v2r,v2])
    print(combi.end)
    print('Audio too long, need to add ending manually')

final=combi.set_audio(peiyin)
final.write_videofile('zhuduan.mp4')


peiyin.close()
v1.close()
v2.close()
v2r.close()
vend.close()

input('100% completed! Q4-魔球，Q10-雪花框')
