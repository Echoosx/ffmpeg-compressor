import subprocess

def cmd(command):
    ret = subprocess.run(command,shell=True,encoding="utf-8")
    
    if ret.returncode == 0:
        return "Success!"
    else:
        return "Failed!"

def Compressor(input_path,subtitle_path,output_path):
    subtitle = "subtitles='" + subtitle_path.replace(':','\:') + "'"
    msg = cmd(["ffmpeg.exe",
                "-i",input_path,
                "-vf",subtitle,
                "-y",output_path])
    return msg
