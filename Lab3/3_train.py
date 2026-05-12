import os
import subprocess

def main():
    yolo_dir = "yolov5"
    
    if not os.path.exists(yolo_dir):
        print("Папка yolov5 не найдена.")
        return

    dataset_yaml_path = os.path.abspath("dataset.yaml")
    if not os.path.exists(dataset_yaml_path):
        print("Файл dataset.yaml не найден.")
        return

    print("Запуск скрипта обучения train.py...")

    train_cmd = [
        "python", "train.py",
        "--img", "640",
        "--batch", "16",
        "--epochs", "50",
        "--data", dataset_yaml_path,
        "--weights", "yolov5s.pt",
        "--optimizer", "Adam",
        "--name", "planes_detector_yolov5s"
    ]
    
    subprocess.run(train_cmd, cwd=yolo_dir)
    print("Обучение завершено. Лучшие веса сохранены в yolov5/runs/train/planes_detector_yolov5s/weights/best.pt")

if __name__ == '__main__':
    main()
