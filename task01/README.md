# Bài tập 1: Thu dữ liệu âm thanh
## Danh sách link chủ đề
1. Thời sự:     https://vnexpress.net/thoi-su/thu-tuong-yeu-cau-ha-noi-tp-hcm-san-sang-moi-phuong-an-cach-ly-4076616.html
1. Góc nhìn:    https://vnexpress.net/goc-nhin/o-nha-khong-chan-4076209.html
1. Thế giới:    https://vnexpress.net/the-gioi/nguoi-goc-viet-nhiem-ncov-xin-nghi-ky-truoc-khi-ra-khoi-nha-4082135.html
1. Kinh doanh:  https://vnexpress.net/kinh-doanh/bo-cong-thuong-giai-thich-viec-xin-tiep-tuc-xuat-khau-gao-4074526.html
1. Giải trí:    https://vnexpress.net/giai-tri/phim-moi-ve-tham-tu-conan-an-khach-3775584.html
1. Thể thao:    https://vnexpress.net/bong-da/sau-doi-ung-ho-tap-trung-cach-ly-da-v-league-4076586.html
1. Pháp luật:   https://vnexpress.net/phap-luat/don-tra-thu-cua-nguoi-dan-ba-han-tinh-4081160.html
1. Giáo dục:    https://vnexpress.net/giao-duc/giao-vien-tim-cach-bao-mat-lop-hoc-online-4083929.html
1. Sức khoẻ:    https://vnexpress.net/suc-khoe/nguoi-phu-nu-khong-the-giu-co-thang-4075152.html
1. Đời sống:    https://vnexpress.net/doi-song/9-meo-hieu-qua-tri-chieu-tro-cua-tre-4075337.html
1. Du lịch:     https://vnexpress.net/du-lich/van-ly-truong-thanh-don-khach-tro-lai-4074897.html
1. Khoa học:    https://vnexpress.net/khoa-hoc/loai-than-lan-de-trung-va-sinh-con-cung-luc-4082961.html
1. Số hoá:      https://vnexpress.net/so-hoa/internet-khap-the-gioi-cham-4076046.html
1. Xe:          https://vnexpress.net/oto-xe-may/trien-lam-oto-tro-thanh-benh-vien-da-chien-4076425.html
1. Ý kiến:      https://vnexpress.net/y-kien/bon-dieu-tot-lanh-khi-o-nha-chong-dich-4080125.html
1. Tâm sự:      https://vnexpress.net/tam-su/muon-thu-nhan-chuyen-sai-trai-voi-chong-4076229.html

## Cấu trúc cây thư mục
Mỗi thư mục chứa một chủ đề. Trong mỗi thư mục chứa:
1. `content.txt`: Chứa đường dẫn và nội dung bài báo ứng với chủ đề đó theo định dạng
    ```
        Dòng 1: <đường dẫn bài báo>
        Dòng 2 trở đi: mỗi dòng là 1 đoạn văn (paragraph) của bài báo
    ```
    Chương trình Python `do_tokenize.py` sẽ sử dụng các file `content.txt` để sinh ra các file `info.txt` dưới đây
1. `info.txt`: Được sử dụng để cung cấp thông tin cho chương trình ghi âm `recorder.py`, nội dung trong file có định dạng
    ```
        Dòng 1: Link: <đường dẫn bài báo>
        Dòng 2 trở đi: thông tin các câu biểu diễn theo 2 dòng một:
            Dòng 1: <tên file wav chứa nội dung ghi âm của câu>
            Dòng 2: nội dung câu cần ghi âm
    ```
1. Còn lại là danh sách các file `*.wav` là các đoạn ghi âm tương ứng như trong file `info.txt` đã ghi chú
---
*Phạm Thanh Tùng - 17020042 - QH-2017-I/CQ-C-A-C*