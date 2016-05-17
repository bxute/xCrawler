# To Download All files of any site
# Find Regex for each level
# Call __initiate() with levels , website and regex list with respective height
# All the file will be stored with nested folder structure
# For speed purpose Download is single-threaded
import os
import re
from datetime import datetime,date
from os import mkdir, chdir, path
from threading import Thread
from urllib import request
from time import sleep

class Crawler:
    MaxHeight = 0
    regex = []
    website_url = ''

    def __init__(self, base_url, list_of_regex):
        self.MaxHeight = len(list_of_regex) - 1
        self.regex = list_of_regex
        self.website_url = base_url

    def __initiate__(self):
        if not path.isdir('download'):
            mkdir('download')
        chdir('download')
        print('Crawling Web: {0}'.format(self.website_url))  # debug
        _homePage = str(request.urlopen(str(self.website_url)).read())
        self._dive_down(_homePage, 0)

    def _dive_down(self, page, height):
        if height == self.MaxHeight:
            self._save(self.regex[height], page)
        else:
            page = re.sub(r'<img(.*?)\>', '', page)  # for removing <img> tag obstacle
            _url_list = re.findall(r'{0}'.format(self.regex[height]), page)
            for _link, _title in _url_list:
                title = _title[:len(_title) - 6]  # could be ==> re.sub(r'[t\/\\]+','',_title)
                if not path.isdir(title):
                    print('Making Directory: {0}'.format(title))  # debug
                    mkdir(title)
                else:
                    print('{0} already exits '.format(title))

                print('Changing Directory To: {0}'.format(title))  # debug
                chdir(title)
                new_url = '{0}/{1}'.format(self.website_url, _link)
                print('Crawling Web: {0}'.format(new_url))  # debug
                _npage = str(request.urlopen(new_url).read())
                self._dive_down(_npage, height + 1)

        chdir('../')

    def _save(self, regex, page):

        _files = re.findall(regex, page)
        for sub_dir, _title in _files:
            # --------------------------------------------------#
            # Website Based Custom Re-formatting #
            # --------------------------------------------------#
            file_name = re.sub('[ ]', '%20', _title)
            subpart1 = '/siteuploads/files/sfd9/'
            subpart2 = sub_dir[18:]
            postfix = '(Mp3Bhojpuri.com).mp3'
            file_name = file_name[:len(file_name) - 4] + postfix

            file = self.website_url + subpart1 + subpart2 + '/' + file_name
            print('Downloading file: {0}'.format(file))  # debug
            if not path.exists(_title):
                dnld_start_time = datetime.now().time().strftime('%H:%M:%S')
                _title=_title[:20].rstrip()+'.mp3'
                request.urlretrieve(file, _title)
                with open(_title,'r') as test_read:
                    try:
                        test_read.readline()
                        print('[Html Content]')
                        ## if exception not occurs means it`s a html file
                        ## so redownload with different path
                        subpart1 = '/siteuploads/files/sfd8/'
                        file = self.website_url + subpart1 + subpart2 + '/' + file_name
                        print('Redownloading file from {0}'.format(file) )
                        request.urlretrieve(file, _title)
                    except UnicodeDecodeError:
                        continue
                print('Downloaded...')
                dnld_end_time = datetime.now().time().strftime('%H:%M:%S')
                log_line = '{0}\t\t{1}\t\t{2}\t\t{3}\n'.format(_title, date.today(), dnld_start_time, dnld_end_time)
                with open('DownloadLog.txt','a+') as log_file:
                    log_file.write(str(log_line))
                log_file.close()
                print(log_line)

            else:
                print('{0} already downloaded....'.format(_title))



def main():
        print('Welcome')
        home='http://mp3bhojpuri.com'
        reg_list = ['catRow.*?\\/(.*?)\\">(.*?)\\<', 'fileNames".*?\\/(.*?)\\"><div><div></div><div>(.*?)\\<', 'fileNames".*?\\/(.*?)\\"><div><div></div><div>(.*?)\\<', 'fileName".*?\\/(.*?)\\"\\><div><div></div><div>(.*?)\\<', 'Download \\:\\<a class=\\"dwnLink\\" rel=.*?\\/(.*?)\\"\\>(.*?)\\<']
        crawler = Crawler(home, reg_list)
        task = Thread(target=crawler.__initiate__, args=())
        task.start()

if __name__ == '__main__':
    main()
