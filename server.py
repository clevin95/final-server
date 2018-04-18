from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import simplejson
import json
import downloader
import parser
# import crop
import os

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
    
	def do_POST(self):
		self._set_headers()
		body_data = self.rfile.read(int(self.headers['Content-Length']))

		self.end_headers()

		data = simplejson.loads(body_data)
		file_name = data['file_name']
		print(file_name)
		downloader.download_image(file_name)


		# signs = crop.signs_from_image(file_name)
		# print(signs)

		# red_signs = signs["red"]
		# green_signs = signs["green"]

		# response = {}
		# response["red"] = parser.parse_image(red_signs)
		# response["green"] = parser.parse_image(green_signs)

		# formatted_json = json.dumps(response)
		# self.wfile.write(formatted_json.encode())

PORT = int(os.environ['PORT'])
def run(server_class=HTTPServer, handler_class=S, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
	run()
