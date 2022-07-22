test = """
T hông tin cá nhân
Họ & tên
Nguyễn Trường Thi
Giới tính
Nam
Ngày sinh
22/02/1981
Quốc tịch
Việt Nam
Tình trạng hôn nhân
Đã kết hôn
Địa chỉ
82 Lien khu 2-5, Binh Tri Dong Ward , Hồ Chí Minh, Việt Nam
Điện thoại
0902220281
Email
t ruongt hi220281@gmail.com
nghề nghiệp
- Become an IT manager
Công việc mong muốn
Vị trí / Chức danh
IT Administ rat or
Cấp bậc
Quản lý
Mức lương
14,000,000 - 16,000,000 VND
Hình thức làm việc
Nhân viên chính thức
Ngành nghề
CNTT - Phần mềm, CNTT - Phần cứng / Mạng
Nơi làm việc
Hồ Chí Minh
"""
import re

x = re.finditer("IT Administ rat or", test)

for i in x:
    print(i)
