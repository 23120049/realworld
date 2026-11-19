# Video 2: GitHub Actions CI (5–7 phút)

## Chuẩn bị 5 tab

1. [Repository và README](https://github.com/thu2005/realworld/tree/next)
2. [Run CI thành công ngày 30/10/2026](https://github.com/thu2005/realworld/actions/runs/41007469847) — minh chứng 11 jobs, Jest, SuperTest, Docker và GHCR. Đây là run lịch sử trước khi bật audit gate thật.
3. [CI Pipeline trên nhánh `next`](https://github.com/thu2005/realworld/actions/workflows/ci.yml?query=branch%3Anext) — mở run mới nhất để minh họa npm audit fail-fast và artifact Allure.
4. [Run CodeQL](https://github.com/thu2005/realworld/actions/runs/41007469929) — mở thêm [Code scanning alerts](https://github.com/thu2005/realworld/security/code-scanning) trong cùng tab khi nói về kết quả.
5. [GHCR package](https://github.com/thu2005/realworld/pkgs/container/realworld) — đối chiếu tag `ef0684e72c2c2f4c35a42b468ce03a35e0ad48f3` với SHA của run lịch sử.

Mở sẵn file [`ci.yml`](../.github/workflows/ci.yml) và [`Dockerfile`](../Dockerfile) từ tab 1 nếu cần chỉ trực tiếp vào mã nguồn. Kiểm tra run mới và danh sách artifact ngay trước khi quay vì trạng thái CI và thời hạn lưu artifact thay đổi theo thời gian.

## Lời thoại gợi ý

### 0:00–0:45 — README và phạm vi

"Em là Dương Trọng Hòa, mã số sinh viên 23120127, phụ trách phần GitHub Actions CI của nhóm. Video này minh họa luồng kiểm thử, bảo mật, đóng gói và xuất bản image của dự án RealWorld. CI có 11 jobs. Huy hiệu CI phản ánh run mới nhất trên nhánh `next`; các huy hiệu 31 tests, 15 tests và coverage là số liệu của run đã xác minh, không tự cập nhật theo thời gian thực."

### 0:45–2:20 — Run thành công và kết quả kiểm thử

"Ở run thành công này, job Unit Tests chạy 31 bài Jest. Báo cáo cho thấy Statements, Lines và Functions đạt 100%; Branches đạt 94,73%. Job API Tests chạy 15 bài SuperTest. Hai job xuất JUnit XML và coverage làm artifact. Các job lint, unit, API và security là điều kiện trước khi Docker build chạy. Đây là các nhánh có quan hệ phụ thuộc trong DAG, không phải 11 jobs chạy tuần tự."

Mở Unit Tests, API Tests và summary/artifacts. Không gọi artifact Allure của run này là còn tải được: chính sách lưu 7 ngày đã qua.

### 2:20–3:20 — npm audit fail-fast trong run mới

"Trong cấu hình hiện tại, `npm audit` tạo báo cáo JSON và bảng tổng kết. Khi có lỗ hổng mức high hoặc critical, Security Vulnerability Scan thất bại, vì vậy Docker build và GHCR push không được kích hoạt. Đây là fail-fast gate thật. Dự án còn nhiều dependency cũ nên run mới có thể đỏ; điều đó thể hiện gate đang chặn phát hành, không có nghĩa là quá trình quét lỗi. Báo cáo JSON vẫn được upload để nhóm xử lý."

Mở run mới nhất ở tab 3, chỉ vào Security Vulnerability Scan, Step Summary và các job Docker bị skipped. Nếu Allure đã xuất bản thành công, chỉ vào artifact `allure-report-dashboard`; báo cáo này được tạo từ 46 test case Jest/SuperTest.

### 3:20–4:10 — CodeQL SAST

"CodeQL chạy bằng workflow riêng cho JavaScript và TypeScript, với các bộ truy vấn `security-extended` và `security-and-quality`. Job xanh chứng minh phân tích hoàn thành. Kết quả bảo mật phải xem trong Code scanning alerts; tại thời điểm rà soát có 15 cảnh báo mở, vì vậy em không kết luận rằng mã nguồn không còn lỗ hổng."

### 4:10–5:25 — Docker và GHCR trên run lịch sử

"Trở lại run thành công ngày 30/10: Docker Image Build chỉ chạy sau các job phụ thuộc, build image từ Dockerfile và thử gọi `GET /api/tags` trong container. Dockerfile chuyển sang user `node` trước khi chạy ứng dụng. Sau smoke test, Docker Image Push đẩy image lên GHCR với tag là commit SHA đầy đủ 40 ký tự. Tag `ef0684e72c2c2f4c35a42b468ce03a35e0ad48f3` trên trang package trùng SHA của run này."

### 5:25–6:00 — Kết luận trung thực

"Video đã chỉ ra đường đi end-to-end của run thành công và cơ chế chặn phát hành của audit gate hiện tại. Các bước tiếp theo của nhóm là nâng cấp dependency để audit gate thông qua, xử lý hoặc phân loại cảnh báo CodeQL, rồi ghi lại một run mới có đầy đủ test, scan, Docker push và artifact. Em cảm ơn thầy cô và các bạn."

## Những câu không nên nói trong bản nháp cũ

- "11 jobs xanh liên hoàn, tuần tự fail-fast": workflow có các nhánh chạy song song, và run lịch sử bỏ qua mã lỗi `npm audit`.
- "CodeQL không ghi nhận cảnh báo": job hoàn thành nhưng còn 15 cảnh báo mở khi kiểm tra ngày 20/11/2026.
- "Các badge 31/15/100% cập nhật theo thời gian thực": đó là các badge tĩnh.
- "Allure của run lịch sử còn tải được": artifact có thời hạn lưu 7 ngày và không còn trong danh sách artifact của run.
