from __future__ import unicode_literals
import youtube_dl
import sys
import csv
import os
import subprocess
from datetime import datetime,timedelta
quality="256"
codec="best"
from_csv = False
links = []
fileAdd = ""
output_folder = ""
to_mp3 = False
to_m4a = False
help_text = """
Hello, this is an Youtube audio downloader.
Use this to easily download the audio from multiple youtube videos in any format you would like.

Commands available:

-h for help.

-f [path to folder] -> outputs to the specified folder (default: .)

-l -> set quality to low (192kbps) (default: 320kbps)

-c [codec] -> specifies the codec you want to download from youtube. Highly recommended to be set to "best" (default: best)

-q -> specifies the bitrate in kbps (default: 256)

--csv [path to .csv] -> if a csv file is passed here the code will download from the links in the csv. The csv has a format as follows:

tagName,url,startime,endtime

the times can be in fthe format of "0" for seconds, "0:0" for minutes:seconds and "0:0:0" for hours:minutes:seconds

--to-mp3 -> converts all the downloads to mp3 at the end

--to-m4a -> converts all the downloads to mp4 at the end

-a [link1] [link2] [link3]... downloads from the given urls separated by space

"""

for index,arg in enumerate(sys.argv):
    if arg == "-h":
        print(help_text)
        exit(0)
    if arg == "-f":
        output_folder = sys.argv[index+1]
    if arg == "-l":
        quality = "192"
    if arg == "-c":
        codec = sys.argv[index+1]
    if arg == "--csv":
        from_csv = True
        fileAdd = sys.argv[index+1]
    if arg =="--to-mp3":
        to_mp3=True
    if arg =="--to-m4a":
        to_m4a=True
    if arg =="-q":
        quality = sys.argv[index+1]
    if arg == "-a":
        selection = sys.argv[index+1::]
        closers = [i for i,value in enumerate(selection) if value[0] == "-"]
        if len(closers) != 0:
            end_index = closers[0]
        else:
            end_index = len(selection)
        selection = selection[0:end_index]
        links = selection


def convert_to_m4a(video_file,temp_file,quality):
    errorHappened = False
    new_video_file_parts = video_file.split(".")
    new_video_file_parts[-1] = "m4a"
    new_video_file = ".".join(new_video_file_parts)
    result2 = run_process(["ffmpeg","-y","-i",temp_file,"-ab",quality+"k", new_video_file])
    if result2 == False:
        errorHappened = True
    else:
        os.remove(temp_file)
    return errorHappened,new_video_file

def convert_to_mp3(video_file,temp_file,quality):
    errorHappened = False
    new_video_file_parts = video_file.split(".")
    new_video_file_parts[-1] = "mp3"
    new_video_file = ".".join(new_video_file_parts)
    result2 = run_process(["ffmpeg","-y","-i",temp_file,"-ab",quality+"k","-f","mp3",new_video_file])
    if result2 == False:
        errorHappened = True
    else:
        os.remove(temp_file)
    return errorHappened,new_video_file

def run_process(args):

    try:

        # using stderr=subprocess.DEVNULL to mute the command
        res = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,cwd=os.getcwd(),shell=False)
    except OSError:
        print("An error occured when trying to initiate the process")
        return False

    res.wait() # wait for process to finish; this also sets the returncode variable inside 'res'
    if res.returncode != 0:
        print("An error occured!")
        result = res.stdout.read().decode("utf-8")
        print ("Output:\n {}".format(result))
        return False
    else:
        return True

def get_time(str_time):
    try:
        t = datetime.strptime(str_time,"%H:%M:%S")
    except:
        try:
            t = datetime.strptime(str_time,"%M:%S")
        except:
            t =  datetime.strptime(str_time,"%S")
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': codec,
        'preferredquality': quality
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': False,
}

def get_files(path=os.getcwd()):

    name_list = os.listdir(path)
    full_list = [os.path.join(path,i) for i in name_list]
    time_sorted_list = sorted(full_list, key=os.path.getmtime)


    sorted_filename_list = [ os.path.basename(i) for i in time_sorted_list]

    return sorted_filename_list
        
def get_video_file_name(video_id):
    return os.getcwd()+"/"+[i for i in  get_files(os.getcwd()) if video_id in i][0]

def get_temp_file_name(video_file):
    temp_file_parts = video_file.split(".")
    temp_file_parts[-2] = temp_file_parts[-2]+"-temp"
    return ".".join(temp_file_parts)

def clean_file(new_video_file,video_id):
    clean_name = new_video_file.replace("-"+video_id,"")
    os.rename(new_video_file,clean_name)
errors = 0
count = 0
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    if output_folder != "":
        os.chdir(output_folder)
        if from_csv and fileAdd[0] !="/":
            fileAdd = "../"+fileAdd
    if from_csv == False:
        for link in links:
            try:
                video_info = ydl.extract_info(link, download=False)
                video_id = video_info.get("id",False)
                results = ydl.download([link]) 
                video_file = get_video_file_name(video_id)
                temp_file = get_temp_file_name(video_file)
                os.rename(video_file,temp_file)
                error_happened = False
                if to_mp3:
                    error_happened,new_video_file = convert_to_mp3(video_file,temp_file,quality)
                elif to_m4a:
                    error_happened,new_video_file = convert_to_m4a(video_file,temp_file,quality)
                clean_file(new_video_file,video_id)
                if not error_happened:
                    count+=1
                else:
                    errors+=1
            except Exception as e:
                errors+=1
            
    else: #Using a .csv file
        with open(fileAdd, 'r') as file:
            reader = csv.reader(file)
            for index,row in enumerate(reader):
                #getting video data
                video_info = ydl.extract_info(row[1], download=False)
                video_title = video_info.get("title", None)
                video_id = video_info.get("id", None)
                extension = codec
                if codec == "best":
                    extension = video_info.get("acodec",None).split(".")[0]
                    if video_info.get("ext",None) == "m4a":
                        extension = "m4a"
                    
                #Downloading the video
                ydl.download([row[1]])

                video_file = get_video_file_name(video_id)
                temp_file = get_temp_file_name(video_file)

                os.rename(video_file,temp_file)

                #Slicing the audio
                begin = str(get_time(row[2]))
                length = str(get_time(row[3]) - get_time(row[2]))

                result1 = run_process(["ffmpeg", "-ss", begin,  "-t", length, "-y","-i", temp_file, video_file])
                os.remove(temp_file)
                os.rename(video_file,temp_file)
                errorHappened = False

                if result1 == False:
                    errorHappened = True
                #Converting it to mp3 or m4a if specified by the user
                new_video_file = video_file
                if to_mp3:
                    conversion_worked,new_video_file = convert_to_mp3(video_file,temp_file,quality)
                elif to_m4a:
                    conversion_worked,new_video_file = convert_to_m4a(video_file,temp_file,quality)
                if not conversion_worked:
                    errorHappened = True
                #Just cleaning the name of the final output file to remove the youtube id
                clean_file(new_video_file,video_id)

                if errorHappened:
                    errors+= 1
                else:
                    print(row[0] + " downloaded sucessfuly")
                    count+=1
                
print("Tasks Finished with {} errors and {} total downloads".format(errors,count))