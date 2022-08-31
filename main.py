import os
import time
import config

import page_source_storer
import page_source_extractor

from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

class myServer(BaseHTTPRequestHandler):

    def get_url(self, field, query):
        field_value = None
        try:
            field_value_dictionary = parse_qs(query)
            field_value = field_value_dictionary[field]
        except Exception as exception:
            pass
        return field_value

    def get_query_url(self, parsed_url):
        query =  parsed_url.query
        field = 'url'
        url_list = self.get_url(field, query)
        url = None
        if url_list:
            url = url_list[0]
        return url

    def write_message(self, message):
        self.wfile.write(bytes(f"<p>{message}</p><br/>", 'utf-8'))
        time.sleep(2)

    def process_query_url(self, parsed_url):
        url = self.get_query_url(parsed_url)
        self.write_message(f"please wait selenium is processing your test url : <span style='color:blue'>{url}</span>")
        try:
            getPageSource_object = page_source_extractor.getPageSource()
            page_source = getPageSource_object.get_page_source(url)
            self.write_message(f"<span style='color:green'>fetching data successful from test url</span>")
            localFiles_object = page_source_storer.localFiles()
            localFiles_object.save_html_file(page_source)
            self.write_message(f"webpage saved in server : <span style='color:#AF3C00'>{self.headers.get('Host')}</span>")
            self.write_message(f"to view webpage click <a href='http://localhost:8080/{config.html_file_name}'>here</a>")
            self.write_message(
                f"to download webpage click <a href='http://localhost:8080/{config.html_file_name}' download='{config.html_file_name}'>here</a>"
            )
        except Exception as exception:
            print(exception)
            self.write_message(f"<span style='color:red'>failed processing test url</span>")

    def check_file_exists(self):
        html_file_path = None
        if os.path.exists(config.html_file_name):
            html_file_path = os.path.join(os.getcwd(), config.html_file_name)
        return html_file_path

    def process_html_file(self):
        html_file_path = self.check_file_exists()
        if html_file_path:
            with open(html_file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.write_message(f"<span style='color:red'>sorry webpage does not exist</span>")

    def send_success_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_not_found_headers(self):
        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        if path == '/GetPageSource' or path == '/favicon.ico' or path == '/' + config.html_file_name:
            self.send_success_headers()
            if path == '/GetPageSource':
                self.process_query_url(parsed_url)
            elif path == '/' + config.html_file_name:
                self.process_html_file()
        else:
            self.send_not_found_headers()

def main():
    web_server = HTTPServer((config.host_name, config.server_port), myServer)
    print(f"server started http://{config.host_name}:{config.server_port}")
    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    web_server.server_close()
    print('server stopped')

if __name__ == '__main__':
    main()