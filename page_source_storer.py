import os
import codecs

from config import html_file_name

class localFiles:

    def __init__(self):
        self.current_directory_path = os.getcwd()
        self.set_html_file_path()

    def set_html_file_path(self):
        self.html_file_path = os.path.join(self.current_directory_path, html_file_name)

    def save_html_file(self, html):
        file = codecs.open(self.html_file_path, 'w', 'utf−8')
        file.write(html)
        file.close()