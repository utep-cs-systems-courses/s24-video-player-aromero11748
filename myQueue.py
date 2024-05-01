#! /usr/bin/env python3
import queue
import threading
import time
import ExtractAndDisplay
import ConvertToGreyscale
import DisplayFrames
import ExtractFames

def convert_to_grayscale(input_buffer, output_buffer):
    
    count = 0
    input_frame = input_buffer.get()
    
    while not (isinstance(input_frame, str) and input_frame == "END"):
        print(f'Converting frame {count}')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)
        
        # write output file
        output_buffer.put(grayscaleFrame)

        count += 1

        # load the next frame
        input_frame = input_buffer.get()
    
    output_buffer.put("END")

def blockingQ(capacity):
    emptyS = threading.Semaphore(capacity)
    fullS = threading.Semaphore(capacity)
    conventionalQ = queue.Queue(capacity)
    Qlock = threading.Lock()
    
    def putItem(n):
        emptyS.acquire()
        Qlock.acquire()
        conventionalQ.put(n)
        Qlock.release()
        fullS.release()
        
    def getItem():
        fullS.acquire()
        Qlock.acquire()
        item = conventionalQ.get()
        Qlock.release()
        emptyS.release()
    
fileName = 'clip.mp4'        
# Create a blocking queue
exQ, gsQ = blockingQ(10)

# Create threads for producing and consuming items
exQ_thread = threading.Thread(target=lambda: ExtractAndDisplay.extractFrames(fileName, exQ, 72))

gsQ_thread = threading.Thread(target=lambda: convert_to_greyscale(exQ, gsQ))

dis_thread = threading.Thread(target=lambda: ExtractAndDisplay.displayFrames(gsQ))
threading.Thread()


# Start threads
exQ_thread.start()
gsQ_thread.start()
dis_thread.start()

# Wait for threads to finish
#producer_thread.join()
#consumer_thread.join()
