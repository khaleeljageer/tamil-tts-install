import sys
import os
import time
import datetime
import subprocess as s
import eyed3

ssn_demo_path = "/home/khaleeljageer/Documents/TamilTTS/packages/ssn_hts_demo"
mp3_out_path = "/home/khaleeljageer/Documents/TamilTTS/tamil-tts-install"


ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

input_file = sys.argv[1]

filename = input_file.split(".txt")[0]

out_dir = mp3_out_path +"/" + filename + "-" + timestamp

os.system("mkdir " + out_dir)

lines = open(input_file).readlines()

count_of_lines = len(lines)
digits = len(str(abs(count_of_lines))) +1

line_count = 1

for line in lines:
	print line
	line = line.strip()
	os.chdir(ssn_demo_path)
	command = "./scripts/complete  '" + line + "' linux"
	print command
	os.system(command)
	os.system("lame -q 0 -b 128 wav/1.wav " + out_dir + "/"   + str(line_count).zfill(digits) + ".wav")
	line_count = line_count + 1


os.chdir(out_dir)
os.system("cat *.wav > "+filename+".wav")
os.system("ffmpeg -f concat -safe 0 -i <(printf \"file '$PWD/%s'\n\" *.wav) -c copy"+filename+".wav")
os.system("ffmpeg -i "+filename+".wav -codec:a libmp3lame -qscale:a 2 "+filename+".mp3")
os.system("rm *.wav")

finalPath = out_dir+"/"+filename+".mp3"
audiofile = eyed3.load(finalPath)
audiofile.initTag()
audiofile.tag.artist = u"Marxist"
audiofile.tag.album = u"Marxist Article Audio"
audiofile.tag.album_artist = u"Marixst Team"
u = unicode(filename, "utf-8")
audiofile.tag.title = u
audiofile.tag.genre = u"marxist.tncpim.org"

audiofile.tag.save()

message=filename+' Completed'
s.call(['notify-send','TTS-Tamil',message])
