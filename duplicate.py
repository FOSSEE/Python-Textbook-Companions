import os
import shutil
import sys


def remove_duplcates(book_path):
	"""
	This function will find latest version and remove duplicates of a chapter
	to backup folder in current path. function returns number of files moved.
	"""
	
	moved_file_count = 0
	flag = 0
	dic={}
	keep=[]
	delete = []
	latest_chapter = []
	temp_list =[]
	temp_list_updated =[]
	chapter_name=[]
	for path,dirname,filenames  in os.walk(book_path,topdown=False):
		dic[path]={}
		for files in filenames:
			if files.endswith('.ipynb'):
				dot_index = files.index('.')
				chapter = files[:dot_index]+'_'
				chapter_name.append(chapter)
		chapter_name.sort()


		for name in chapter_name:
			x =[i for i in chapter_name if name in i]
			if len(x)==1:
				temp_list.append(x[0])
				continue
			x.sort()
			key_name = x.pop(0)
			for j in x:
				if dic[path].has_key(key_name):
					dic[path][key_name].append(j)
				else:
					dic[path][key_name]=[j]
			
		for i in temp_list:
			for key in dic[path].keys():
				if key in i:
					temp_list_updated.append(i)
		
		single_chapter = set(temp_list).difference(set(temp_list_updated))

	
		for key in dic[path].keys():
			if len(dic[path][key])==0:
				latest_chapter.append(key)
			else:
				latest_chapter.append(max(dic[path][key]))

		latest_chapter_updated = set(latest_chapter).union(single_chapter)

	for path,dirname,filenames  in os.walk(book_path,topdown=False):

		for files in filenames:
			if files.rfind('.')>0:
				dot_index = files.rindex('.')
				files_update = files[:dot_index]+'_'
			else:
				files_update = files

			for latest in latest_chapter_updated:
				if files_update.__contains__(latest):
					flag = 1
					keep.append(os.path.join(path,files))
					break
				else:
					flag = 0

			if not flag and ('.ipynb' in files or '.html' in files):
				delete.append(os.path.join(path,files))

		moved_file_count = moved_file_count+len(delete)
		
		book_name = path.split('/')[-1]

		try:
			os.mkdir(os.path.join(path,book_name+'_version_backup'))
		except OSError:
			pass

		while delete:
			try:
				shutil.move(delete.pop(),os.path.join(path,book_name+'_version_backup'))
			except Exception:
				pass

	return moved_file_count

def remove_emptyfolders(book_path):
	
	for path,dirname,filenames  in os.walk(book_path,topdown=False):
		if len(os.listdir(path))==0:
			os.rmdir(path)

def move_backupfolders(book_path,root_backup):

	for path,dirname,filenames  in os.walk(book_path,topdown=False):
		if 'version_backup' in path:
			shutil.move(path,root_backup)
			break
		else:
			pass


def main(book_path,root_backup):
	remove_emptyfolders(book_path)
	print "Removing duplicates in given path:\n"
	number_of_moved = remove_duplcates(book_path)
	print ("moved {0} files to backup folder in given path\n".format(number_of_moved))
	print "Removing empty folders in given path:\n"
	remove_emptyfolders(book_path)
	print "Moving version_backup to backup folder:\n"
	move_backupfolders(book_path,root_backup)


if __name__=='__main__':
	cwd = os.getcwd()
	try:
		os.mkdir(os.path.join(cwd,'backup'))
	except OSError:
		pass
	root_backup = os.path.join(cwd,'backup')
	#main(os.sep.join((cwd,'Analog_and_Digital_Communications_by_H_P_Hsu')),root_backup=root_backup)

	dirs = os.listdir(cwd)
	for k in dirs:
		if os.path.isdir(os.path.join(cwd,k)) and (k != 'backup'):
			print '----------------------------------------------------------'
			print k
			main(os.path.join(cwd,k),root_backup)
