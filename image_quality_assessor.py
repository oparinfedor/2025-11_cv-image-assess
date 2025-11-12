import cv2
import numpy as np

def assess_image(image_path):
  if isinstance(image_path, str):
    img = cv2.imread(image_path)
  else:
    img = image_path.copy()
  gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  #Определяем степень размытости через дисперсию оператора Лапласа
  var_lap = cv2.Laplacian(gray_img, cv2.CV_64F).var()
  blur_treshold = 80
  blur_score = var_lap
  too_blurry = blur_score <= blur_treshold
  
  #Определяем контрастность с использованием гистограммы яркости
  mean_brightness = np.mean(gray_img)
  std_deviation = np.std(gray_img)
  contrast_score = std_deviation / mean_brightness
  low_contrast_threshold = 0.1 
  high_contrast_threshold = 0.5
  low_contrast = contrast_score < low_contrast_threshold
  high_contrast = contrast_score > high_contrast_threshold

  #Измеряем среднюю интенсивность пикселей и определяем уровень освещенности
  brightness_score = mean_brightness
  dark_threshold = 50
  bright_threshold = 200
  under_exposed = brightness_score < dark_threshold
  over_exposed = brightness_score > bright_threshold

  #Определяем количество пикселей со слишком высокой (клиппированные) и слишком низкой (недоэкспонированные) яркостью
  hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
  clipped_pixels = hist[:10].sum() + hist[-10:].sum()
  total_pixels = gray_img.size
  clipping_ratio = clipped_pixels / total_pixels
  clipping_threshold = 0.05
  excess_clipping = clipping_ratio >= clipping_threshold

  #Формируем итог: пригодно изображение для обработки или нет
  is_usable = not any([
      too_blurry, low_contrast, high_contrast, under_exposed, over_exposed, excess_clipping
   ])

  #Формируем список "диагнозов"
  reasons = []
  if too_blurry:
      reasons.append('Too Blurry') #слишком размыто
  if low_contrast or high_contrast:
      reasons.append('Low Contrast' if low_contrast else 'High Contrast') #низкий или высокий контраст
  if under_exposed or over_exposed:
      reasons.append('Under Exposure' if under_exposed else 'Over Exposure') #низкая или высокая освещенность
  if excess_clipping:
      reasons.append('Excess Clipping') #пиксели с экстремальной яркостью

  return {
      'is_usable': is_usable,
      'blur_score': blur_score,
      'contrast_score': contrast_score,
      'brightness_score': brightness_score,
      'clipping_ratio': clipping_ratio,
      'reasons': reasons
  }