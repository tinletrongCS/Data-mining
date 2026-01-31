**Cấu trúc dự án**

        .
        ├── README.md
        ├── __pycache__
        │   └── code.cpython-312.pyc
        ├── data                      # File dataset gốc - không chỉnh sửa !!
        │   └── jewelry.csv
        ├── main.ipynb                # File chính để tổng hợp kết quả
        ├── notebooks                 # Nơi để mỗi người nháp code 
        │   ├── tin.ipynb
        │   ├── toan.ipynb
        │   └── ton.ipynb
        ├── requirements.txt
        ├── setting.json
        └── src                       # Trong đây chứa các hàm dùng chung 
            └── __init__.py
            ├── preprocessing.py      # Các hàm tiền xử lý dữ liệu
            └── visualization.py      # Vẽ hình 

**Chạy dự án từ đầu**

    1. Nhấn Ctrl + Shifft + P, chọn Python: Select Interpreter

<img width="746" height="443" alt="image" src="https://github.com/user-attachments/assets/a718cdf1-b799-450f-94d1-06c7829e1d7b" />

    2. Tạo môi trường ảo mới 

<img width="742" height="263" alt="image" src="https://github.com/user-attachments/assets/be6a5e33-624c-4eb9-93d5-933e05c7cfd4" />

    3. Chọn tiếp Venv

<img width="742" height="97" alt="image" src="https://github.com/user-attachments/assets/29e48aaf-78d1-4cb8-a27c-83a708d3a4f5" />

    4. Chọn python.exe nằm trong AppData

<img width="753" height="247" alt="image" src="https://github.com/user-attachments/assets/223ade53-2e30-47f7-af07-ef672171acb8" />

    5. Click chọn cài đặt tất cả thư viện trong requirements.txt, chờ cho nó tải xong (tầm 3-5 phút tùy máy)

<img width="748" height="111" alt="image" src="https://github.com/user-attachments/assets/398d3760-c82f-4c25-af86-0905ccb1661e" />


**Cấu hình trước khi chạy - Khuyến khích chạy trong WSL thì tốc độ restart Kernel sẽ nhanh hơn**

    1. Cài extension Jupyter của Microsoft

    2. Trên góc phải, chọn Kernel, và tạo một .venv mới

    3. Sau đó chọn cài đặt tất cả trong requirements.txt

    4. Lưu ý khi mỗi người tự code (trong các file toan.ipynb, ton.ipynb) thì chọn Kernel khớp với Kernel đã chọn ở ngoài thư mục gốc vừa làm. 

<img width="1452" height="283" alt="image" src="https://github.com/user-attachments/assets/d3e7cd5d-80d7-4982-91c5-ab7df0339376" />

**Nếu vào VS Code mở các file .ipynb lên mà nó bị treo thì đóng VS Code rồi vào lại**

**Tạo thử từng cell code và chạy thử xem kết quả**

<img width="1446" height="405" alt="image" src="https://github.com/user-attachments/assets/1f5828bb-06a4-4c89-af02-92673173471b" />


    Nó hiện từng cell như vầy, code cell nào thì bấm chạy cell đó.

**Trong file src**

    Khi thêm một hàm mới trong mỗi file của ae, ví dụ Tín thêm hàm func_1() để xử lý, chạy test xong nếu thấy OK thì copy hàm đó vào src/preprocessing.py.

    Để tái sử dụng, khi Tôn thao tác trong ton.ipynb thì gọi 'from src.preprocessing import func_1'

    Good luck ae.

<img width="1863" height="553" alt="image" src="https://github.com/user-attachments/assets/3631caf3-86be-4cda-b74d-8dc8010e0a13" />

     Khi có thay đổi bên file trong src/ thì muốn chạy lại: 

<img width="1042" height="637" alt="image" src="https://github.com/user-attachments/assets/81b80be9-74e3-467e-b3db-dd9415721917" />


**[git1] - Tạo 1 nhánh mới và commit lên**

    git checkout -b <tên_nhánh_mới>
    
    git add .
    
    git commit -m "<nội dung muốn ghi>"
    
    git push origin <tên_nhánh_mới>

**[git2] - Trước khi tạo Pull Request cần check xem có bị conflict không**

    git checkout dev 

    git pull origin dev

    git checkout <tên_nhánh_của_ae>

    git merge dev

    (Nếu không báo conflict thì thực hiện tiếp)

    git add .

    git commit -m "<nội dung muốn ghi>"

    git push origin <tên_nhánh_mới>

    (Lưu ý tên_nhánh_mới là nhánh của mình do ae tự đặt tên)

    
  
  















