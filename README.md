# FG Video Recorder

RTSP 스트림 또는 웹캠 영상을 실시간으로 시청하고, 프레임 보간과 함께 녹화할 수 있는 OpenCV 기반 영상 녹화 도구입니다.

## 기능

- **실시간 스트림 재생** — RTSP URL 또는 웹캠(로컬 장치) 입력 지원
- **녹화** — Space 키로 녹화 시작/중지, `output/` 폴더에 타임스탬프 파일명으로 저장
- **프레임 보간** — 녹화 시 프레임 사이에 보간 프레임을 삽입하여 부드러운 영상 생성
  - `1`: 보간 OFF (원본 30fps)
  - `2` ~ `6`: n배 보간 (60fps ~ 180fps)
- **REC 표시** — 녹화 중 화면 우상단에 빨간 원과 REC 텍스트 오버레이

## 요구사항

```bash
pip install opencv-python opencv-contrib-python
```

## 사용법

```bash
# 웹캠 사용 (인수 없음)
python main.py

# RTSP 스트림 사용
python main.py rtsp://your.stream.url/live/channel.stream

# 로컬 영상 파일 사용
python main.py video.mp4
```

### 키 조작

| 키 | 동작 |
|---|---|
| `Space` | 녹화 시작 / 중지 |
| `1` | 프레임 보간 OFF |
| `2` ~ `6` | n배 프레임 보간 ON |
| `ESC` | 프로그램 종료 |

## 출력

녹화된 파일은 `output/` 폴더에 MP4 형식으로 저장됩니다.

```
output/recorded_20260312_153045.mp4
```

## 설정

[main.py](main.py) 상단에서 기본 FPS를 변경할 수 있습니다.

```python
base_fps = 30  # 기본 FPS
```
