import os
import glob
from pathlib import Path

def main():
    dataset_dir = Path('Dataset')
    img_dir = dataset_dir / 'img'

    # Поиск изображений и существующих разметок
    images = sorted(glob.glob(str(img_dir / '*.jpg')))
    labels = sorted(glob.glob(str(img_dir / '*.txt')))
    
    print(f"Всего изображений: {len(images)}")
    print(f"Всего файлов разметки: {len(labels)}")

    # Обработка изображений без разметки
    missing_labels_count = 0
    for img_path in images:
        label_path = Path(img_path).with_suffix('.txt')
        if not label_path.exists():
            open(label_path, 'w').close()
            missing_labels_count += 1
            
    print(f"Создано пустых файлов разметки (фоновые изображения): {missing_labels_count}")

    # Обновление файлов разбиения выборки абсолютными путями
    def fix_split_file(split_name):
        orig_path = dataset_dir / f'{split_name}.txt'
        with open(orig_path, 'r') as f:
            lines = f.read().splitlines()
        
        # правильные абсолютные пути для картинок
        fixed_lines = [os.path.abspath(img_dir / os.path.basename(line)) for line in lines]
        
        new_path = dataset_dir / f'{split_name}_fixed.txt'
        with open(new_path, 'w') as f:
            f.write('\n'.join(fixed_lines))
            
        return os.path.abspath(new_path)

    train_file = fix_split_file('train')
    val_file = fix_split_file('validation')
    test_file = fix_split_file('test')

    # 4. Создание конфигурационного файла dataset.yaml
    with open(dataset_dir / 'obj.names', 'r') as f:
        class_names = f.read().splitlines()

    data_yaml = f"""train: {train_file}
val: {val_file}
test: {test_file}

nc: {len(class_names)}
names: {class_names}
"""

    with open('dataset.yaml', 'w') as f:
        f.write(data_yaml)

    print(f"Файл dataset.yaml успешно создан в {os.path.abspath('dataset.yaml')}")

if __name__ == '__main__':
    main()