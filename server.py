import http.server
import socketserver
import argparse
import ipaddress
import sys
import os
 
VERSION = 1.0
PORT = 8081
IP = "0.0.0.0"
 
 
def start_web_server(ip, port, root):
    Handler = http.server.SimpleHTTPRequestHandler
    print("pyWebServer v{}".format(VERSION), " by HanselSoft")
    print("starting web server at {}:{}, root dir={}".format(ip, port, root))
 
    try:
        os.chdir(root)
        with socketserver.TCPServer((ip, port), Handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print("Error: ", e)
        sys.exit(-2)
 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int,
                        help='server port number, default is {}'.format(PORT),
                        default=PORT)
    parser.add_argument('--ip', '-i', 
                        help='bind to address, default is {}'.format(IP),
                        default=IP)
    parser.add_argument('--dir', '-d',
                        help='web server root directory, default is current \
                        directory', default=os.getcwd())
    args = parser.parse_args()
    try:
        ipaddress.ip_address(args.ip)
    except ValueError:
        print("Error: incorrect IP: ", args.ip)
        sys.exit(-1)
 
    if not os.path.isdir(args.dir):
        print("Error: directory '{}' is not existed.".format(args.dir))
        sys.exit(-1)
 
    start_web_server(args.ip, args.port, args.dir)
 
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)