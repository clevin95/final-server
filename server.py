from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
import simplejson
# import downloader
# import parser
# from sys import argv
import os

class S(BaseHTTPRequestHandler):
	def parse_POST(self):
		ctype, pdict = parse_header(self.headers['content-type'])
		if ctype == 'multipart/form-data':
			postvars = parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers['content-length'])
			postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
		else:
		    postvars = {}
		return postvars

	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		self.wfile.write("<html><body><h1>hi!</h1></body></html>")

	def do_HEAD(self):
		self._set_headers()
        
	def do_POST(self):
		print("NOTHING HERE")
		# self._set_headers()
		# self.data_string = self.rfile.read(int(self.headers['Content-Length']))

		# self.send_response(200)
		# self.end_headers()

		# data = simplejson.loads(self.data_string)
		# with open("test123456.json", "w") as outfile:
		#     simplejson.dump(data, outfile)
		# file_name = data['file_name']
		# downloader.download_image(file_name)
		# print(parser.parse_image(file_name))
		# return

PORT = int(os.environ['PORT'])
def run(server_class=HTTPServer, handler_class=S, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
	run()
    # if len(argv) == 2:
    #     run(port=int(argv[1]))
    # else:
    #     run()