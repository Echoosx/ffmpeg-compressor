import subprocess
import sys

def cmd(command):
    ret = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding="utf-8")
    while ret.poll() is None:
        line = ret.stdout.readline()
        if line:
            sys.stdout.flush()
            if line.startswith('frame='):
                index = line.find('time=')
                if(index!=-1):
                    current_time_format = line[index+5:index+16]
                    current_time_sec = format2sec(current_time_format)
                    percentage = (current_time_sec/full_time_sec) * 100
                    print('\r'+'【进度:{:.2f}%】 '.format(percentage) + line.strip(),end='\r')
                else:
                    print(line.strip(),end='\r')
            else:
                print(line,end='')
    
    if ret.returncode == 0:
        sys.stdout.write("Compress success!")
        sys.stdout.flush()
        # return "Success!"
    
    else:
        sys.stdout.write("Compress failed!")
        sys.stdout.flush()
        # return "Failed!"

def Compressor(input_path,subtitle_path,output_path):
    global full_time_sec 
    full_time_sec = float(subprocess.check_output("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i \"{}\"".format(input_path),shell=True))

    subtitle = "subtitles='" + subtitle_path.replace(':','\:') + "'"
    # msg = 
    cmd(["ffmpeg.exe",
                "-i",input_path,
                "-vf",subtitle,
                "-crf",'21',
                "-y",output_path])
    # return msg


def format2sec(format):
    list = format.split(':')
    sec = float(list[-1]) + int(list[-2]) * 60 + int(list[-3]) * 60 * 60
    return sec