### Lý thuyết
Phương pháp giấu tin ***Structure Preserving*** (Bảo toàn cấu trúc) - Phương pháp giấu tin mà không thay đổi cấu trúc cơ bản của dữ liệu hoặc gói tin, giúp tránh bị phát hiện bởi các hệ thống giám sát, phân tích giao thức.

Kỹ thuật ***Structure Preserving*** cụ thể được bài lab mô phỏng là ***Reserved/Ununsed***. Các giao thức mạng thường có các fields hoặc bit trong header được đánh dấu là “dự trữ” hoặc “chưa sử dụng” để đảm bảo tính tương thích với các phiên bản tương lai. Bình thường, những fields này thường không được sử dụng, do đó có thể được khai thác để nhúng thông tin bí mật mà không ảnh hưởng đến chức năng của giao thức.

Kịch bản của bài lab:

*Trên máy gửi (Sender)*:

- Chuỗi tin nhắn được chuyển thành nhóm 3-bit (do trường reserved trong TCP header chỉ có 3 bit).
- Mỗi nhóm 3-bit được đặt vào trường reserved của gói TCP.
- Các gói tin được gửi đi với:

    - IP nguồn (src_ip) và IP đích (dst_ip) cố định.
    - Cờ ACK (Flags="A") để mô phỏng gói tin hợp lệ.
    - Số thứ tự (seq) tăng dần để đảm bảo thứ tự nhận.

- 3 gói FIN (Flags="F") với reserved=7 được gửi cuối cùng để đánh dấu kết thúc.

*Trên máy nhận (Receiver)*:

- Bắt các gói TCP từ IP nguồn 173.30.0.3 (máy Sender) đến IP đích 173.30.0.4 (máy Container).
- Trích xuất 3-bit từ trường reserved của mỗi gói.
- Khi nhận được gói FIN + reserved=7, máy nhận biết tin nhắn đã kết thúc.
- Ghép các bit lại, chuyển thành chuỗi ký tự ASCII (8-bit/char) để khôi phục tin nhắn gốc.

### Cài đặt và chạy bài lab
Dùng lệnh sau để tải bài lab:

    imodule https://raw.githubusercontent.com/DucThinh47/network-steganography/refs/heads/main/imodule3.tar

Chạy bài lab:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image.png?raw=true)

### Hướng dẫn thực hiện bài lab

*Checkwork 1*<br>
Trên máy Monitor, thực thi file text_to_bit_groups.py:

    python3 text_to_bit_groups.py

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image1.png?raw=true)

Output là 3 bit ***Reserved*** trong trường ***Flags*** của TCP header tương ứng với từng ký tự trong thông điệp "hi".<br>
Mở file và thay đổi thông điệp thành "HelloPTIT":

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image2.png?raw=true)

Thực thì file và lưu output vào result_bit_groups.txt: 

    python3 text_to_bit_groups.py > result_bit_groups.txt

In ra nội dung file result_bit_groups.txt:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image3.png?raw=true)

*Checkwork 2*<br>
Trên máy Receiver, thực thi file receive_reserved_unused.py để lắng nghe gói tin đến:

    sudo python3 eceive_reserved_unused.py

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image4.png?raw=true)

Trên máy Sender, thực thi file send_reserved_unused.py và nhập thông điệp:

    sudo python3 send_reserved_unused.py
Quan sát quá trình giấu và tách tin:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image5.png?raw=true)

*Checkwork 3*<br>
Trên máy Receiver, dùng ***tcpdump*** trên máy Receiver để lưu lưu lượng gói tin đến vào file .pcap:

    sudo tcpdump -i eth0 "tcp and src 173.30.0.3 and dst 173.30.0.4" -w captured_traffic.pcap

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image6.png?raw=true)

Trên máy Sender, thực thi file send_reserved_unused.py và nhập thông điệp:

    sudo python3 send_reserved_unused.py
Trên máy Receiver, sau khi máy Sender đã gửi hết gói tin, Ctrl + C để dừng ***tcpdump***:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image7.png?raw=true)

Mở dịch vụ ***ssh*** trên máy Monitor:

    sudo systemctl start ssh

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image8.png?raw=true)

Chuyển file captured_traffic.pcap từ máy Receiver sang máy Monitor:

    scp captured_traffic.pcap ubuntu@173.30.0.5:/home/ubuntu/
Nhập password là ***ubuntu***:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image9.png?raw=true)

Trên máy Monitor mở file captured_traffic.pcap:

    wireshark captured_traffic.pcap &

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image10.png?raw=true)

Quan sát trong Wireshark các gói tin có các bit ***Reserved*** được set:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image11.png?raw=true)

*Checkwork 4*<br>
Trên máy Receiver, thực thi file receive_reserved_unused.py và lưu kết quả vào hidden_mess.txt:
    
    sudo python3 receive_reserved_unused.py > hidden_mess.txt

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image12.png?raw=true)

Trên máy Sender, thực thi file send_reserved_unused.py và nhập thông điệp là mã sinh viên của mình, sau đó gửi thông điệp:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image13.png?raw=true)

Trên máy Receiver, in ra nội dung file hidden_mess.txt:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image14.png?raw=true)

Checkwork bài lab:

![img](https://github.com/DucThinh47/network-steganography/blob/main/images/image15.png?raw=true)
