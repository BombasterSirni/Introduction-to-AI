import os
import subprocess

def main():
    
    if not os.path.exists("yolov5"):
        print("Клонирование репозитория YOLOv5...")
        subprocess.run(["git", "clone", "https://github.com/ultralytics/yolov5", "-q"], check=True)
    else:
        print("Репозиторий YOLOv5 уже склонирован.")
        
    print("Установка зависимостей...")
    subprocess.run(["pip", "install", "-r", "yolov5/requirements.txt"], check=True)
    
    print("YOLOv5 готов к работе.")

if __name__ == '__main__':
    main()
