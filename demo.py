from image_quality_assessor import assess_image
import cv2
import matplotlib.pyplot as plt
import os
import argparse

def process_image(image_path):
    print('Скрипт запущен')
    
    #Проверяем наличие файла
    if not os.path.exists(image_path):
        print(f'Файл {image_path} не найден.')
        return
    
    #Загружаем изображение
    try:
        image = cv2.imread(image_path)
    except:
        print(f'Не удалось прочитать файл {image_path}.')
        return
    
    #Преобразовываем изображение в формат RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    #Выводим изображение на экран
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()

#Готовим запуск программы из командной строки
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some image.')
    parser.add_argument('--image', type=str, required=True, 
                       help='Path to the image file')
    
    args = parser.parse_args()
    try:
        process_image(args.image)
        print('Результаты проверки:', assess_image(args.image))
    except:
        print('Ошибка обработки изображения!')

    print('Скрипт завершил работу')