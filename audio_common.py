#ffmpeg -i input_mp3 -ss start_time -to end_time out_mp3
#ffmpeg -i "concat:in1.mp3|in2.mp3" -acodec copy out.mp3
#ffmpeg -i "concat:concat_in_pipe" -acodec copy out_mp3

from functions import *

class Audio:
    def __init__(self):
        self.out_dict = dict()
        self.cut_cmd ="ffmpeg -i input_mp3 -ss start_time -to end_time out_mp3"
        self.merge_cmd ='ffmpeg -i "concat:concat_in_pipe" -acodec copy out_mp3'

        print ("Welcome to audio cutter and merger")
    def take_inputs(self, config_file):
        list1 = parse_file_as_list(config_file)
        for i in list1:
            line=i.strip()
            if (line==""):
                continue
            if (line[0]=="#"):
                continue
            line_list = [k.strip() for k in line.split()]
            outfile = line_list[-1]
            if (outfile in self.out_dict):
                self.out_dict[outfile].append(line_list[:-1])
            else:
                self.out_dict[outfile] = list()
                self.out_dict[outfile].append(line_list[:-1])
    def generate_mp3(self):
        for i in self.out_dict:
            concat_mp3=[]
            cmd_call("rm temp*mp3")
            cmd_call("rm "+i)
            for j in self.out_dict[i]:
                out_mp3 = "temp"+str(self.out_dict[i].index(j))+".mp3"
                #self.cut_cmd ="ffmpeg -i input_mp3 -ss start_time -to end_time out_mp3"
                cut_cmd = self.cut_cmd.replace("input_mp3", j[0])
                cut_cmd = cut_cmd.replace("start_time", j[1])
                cut_cmd = cut_cmd.replace("end_time", j[2])
                cut_cmd = cut_cmd.replace("out_mp3", out_mp3)
                concat_mp3.append(out_mp3)
                cmd_call(cut_cmd)
            merge_cmd = self.merge_cmd.replace("concat_in_pipe","|".join(concat_mp3))  #='ffmpeg -i "concat:concat_in_pipe" -acodec copy out_mp3'
            merge_cmd = merge_cmd.replace("out_mp3", i)
            cmd_call(merge_cmd)
