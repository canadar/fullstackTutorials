from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import cgi

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/menus"):
			#connect to the database and bind the metadata
				self.engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = self.engine
				self.DBSession = sessionmaker(bind=engine)
			#assign the session and pull all restaurants from the database, store collection.
				self.session = self.DBSession
				self.restaurants = session.query(Restaurant).all()
				output = ""
				output += "<html><body>"
				for item in self.restaurants:
					output += "<h1>%s</h1><br />" % item.name
				#insert from to add new data
				
				output += "</body></html>"
				
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
				
			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				output += "&#161Hola!"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
		except:
			self.send_error(404, 'File Not Found %s' % self.path)
			
	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()
			
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
				
			output = ""
			output += "<html><body>"
			output += "<h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"> </form>'''
			output += "</body></html>"
			self.wfile.write(output)
			print output
			
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print 'Web server running on port %s' % port
		server.serve_forever()
	except KeyboardInterrupt:
		print"^C entered, stopping web server..."
		server.socket.close()

if __name__=='__main__':
	main()