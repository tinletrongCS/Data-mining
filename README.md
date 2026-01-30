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
            
**Cấu hình trước khi chạy**

    1. Cài extension Jupyter của Microsoft

    2. Trên góc phải, chọn Kernel, và tạo một .venv mới

    3. Sau đó chọn cài đặt tất cả trong requirements.txt

    4. Lưu ý khi mỗi người tự code (trong các file toan.ipynb, ton.ipynb) thì chọn Kernel khớp với Kernel đã chọn ở ngoài thư mục gốc vừa làm. 

<img width="1452" height="283" alt="image" src="https://github.com/user-attachments/assets/d3e7cd5d-80d7-4982-91c5-ab7df0339376" />


   

**Tạo thử từng cell code và chạy thử xem kết quả**

<img width="1452" height="552" alt="image" src="https://github.com/user-attachments/assets/9c1422c9-9fb6-4514-8ba8-b3a897103c0d" />

    Nó hiện từng cell như vầy, code cell nào thì bấm chạy cell đó.


**Tạo 1 nhánh mới và commit lên**

    git checkout -b <tên_nhánh_mới>
    
    git add .
    
    git commit -m "<nội dung muốn ghi>"
    
    git push origin <tên_nhánh_mới>

**Trước khi tạo Pull Request cần check xem có bị conflict không**

    git checkout dev 

    git pull origin dev

    git checkout <tên_nhánh_của_ae>

    git merge dev

    (Nếu không báo conflict thì thực hiện tiếp)

    git add .

    git commit -m "<nội dung muốn ghi>"

    git push origin <tên_nhánh_mới>

    (Lưu ý tên_nhánh_mới là nhánh của mình do ae tự đặt tên)

    
  
  






