#-*- coding: utf-8 -*-

from watchdog.observers import Observer
from watchdog.events import *

class FileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        pass

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))

if __name__ == "__main__":
    import time
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, r"./", False)
    observer.start()
    print(observer.name)
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()