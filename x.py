import http.server
import json

class Server(http.server.BaseHTTPRequestHandler):
    
    def send_ok(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
    
    def send_bad(self):
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Error 404')
    
    def do_GET(self):
        path_name = self.path
        try:
            if self.path == '/directors':
                    data = ""
                    with open('database.json', 'r') as read_file:
                        data = json.load(read_file)
                        response = json.dumps(data)
                        self.send_ok()
                        self.wfile.write(response.encode())
            
            elif  '/directors/' in path_name:
                    id = int(path_name.split('/')[-1])
                    json_data = []
                    with open('database.json', 'r') as read_file:
                        json_data = json.load(read_file)
                    
                    ans = ""
                    flag=False
                    for item in json_data:
                        if int(item["id"])==id:
                            flag=True
                            ans = item["name"]
                            break
                    if not flag:
                        raise Exception()
                    self.send_ok()
                    response='Director name with id ' + str(id) + ' is ' + ans
                    self.wfile.write(bytes(response.encode('utf-8')))
            else:
                raise Exception()
        except:
            self.send_bad()
            

    def do_POST(self):
        try:
            if self.path == '/directors':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                json_data = []
                with open('database.json', 'r') as read_file:
                    json_data = json.load(read_file)
                
                json_data.append(json.loads(post_data.decode()))
                
                with open('database.json', 'w') as write_file:
                    json.dump(json_data, write_file)
                
                self.send_response(201)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'New director added!')
        except:
            self.send_bad()
            
    def do_PUT(self):
        path_name = self.path
        if '/directors/' in path_name:
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data_str = data.decode('utf-8')
            
            json_data = []
            with open('database.json', 'r') as read_file:
                json_data = json.load(read_file)
            
            post_data = json.loads(data_str)
            
            for item in json_data:
                if post_data["id"] == item["id"]:
                    item.update(post_data)
                    break
            
            with open('database.json', 'w') as write_file:
                json.dump(json_data, write_file)
            
            self.send_response(201)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Director updated!')
    
    def do_DELETE(self):
        path_name = self.path
        if '/directors/' in path_name:
            id = int(path_name.split('/')[-1])
            
        json_data = []
        with open('database.json', 'r') as read_file:
            json_data = json.load(read_file)
        
        updated_data = []
        for item in json_data:
            if int(item["id"])!=id:
                updated_data.append(item)
        
        with open('database.json', 'w') as write_file:
            json.dump(updated_data, write_file)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Director deleted!')
    
PORT = 8000
server_address = ('localhost', PORT)
httpd = http.server.HTTPServer(server_address, Server)

print("Server started on port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()
    print("Server closed")

