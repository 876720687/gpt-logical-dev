from pdf2image import convert_from_path
import easyocr
import cv2
import numpy as np



# 初始化EasyOCR
reader = easyocr.Reader(lang_list=['en'])  # 指定语言列表
pdf_path = '../tmp/wiper_manual_mechanical.pdf'
images = convert_from_path(pdf_path
                           # ,dpi=300  # 会影响识别率
                           )  # 将PDF转换为图像
extracted_text = ""

print("Start reading...")
for image in images:
    # 将PpmImageFile对象转换为numpy array格式
    image_np = np.array(image)

    try:
        results = reader.readtext(image_np)  # 使用EasyOCR识别图像中的文本-> 切换
        print("read success...")
        for (bbox, text, prob) in results:
            extracted_text += text + " "
    except Exception as e:
        print(f"Error while processing image: {e}")

print("Extract success!")

print(extracted_text)