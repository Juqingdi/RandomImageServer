#!/usr/bin/env python
#--coding:utf-8--

# import time

from sys import exit
from http.server import BaseHTTPRequestHandler, HTTPServer
from ipaddress import ip_address
from os import path, scandir
from argparse import ArgumentParser
from random import randint
from urllib.parse import urlparse
from watchdog.observers import Observer
from watchdog.events import *

curdir = path.dirname(path.realpath(__file__))
sep = '/'

IP = "127.0.0.1" #accessible to only this device
PORT = 8001

images = []
unvisited_images = []

# MIME-TYPE
mimedic = [
    # ('.html', 'text/html'),
    # ('.htm', 'text/html'),
    # ('.js', 'application/javascript'),
    # ('.css', 'text/css'),
    # ('.json', 'application/json'),
    ('.png', 'image/png'),
    ('.jpg', 'image/jpeg'),
    ('.jpeg', 'image/jpeg'),
    ('.gif', 'image/gif'),
    # ('.txt', 'text/plain'),
    # ('.avi', 'video/x-msvideo'),
]


class myHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        sendReply = False
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query
        # print(filepath)
        
        if filepath == '/randomPic':
            print(unvisited_images)
            if len(images) == 0:
                self.send_error(404, 'No Images Found')
                return
            randomIndex = randint(0, len(unvisited_images) - 1)
            filepath = unvisited_images[randomIndex]
            unvisited_images.pop(randomIndex)
            if len(unvisited_images) == 0:
                print('readd unvisited_images')
                for image in images:
                    unvisited_images.append(image)
                print('after readd', unvisited_images)

        # print('path', path)
        filename, fileext = path.splitext(filepath)
        # print(filename, fileext)
        for e in mimedic:
            if e[0] == fileext:
                mimetype = e[1]
                sendReply = True

        if sendReply == True:
            try:
                with open(path.realpath(curdir + sep + filepath),'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type',mimetype)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
        else:
            self.send_error(405, 'Only Images Are Accessible')

class FileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        pass

    def on_moved(self, event):
        if not(event.is_directory) and is_image(event.src_path):
            print("image renamed from {0} to {1}".format(event.src_path,event.dest_path))
            images[images.index(event.src_path)] = event.dest_path
            if event.src_path in unvisited_images:
                unvisited_images[unvisited_images.index(event.src_path)] = event.dest_path
            print(images, unvisited_images)

    def on_created(self, event):
        if not(event.is_directory) and is_image(event.src_path):
            print("image created:{0}".format(event.src_path))
            images.append(event.src_path)
            unvisited_images.append(event.src_path)
            print(images, unvisited_images)

    def on_deleted(self, event):
        if not(event.is_directory) and is_image(event.src_path):
            print("image deleted:{0}".format(event.src_path))
            images.remove(event.src_path)
            if event.src_path in unvisited_images:
                unvisited_images.remove(event.src_path)
            print(images, unvisited_images)

    def on_modified(self, event):
        pass

def is_image(filePath):
    if path.splitext(filePath)[1] in ['.png', '.jpg', '.jpeg', '.gif']:
        return True
    else:
        return False

def scan_image():
    dirs = scandir(r"./")
    for file in dirs:
        if file.is_file():
            if is_image(file.path):
                images.append(file.path)
                unvisited_images.append(file.path)
    print(images)

def watch_image():
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, r"./", False)
    observer.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()

def start_web_server(ip, port):
    print('starting server, port', port)
    # Server settings
    server_address = (ip, port)
    httpd = HTTPServer(server_address, myHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

def main():
    parser = ArgumentParser()
    parser.add_argument('--port', '-p', type=int,
                        help='server port number, default is {}'.format(PORT),
                        default=PORT)
    parser.add_argument('--ip', '-i', 
                        help='bind to address, default is {}'.format(IP),
                        default=IP)
    args = parser.parse_args()
    try:
        ip_address(args.ip)
    except ValueError:
        print("Error: incorrect IP: ", args.ip)
        exit(-1)

    scan_image()
    watch_image()
    start_web_server(args.ip, args.port)



if __name__ == '__main__':
    main()