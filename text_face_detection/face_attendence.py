import cv2 
import pytesseract
import re
# img = cv2.imread('./image/id_4.jpg')
# print(img)
# cv2.imshow("ID_CARD" , img)
# cv2.waitKey(0)

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"
# faces = cascade.detectMultiScale(img , scaleFactor=1.1, minNeighbors=5, minSize=(5,5))
# print(faces)


#     cv2.imshow("face_rectengle" , img_rec)
# cv2.waitKey(0)

def convert_gray_color(file_path):
    img = cv2.imread(file_path)
    gray_image = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    # print(gray_image)
    return gray_image

def image_smoothing(img):
    ret , th1 = cv2.threshold(img, 127 , 255 , cv2.THRESH_BINARY)
    _ , th2 = cv2.threshold(th1, 0 , 255 , cv2.THRESH_BINARY)
    blur = cv2.GaussianBlur(th2 , (1,1), 0)
    # print(th1)
    return blur

def clean_text(read_data):
    text = re.sub('[=+,#/\?:^$.@*\"※~&%ㆍ!』\\"|\(\)\[\]\<\>`\"…》£"¢¥"Ÿ«éȮϽñٶϴ»「—©]', '',read_data )
    return text


img = convert_gray_color('./image/id_2.jpg')
smoothing_img = image_smoothing(img)
# cv2.imshow("smoothing_img" ,smoothing_img)
# cv2.waitKey(0)


# print(text)
config  = r'--oem 1 --psm 6 outoutbase digits' #숫자들만 인식
def rectangle_detect(file_path, lang='kor'):
    img = convert_gray_color(file_path)
    text = clean_text(pytesseract.pytesseract.image_to_string(img, lang='kor'))
    faces = cascade.detectMultiScale(img , scaleFactor=1.1, minNeighbors=5, minSize=(5,5))
    for i in faces:
        x , y ,w , h = i
        img_rec = cv2.rectangle(img , (x , y) , (x+w, y+h),(0,0,256), -1 )
    num_boxes = pytesseract.pytesseract.image_to_data(img , lang=lang,config=config )
    # print(num_boxes.splitlines())
    num_list=[]
    file_name = ''
    for x , b in enumerate(num_boxes.splitlines()):
        if x !=0:
            b = b.split()
            print(b)
            if len(b) ==12 and len(b[11])>11:
                num_list.append(b)
                # print(b)
    for i in range(len(num_list)):
        number = num_list[i][11]
        if len(number) ==14:
            if '-' in number:
                x , y , w, h =int(num_list[i][6]), int(num_list[i][7]), int(num_list[i][8]), int(num_list[i][9])
                img_rac = cv2.rectangle(img , (x , y) ,(x+w, y+h) , (0, 0, 256), -1 )
                naming_number = clean_text(num_list[i][11])
                for i in range(len(naming_number)):
                    if i%2 == 0:
                        file_name +=naming_number[i]
                print(file_name)
                # cv2.imshow("number", img_rac)
    if file_name:
        cv2.imwrite(f'result_img/{file_name}.jpg',img )
        with open(f'result_img/{file_name}.txt', 'w', encoding='UTF-8') as f:
            f.write(text)
            f.close()
        return f'result_img/{file_name}'
    # cv2.waitKey(0)
    else:
        import string
        import random
        number_of_string = 5
        length_of_string = 8
        for i in range(length_of_string):
            temp_filename=''.join(random.choice(string.ascii_letters+string.digits) for _ in range(number_of_string) )
        # print(temp_filename)
        cv2.imwrite(f'result_img/{temp_filename}.jpg',img)
        with open(f'result_img/{temp_filename}.txt', 'w', encoding='UTF-8') as f:
            f.write(text)
            f.close()
        return f'result_img/{temp_filename}'
# rectangle_detect('./image/id_6.jpg')
