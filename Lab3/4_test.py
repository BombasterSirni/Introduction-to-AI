import shutil
import os
import subprocess
import random


def main():
    yolo_dir = "yolov5"

    if not os.path.exists(yolo_dir):
        print("Папка yolov5 не найдена.")
        return

    dataset_yaml_path = os.path.abspath("dataset.yaml")
    best_weights = "runs/train/planes_detector_yolov5s/weights/best.pt"

    if not os.path.exists(os.path.join(yolo_dir, best_weights)):
        print(
            f"Веса {best_weights} не найдены. Обучение еще не проводилось или не завершено.")
        return

    print("\n--- 1. Получение метрик качества на тестовом наборе ---")
    val_cmd = [
        "python", "val.py",
        "--weights", best_weights,
        "--data", dataset_yaml_path,
        "--task", "test",
        "--name", "planes_test_metrics"
    ]
    subprocess.run(val_cmd, cwd=yolo_dir)

    print("\n--- 2. Визуальный инференс на случайных изображениях ---")
    test_fixed_path = "Dataset/test_fixed.txt"
    if not os.path.exists(test_fixed_path):
        print(f"Файл {test_fixed_path} не найден.")
        return

    with open(test_fixed_path, "r") as f:
        test_images = f.read().splitlines()

    # Берем 5 случайных изображений
    random_test_images = random.sample(test_images, min(5, len(test_images)))

    # Создаем временную папку с выбранными картинками
    tmp_img_dir = os.path.abspath("tmp_test_images")
    os.makedirs(tmp_img_dir, exist_ok=True)

    # Очищаем папку от предыдущих запусков
    for f in os.listdir(tmp_img_dir):
        os.remove(os.path.join(tmp_img_dir, f))

    # Копируем туда 5 случайных картинок
    for img_path in random_test_images:
        shutil.copy(img_path, tmp_img_dir)

    detect_cmd = [
        "python", "detect.py",
        "--weights", best_weights,
        "--img", "640",
        "--conf", "0.25",
        "--source", tmp_img_dir,
        "--name", "planes_inference"
    ]

    subprocess.run(detect_cmd, cwd=yolo_dir)
    print("\nИнференс завершён. Изображения с отрисованными боксами можно посмотреть в: yolov5/runs/detect/planes_inference/")


if __name__ == '__main__':
    main()
