**Lưu ý chạy trong WSL**

    python3 -m venv venv
    
    source venv/bin/activate
    
    pip install -r requirements.txt 
    
    python3 jewelry.py

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

    
  
  

