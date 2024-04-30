# 필요한 라이브러리 임포트 #
import cv2
import numpy as np
import hashlib
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

# 타겟 원본 이미지 메타데이터에서 생성 날짜 추출 #
def get_image_creation_date(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data is not None:
            for tag_id in exif_data:
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == "DateTimeOriginal":
                    return exif_data[tag_id]
        date_input = input("이미지의 생성 날짜와 시간을 YYYY-MM-DD HH:MM:SS 형식으로 입력해주세요: ")
        return datetime.strptime(date_input, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

# 디지털 워터마크 생성 및 LSB 스테가노그래피 적용 #
def apply_lsb_steganography(image, watermark):
    watermark = ''.join([format(ord(i), '08b') for i in watermark])
    idx = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if idx < len(watermark):
                pixel = image[i, j]
                pixel_value = format(pixel, '08b')
                modified_pixel_value = pixel_value[:-1] + watermark[idx]
                image[i, j] = int(modified_pixel_value, 2)
                idx += 1
    return image

def embed_watermark(author_name, image_path, output_path):
    creation_date = get_image_creation_date(image_path) # 원본 이미지 생성 날짜 추출 함수 호출
    application_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 디지털 워터마크 적용 날짜 및 시간 추출 
    watermark_data = f"{author_name}|{creation_date}|{application_date}" # main()에서 입력받은 저작권자명 포함 watermark_data 생성
    
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # 지정된 파일 경로에서 이미지 읽기
    partially_watermarked_image = apply_lsb_steganography(np.copy(img), watermark_data) # LSB스테가노그래피 적용 함수 호출하여 원본 이미지의 복사본에 초기 워터마크 데이터 적용
    image_hash = hashlib.sha256(partially_watermarked_image.tobytes()).hexdigest() # 초기 워터마크가 적용된 이미지의 해시값 계산
    
    full_watermark = f"{watermark_data}|{image_hash}" # 초기 워터마크 데이터와 계산된 해시값을 결합하여 full_watermark 생성
    fully_watermarked_image = apply_lsb_steganography(np.copy(img), full_watermark) # LSB스테가노그래피 적용 함수 호출하여 원본 이미지의 복사본에 최종 워터마크 적용
    
    cv2.imwrite(output_path, fully_watermarked_image) # 최종적으로 워터마크가 적용된 이미지를 사용자가 지정한 경로(output_path)에 저장

"""
1) 원본 이미지에 초기 워터마크 정보 (저작권자명, 생성 날짜, 적용 날짜)를 적용
2) 이 워터마크가 적용된 이미지에 대해 해시값 계산
3) 계산된 해시값을 이미지에 추가적으로 적용 """

"""
복사본을 만든 직후에는 원본 이미지와 복사본 이미지의 해시값이 동일할 것입니다. 
해시 함수는 입력된 데이터의 바이트 내용을 기반으로 해시값을 생성하기 때문에, 데이터가 동일하면 해시값도 동일하게 나옵니다. 
따라서, 원본과 복사본이 변경되지 않은 상태에서는 두 이미지의 해시값이 같습니다."""

# 사용자 입력과 프로그램 실행 #
def main():
    author_name = input("저작권자명을 입력해주세요: ")
    image_path = input("대상 이미지 파일 경로를 입력해주세요: ")
    output_path = input("워터마크가 적용된 이미지를 저장할 경로를 입력해주세요: ")
    embed_watermark(author_name, image_path, output_path)
    print("워터마크 적용이 완료되었습니다.")

if __name__ == "__main__":
    main()
