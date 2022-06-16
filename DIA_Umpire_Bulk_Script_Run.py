#folder with folders for all experiments- will contain param file and will funnel output from program into appropriate folder

from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
from pathlib import Path
from shutil import copyfile, move
from os import remove, mkdir
import sys

#Update path if move location of the jar executable file
DIA_Umpire =  r"C:\Users\lawashburn\Documents\DIA\DIA_Archive\Ashley_Umpire_Package\DIA-Umpire-2.2.2\DIA_Umpire_SE-2.2.2.jar"
#Update path for each new working directory
working_directory =r"C:\Users\lawashburn\Documents\DIA\20220602_analysis\DIA_umpire"
#working directory is main folder that should contain:
#x number of parameter files (x=number of experiments)
#data file (same data for each experiment)

script_summary=[]
#adjust path to be where the working directory is, not where this script is. For each new working directory, don't have to move/copy this script
p=Path(working_directory)
#find the data file
for y in p.iterdir():
	if y.suffix=='.mzXML':
		data_file=y

#mkdir for all Q1, Q2, and Q3
result_dir=working_directory+'\\'+'results'
mkdir(result_dir)

for x in p.iterdir():
	#find the paramter file
	if x.suffix=='.txt':
		#Pull out what experiment number this is for future naming purposes
		path_list=str(x).split('\\')
		name_param=path_list[-1]
		exp_num=name_param[name_param.find('exp'):len(name_param)-4]
		#create a directory for outputs of this experiment #
		exp_dir=working_directory+'\\'+exp_num
		mkdir(exp_dir)
		#move parameter file into new directory
		temp_param_file=exp_dir+'\\'+x.name
		move(working_directory+'\\'+x.name,temp_param_file)
		#make temp data file in new directory so program output will funnel into the directory
		temp_data_file=exp_dir+'\\'+data_file.name
		copyfile(data_file,temp_data_file)
		#run the program
		start_time = datetime.now()
		#with Popen(['java', '-version'],stdout=PIPE,stderr=STDOUT) as proc:
		with Popen(['java',
					 '-jar',
					 '-Xmx12G',
					 DIA_Umpire,
					 temp_data_file,
					 temp_param_file],
					 stdout=PIPE,stderr=STDOUT) as proc:
			myout=proc.stdout.read()
			#create results file
			with open(exp_dir+'\\'+'result.txt','w') as f:
				for item in myout.decode('utf-8').splitlines():
					f.write('{}\n'.format(item))
		remove(temp_data_file)
		#label Q1, Q2, and Q3 and put them in a folder
		pe=Path(exp_dir)
		for z in pe.iterdir():
			if z.suffix=='.mgf':
				Q_file=str(z.name).split('.')
				Q_name=Q_file[0]
				rename_Q_file=result_dir+'\\'+Q_name+'_'+exp_num+z.suffix
				copyfile(exp_dir+'\\'+z.name,rename_Q_file)

		script_summary.append('execution time: {} for parameter file: {}'.format(datetime.now()-start_time,x))

with open('scripts_summary.txt','w') as f:
    for item in script_summary:
        f.write('{}\n'.format(item))
