from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import multiprocessing
import six

if sys.version_info[0] == 3:
    from urllib.request import urlopen, urlretrieve
else:
    from urllib import urlopen, urlretrieve
    
def download(url, target_path): #base function that will be parallelized
	try:
		print(">>Downloading " + target_path)
		urlretrieve(url, target_path)
	except(KeyboardInterrupt, SystemExit):
		print(">>Exiting process")
		
class KGSIndex: #Kiseido Go Server
	
	def __init__(self, kgs_url='http://u-go.net/gamerecords/', index_page='kgs_index.html', data_dest='data'):

		"""Create an index of zip files containing SGF data of actual Go Games on KGS.
		Parameters:
			kgs_url: URL with links to zip files of games
			index_page: Name of local html file of kgs_url
			data_dest: name of directory relative to current path to store SGF data
		"""
		self.kgs_url = kgs_url
		self.index_page = index_page
		self.data_dest = data_dest
		self.file_info = []
		self.urls = []
		self.load_index() #load index on initialization
        	
	def download_files(self):
		"""Download zip files distributing work on all available CPU units"""		

		if not.path.isdir(self.data_dest):
			os.mkdir(self.data_dest)

		urls_to_download = []
		for file_info in self.file_info:
			url = file_info['url']
			file_name = file_info['filename']
			if not os.path.isfile(os.path.join(self.data_dest, file_name)):
				urls_to_download.append((url, os.path.join(self.data_dest, file_name)))
		cores = multiprocessing.cpu_count()
		pool = multiprocessing.Pool(processes=cores)
		try:
			it = pool.imap(worker, urls_to_download)
			for _ in it:
				pass
			pool.close()
			pool.join()
		except KeyboardInterrupt:
			print(">>> Caught KeyboardInterrupt, terminating workers")
			pool.terminate()
			pool.join()
			sys.exit(-1)
        		
	def create_index_page(self):
		"""If there's no local html containing links to files, create one"""
		if os.path.isfile(self.index_page):
			print(">>> Reading cached index page")
			index_file = open(self.index_page, 'r')
			index_contents = index_file.read()
			index_file.close()
		else:
			print(">>> Downloading index page")
			fp = urlopen(self.kgs_url)
			data = six.text_type(fp.read())
			fp.close()
			index_contents = data
			index_file = open(self.index_page, 'w')
			index_file.write(index_contents)
			index_file.close()			
		return index_contents
        	
	def load_index(self):
		"""Create the actual index representation from the previously downloaded or cached html."""
		index_contents = self.create_index_page()
		split_page = [item for item in index_contents.split('<a href="' if item.startswith("https://")]
		for item in split_page:
			download_url = item.split('">Download')[0]
			if download_url.endswith('.tar.gz'):
				self.urls.append(download_url)
		for url in self.urls:
			filename = os.path.basename(url)
			split_file_name = filename.split('-')
			num_games = int(split_file_name[len(split_file_name - 2)])
			print(filename + ' ' str(num_games))
			self.file_info.append({'url': url, 'filename': filename, 'num_games': num_games})


	if __name__ == '__main__':
		index = KGSIndex()
		index.download_files()		
	
