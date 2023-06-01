# Gif-Argument-Reality-and-Change-Background-in-Real-Time-Python-
Nhận dạng hình ảnh từ Webcam và chuyển thành Gif. Sau đó thay đổi nền với đối tượng nhận dạng là Gif đầu ra.

(Detect image from Webcam and convert to Gif. Then change background with object is Gif)



**Detect image and convert to Gif use 2 Algorithm:**
> ORB(Oriented and Rotated BRIEF ): Thuật toán này có thể phát hiện và mô tả đặc trưng như góc, điểm, cạnh ,… một cách đơn giản và nhanh chóng.

> Brute-Force Matcher: thuật toán so sánh tất cả các cặp đặc trưng của ảnh với nhau để tìm ra cặp đặc trưng tốt nhất.

**Remove and change background use package in OpenCV:**
> cvzone: một công cụ thị giác máy tính giúp thực hiện các chức năng xử lý hình ảnh như nhận diện khuôn mặt, theo dõi bàn tay, ước tính tư thế và các chức năng trí tuệ nhân tạo khác. 

> Self Segmentation: Module Self Segmentation trong cvzone được sử dụng để loại bỏ phông nền của ảnh selfie chụp. Quá trình này giúp tách riêng người chụp khỏi nền và tạo điều kiện cho việc thay thế phông nền.

**My project has list background, you just need use keyboard to change other background:** (*You can replace in my code*)
'1': previous background
'2': next background


To use cvzone you need install:
`!pip install mediapipe 
!pip install cvzone`


Ouput of project:

![Image](https://user-images.githubusercontent.com/75652144/242340771-4d2af3da-11f6-4a16-9dd0-7f1aea1335aa.jpg)

_`Unzip background(list background) and imageandgif(contains of 2 files in my code)`_
