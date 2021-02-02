from simple_barcode_detection import detect 
from imutils.video import VideoStream
import argparse
import time
import cv2
#import Pillow
from pyzbar import pyzbar


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect        #1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        #2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)        #3
        #with open("barcode_result.txt", mode ='w') as file:
         #   file.write("Recognized Barcode:" + barcode_info)    

    return frame

def croping(img,box):


	out = np.zeros_like(img) # Extract out the object and place into output image
	out[mask == 255] = img[mask == 255]

	# Now crop
	(y, x) = np.where(mask == 255)
	(topy, topx) = (np.min(y), np.min(x))
	(bottomy, bottomx) = (np.max(y), np.max(x))
	out = out[topy:bottomy+1, topx:bottomx+1]

	return out


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
args = vars(ap.parse_args())

if not args.get("video", False):
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

else:
	vs = cv2.VideoCapture(args["video"])


while True:

	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame
 

	if frame is None:
		break
	# detect the barcode in the image
	box = detect(frame)
	#croped=croping(frame,box)
	#frame=read_barcodes(box)

	


	if box is not None:
		cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

if not args.get("video", False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()