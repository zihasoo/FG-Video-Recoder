import sys
import cv2 as cv
import numpy as np
from datetime import datetime

is_recording = False
video_writer = None
width = None
height = None
base_fps = 30
fps = base_fps
interp_multiplier = 1 
prev_img = None
if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    source = 0
cap = cv.VideoCapture(source)
wait_ms = 1

ret, img = cap.read()

if ret:
    height, width = img.shape[:2]
    print(f"프레임 크기: {width}x{height}")

print("프로그램 시작 - Space: 녹화 시작/중지, 1: 보간 OFF, 2 ~ 6: n배 보간, ESC: 종료")

while True:
    ret, img = cap.read()
    
    if not ret:
        print("에러: 프레임을 읽는데 실패했습니다.")
        break

    display_img = img.copy()

    if is_recording:
        cv.circle(display_img, (width - 30, 30), 15, (0, 0, 255), -1)
        cv.putText(display_img, 'REC', (width - 100, 40), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        if interp_multiplier > 1 and prev_img is not None:
            for i in range(1, interp_multiplier):
                alpha = i / interp_multiplier
                interp_img = cv.addWeighted(prev_img, 1 - alpha, img, alpha, 0)
                video_writer.write(interp_img)
        
        video_writer.write(img)

    prev_img = img
    
    cv.imshow('CCTV', display_img)
    
    key = cv.waitKey(wait_ms)
    
    if key == 27:
        break

    elif key == ord('1'):
        interp_multiplier = 1
        fps = base_fps
        print("프레임 보간 OFF")

    elif key in [i for i in range(ord('2'), ord('7'))]:
        interp_multiplier = key - ord('0')
        fps = base_fps * interp_multiplier
        print(f"{interp_multiplier}배 프레임 보간 ON ({fps}fps)")

    elif key == 32:
        is_recording = not is_recording
        
        if is_recording:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/recorded_{timestamp}.mp4"
            
            fourcc = cv.VideoWriter_fourcc(*'mp4v')
            video_writer = cv.VideoWriter(filename, fourcc, fps, 
                                            (width, height))
            
            # VideoWriter가 제대로 열렸는지 확인
            if video_writer.isOpened():
                print(f"녹화 시작: {filename} ({width}x{height}, {fps}fps)")
            else:
                print("녹화 시작 실패!")
                video_writer = None
                is_recording = False
        else:
            if video_writer is not None:
                video_writer.release()
                video_writer = None
            print("녹화 중지")

if video_writer is not None:
    video_writer.release()
cap.release()
cv.destroyAllWindows()
print("프로그램 종료")
