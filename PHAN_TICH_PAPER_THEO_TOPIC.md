

## 1
## TOP 3 PAPERS / PERSUADE / 26.09.2026
## HỖ TRỢ ĐÁNH GIÁ
## HIỆU QUẢ LẬP LUẬN
Ba nghiên cứu trọng tâm cho dự án
## PERSUADE
Tài liệu chuẩn bị nội dung trình bày midterm
Phiên bản 26/09/2026 • Trích dẫn APA 7 • R01 · R02 · R06
Thông điệp đề xuất: Xây dựng công cụ giúp giáo viên xem xét chất lượng các thành phần lập luận trong
bài viết, ưu tiên những trường hợp cần phản hồi và giữ quyền quyết định cuối cùng ở giáo viên. Không
tuyên bố thay thế việc chấm bài.
Vì sao chọn đúng ba bài này?
Nghiên cứuVai trò trong lập luận của nhómCâu hỏi được hỗ trợ
R01 — Ding et al.
## (2023)
Cơ sở mô hình và baselineĐánh giá một thành phần lập luận nên dùng
những thông tin nào?
R02 — Favero et al.
## (2026)
Khả năng triển khai và giới hạn LLM nhỏMô hình nhỏ có tự tách đoạn, nhận diện vai trò
và đánh giá chất lượng đủ tốt không?
R06 — Baffour et
al. (2023)
Thiên lệch và vai trò con ngườiĐiểm số tổng thể có che giấu sai khác giữa các
nhóm học sinh không?
Đây là ba bài phù hợp nhất với hướng dự án đang chọn trong danh sách mười bài, không phải khẳng định
ba bài tốt nhất toàn bộ lĩnh vực. Cả ba gắn với PERSUADE/Feedback Prize, nhưng phiên bản dữ liệu và thiết lập
thí nghiệm không đồng nhất.
Cách dùng tài liệu
Trang 2: chốt bài toán và phạm vi đầu vào/đầu ra trước khi nói về paper.
Trang 3–8: mỗi paper có một trang phân tích và một trang nội dung rút gọn, lời nói gợi ý, câu hỏi phản
biện.
Trang 9: bảy paper còn lại trong một section giới thiệu ngắn.
Trang 10: ghép related work vào mạch trình bày theo midterm brief.
Trang 11–13: tài liệu tham khảo APA 7, đủ tác giả, năm, nguồn và đường dẫn truy cập.
Lưu ý: Đây là tài liệu đọc, không phải bộ slide nộp. Brief yêu cầu 6–8 slide, trình bày 7 phút và Q&A 3 phút;
không đưa toàn bộ 13 trang này lên màn hình. R01–R10 là mã tra cứu nội bộ, không thay cho trích dẫn tác
giả–năm.

## 2
## TOP 3 PAPERS / PERSUADE / 26.09.2026
01 / Chốt hướng dự án trước khi đọc paper
Vấn đề thực tế và người dùng
Người dùng chính: giáo viên dạy viết tiếng Anh. Khi đọc nhiều bài nghị luận, giáo viên cần xác định thành
phần nào đang thể hiện lập luận chưa hiệu quả để phản hồi có trọng tâm. Dự án đề xuất một bước hỗ trợ rà
soát; lợi ích tiết kiệm thời gian là giả thuyết cần đo, không phải điều ba paper đã chứng minh trong lớp học
của nhóm.
Pipeline khả thi cho phiên bản đầu
- Đầu vào: bài viết tiếng Anh hoàn chỉnh và một hoặc nhiều thành phần lập luận do giáo viên chọn; có thể
bổ sung đề bài và vai trò như Claim/Evidence khi biết chắc. Một thành phần có thể gồm nhiều câu, không
mặc định bằng một đoạn văn xuống dòng.
- Xử lý: lấy văn bản thành phần cùng ngữ cảnh tương ứng → tạo đặc trưng/biểu diễn → mô hình phân loại
ba mức hiệu quả theo nhãn dữ liệu.
- Đầu ra: dự đoán Ineffective / Adequate / Effective, kèm độ tin cậy đã được kiểm tra hoặc trạng thái cần
xem lại. Không diễn giải xác suất thô thành mức chắc chắn tuyệt đối.
- Hành động: giáo viên chấp nhận, sửa hoặc bác bỏ gợi ý; tự viết phản hồi và quyết định đánh giá. Có thể
sắp xếp ưu tiên trong tập thành phần đã được chọn, chưa tự phát hiện mọi vấn đề của toàn bài.
- Đo hữu ích: so sánh thời gian rà soát có/không có công cụ, tính cả thời gian chọn thành phần; đo lỗi bị bỏ
sót, gợi ý bị bác bỏ và đánh giá của giáo viên.
Dữ liệu huấn luyện khác giao diện sử dụng thế nào?
Trong MVP, ranh giới do người chấm gán được dùng để trích thành phần làm input; nhãn hiệu quả mới là
target cần dự đoán. Ranh giới chỉ trở thành target nếu nhóm mở rộng sang nhiệm vụ tự phân đoạn. Khi suy
luận, không đưa nhãn hiệu quả thật vào input. Lựa chọn ban đầu là đánh giá các thành phần đã xác định; tự
tách ranh giới là nhiệm vụ mở rộng riêng. Chọn một đoạn tùy ý không tương ứng đơn vị được gán nhãn sẽ tạo
lệch đầu vào.
Yêu cầu briefQuyết định đề xuất cho nhóm
ML task, input/output, nhãnPhân loại hiệu quả ở cấp thành phần lập luận; một ví dụ
minh họa input → ba xác suất → giáo viên duyệt
Ít nhất hai họ mô hình trong mônTF-IDF + Logistic Regression làm ứng viên baseline; chọn
thêm một họ đã học và xác nhận với syllabus.
Transformer/LLM là mở rộng nếu phù hợp, không tự động
thay yêu cầu hai họ
Split, metric, baselineChia theo essay ID; nếu có student ID thì ưu tiên tách theo
học sinh. Macro-F1, recall Ineffective, confusion matrix;
thêm QWK cho tính thứ bậc
Rủi ro và human-in-the-loopKhông tự cho điểm cuối; kiểm tra theo nhóm đủ mẫu, xử
lý trường hợp không chắc chắn
Chưa được dữ liệu bảo đảm: chẩn đoán đúng “thiếu bằng chứng vì lý do X”, sinh lời khuyên sư phạm đáng
tin, cải thiện kết quả học tập hay áp dụng ngay cho tiếng Việt. Các khả năng đó cần nhãn hoặc đánh giá bổ
sung.

## 3
## TOP 3 PAPERS / PERSUADE / 26.09.2026
02 / R01 — Cơ sở mô hình hóa
## Score It All Together
Tác giả: Yuning Ding, Marie Bexte, Andrea Horbach. Năm: 2023.
Nguồn: Findings of ACL 2023, tr. 13052–13063.
Trang paper và metadata · Toàn văn PDF
Paper đặt vấn đề gì và đã làm gì?
Ding et al. (2023) nghiên cứu đánh giá chất lượng thành phần lập luận trong bài nghị luận, thay vì chỉ chấm
một điểm tổng toàn bài. Dữ liệu thí nghiệm là phần PERSUADE được cung cấp qua Feedback Prize –
Predicting Effective Arguments. Không nên gọi mọi tập con và cách chia trong bài là toàn bộ bản PERSUADE
2.0 mà nhóm sẽ tải.
Study 1: khi đã biết ranh giới đúng của thành phần, dự đoán nhãn chất lượng bằng Logistic Regression với TF-
IDF và BERT. Tác giả khảo sát bổ sung loại thành phần, đề bài và thông tin toàn bài. Study 2: nghiên cứu học
đa nhiệm, kết hợp nhận diện thành phần/loại/chất lượng, so với quy trình tuần tự. Vì vậy paper hữu ích cả cho
MVP dùng ranh giới có sẵn và hướng mở rộng end-to-end.
Kết quả nên đưa lên slide
Study 1, Table 3AccuracyQWK
Logistic Regression baseline0,650,41
Logistic Regression + cả ba thông tin
bổ sung
## 0,670,50
BERT baseline0,670,42
BERT + cả ba thông tin bổ sung0,670,49
Cách đọc: bổ sung thông tin có thể cải thiện mức đồng thuận có trọng số với người chấm, dù accuracy không
tăng tương ứng. QWK là quadratic weighted kappa, không phải “phần trăm dự đoán đúng”. Không quy toàn bộ
chênh lệch cho riêng ngữ cảnh: cấu hình cuối thêm ba loại thông tin đồng thời. Table 3 tổng hợp 10 folds
cho LR và 10 epochs cho BERT; đây không phải cam kết cùng mức tăng khi nhóm đổi split.
Limitation — phải nói rõ
Tác giả nêu: 157 bài quá dài nên phần lập luận phía sau bị cắt trong mô hình transformer; thông tin đề bài
phải suy ra tự động vì không có nhãn gốc; mới kiểm tra trên bài tiếng Anh của học sinh phổ thông. Tác giả còn
cảnh báo rủi ro không khuyến khích cách lập luận sáng tạo nhưng hiệu quả.
Giới hạn khi nhóm vận dụng: kết quả Study 1 dùng ranh giới đúng, không chứng minh một hệ thống tự tách
mọi đoạn đạt cùng chất lượng. Nhãn dự đoán chưa phải lời giải thích nguyên nhân yếu và chưa chứng minh
giáo viên tiết kiệm thời gian.
Điểm kế thừa: bắt đầu bằng baseline nhỏ, so sánh có/không có ngữ cảnh trên cùng split; giữ nhiệm vụ tách
ranh giới ngoài MVP. Nguồn chi tiết: Study 1/Table 3, Study 2 và mục Limitations của paper.

## 4
## TOP 3 PAPERS / PERSUADE / 26.09.2026
03 / R01 — Nội dung trình bày và phản biện
Khối nội dung có thể đặt lên slide
Ding et al. (2023): đánh giá thành phần cần xét thêm thông tin của bài viết.
Nghiên cứu phân loại hiệu quả lập luận trên dữ liệu Feedback Prize/PERSUADE.
Study 1: LR tăng QWK 0,41 → 0,50 khi thêm loại thành phần, đề bài và thông tin toàn bài.
Hạn chế: dùng ranh giới có sẵn; bài dài bị cắt trong transformer; chưa chứng minh khả năng chuyển
sang ngôn ngữ khác.
Nhóm kế thừa: baseline đơn giản và thí nghiệm thêm ngữ cảnh, không bắt đầu bằng pipeline tự động
hoàn toàn.
Trích dẫn chân slide: Ding et al. (2023), Table 3. DOI: 10.18653/v1/2023.findings-acl.825.
Lời nói gợi ý khoảng 45–60 giây
“Bài đầu tiên giúp nhóm xác định cách xây dựng mô hình. Tác giả không chỉ chấm điểm toàn bài mà đánh giá
từng thành phần lập luận. Một kết quả đáng chú ý là Logistic Regression, vốn khá đơn giản, tăng QWK từ 0,41
lên 0,50 khi được bổ sung loại thành phần, đề bài và thông tin toàn bài. Chúng em không hiểu con số này là
tăng accuracy từ 41% lên 50%. Nó phản ánh mức đồng thuận có trọng số với nhãn người chấm. Tuy nhiên, thí
nghiệm này đã biết ranh giới thành phần. Vì vậy nhóm sẽ bắt đầu từ các thành phần được xác định trước và
kiểm tra xem thêm ngữ cảnh có giúp phát hiện trường hợp chưa hiệu quả hay không.”
Những câu dễ bị hỏi
“Paper đã làm rồi, nhóm còn làm gì?”
Nhóm không nhận là phát minh bài toán mới. Đóng góp dự án môn học là triển khai có kiểm chứng một quy
trình hỗ trợ giáo viên: so sánh baseline, kiểm soát rò rỉ dữ liệu, kiểm tra lỗi và thử nghiệm mức hữu ích. Đây là
đóng góp ứng dụng/đánh giá, chưa phải đóng góp phương pháp mới.
“Vậy BERT chắc chắn tốt hơn Logistic Regression?”
Không. Table 3 cho thấy thứ hạng phụ thuộc metric và cấu hình. Nhóm phải dùng cùng split, cùng input và
ngân sách phù hợp để so sánh; không lựa mô hình chỉ vì tên lớn hơn.
“Thêm đề bài có làm lộ nhãn không?”
Đề bài là thông tin có thể biết khi sử dụng nên không mặc nhiên là leakage. Nhưng split phải tránh cùng
bài/cùng học sinh nằm ở hai tập. Nếu muốn tuyên bố tổng quát sang đề mới, cần thêm đánh giá holdout theo
đề; split ngẫu nhiên theo bài chưa trả lời điều này.
“Mô hình có biết vì sao đoạn lập luận yếu không?”
Phân loại ba mức không tự cung cấp nguyên nhân sư phạm đã được kiểm chứng. Giao diện đầu tiên chỉ hỗ trợ
xem xét và ưu tiên; mọi giải thích sinh thêm cần được giáo viên kiểm tra riêng.
Thí nghiệm kế thừa khả thi
Giữ nguyên test set → baseline chỉ văn bản thành phần → thêm ngữ cảnh → so sánh macro-F1, recall
Ineffective và QWK. Nếu dùng loại thành phần, ghi rõ đó là nhãn do người dùng cung cấp hay dự đoán tự
động; hai trường hợp không tương đương. Chưa có kết quả thí nghiệm của nhóm trong tài liệu này.

## 5
## TOP 3 PAPERS / PERSUADE / 26.09.2026
04 / R02 — LLM nhỏ: làm được gì, chưa làm được gì?
Leveraging Small LLMs for Argument Mining in Education
Tác giả: Lucile Favero, Juan Antonio Pérez-Ortiz, Tanja Käser, Nuria Oliver.
Bản trích dẫn: Favero et al. (2026), kỷ yếu CMNA 2025, CEUR-WS Vol. 4166, tr. 11–30. Workshop diễn ra
12/12/2025; kỷ yếu công bố 09/02/2026. Preprint có từ năm 2025.
Trang kỷ yếu chính thức · Toàn văn kỷ yếu · Preprint
Câu hỏi và cách thực hiện
Favero et al. (2026) thử các LLM nhỏ, trọng số mở để phân tích bài viết học sinh với ba nhiệm vụ: tách thành
phần → nhận diện vai trò → đánh giá chất lượng. Paper dùng dữ liệu Feedback Prize – Predicting Effective
Arguments, thuộc họ PERSUADE. Các mô hình gồm Qwen 2.5 7B, Llama 3.1 8B và Gemma 2 9B, với few-shot
prompting hoặc fine-tuning; có đối chiếu các baseline và GPT-4o mini.
Input và thiết lập không chỉ có một dạng: tác giả xét ranh giới thành phần đúng có sẵn (gold segmentation) và
ranh giới do mô hình suy ra (inferred segmentation). Không được lấy kết quả ở điều kiện thứ nhất để quảng
bá hiệu quả end-to-end ở điều kiện thứ hai.
Những điều paper thực sự tìm thấy
Fine-tuning giúp các LLM nhỏ trong tách thành phần và nhận diện loại; đánh giá chất lượng vẫn khó,
không phải nhiệm vụ nào fine-tuning cũng cải thiện.
Kết quả đánh giá chất lượng tốt hơn khi cung cấp ranh giới đúng so với khi dùng ranh giới suy ra (mục
4.4.2). Điều này hỗ trợ việc tách riêng đánh giá phân loại và đánh giá toàn pipeline.
Ví dụ cụ thể — Table 2, joint setup + inferred segmentation: recall của lớp Ineffective chỉ 29,78%, F1 lớp
này 34,84%. Kết quả này cho thấy phải kiểm tra khả năng bỏ sót đúng lớp cần hỗ trợ giáo viên; không chỉ
nhìn một điểm tổng.
Limitation — tác giả và hệ quả ứng dụng
Tác giả nêu: chất lượng dự đoán còn thấp ở tất cả mô hình; một số cấu hình fine-tuned bị lỗi suy luận lặp lại;
chỉ đánh giá trên bài tiếng Anh; cần nghiên cứu trong lớp học để biết hiệu quả thực tế. Chất lượng nhãn là giả
thuyết giải thích kết quả thấp, chưa phải nguyên nhân đã chứng minh.
Khi áp dụng: “nhỏ” không có nghĩa là miễn phí tính toán hoặc chạy tốt trên mọi máy. Paper dùng A100 để
fine-tune và M1 Pro 32 GB cho suy luận cục bộ; nhóm phải đo lại tốc độ, bộ nhớ và tỷ lệ đầu ra lỗi trên thiết bị
của mình.
Điểm kế thừa: dùng LLM nhỏ như hướng mở rộng có đối chứng; ưu tiên đánh giá recall Ineffective, lỗi ranh
giới và đầu ra không hợp lệ. Nguồn: mục 4.4.2–4.4.3, Table 2, Experimental Setup và Limitations.

## 6
## TOP 3 PAPERS / PERSUADE / 26.09.2026
05 / R02 — Nội dung trình bày và phản biện
Khối nội dung có thể đặt lên slide
Favero et al. (2026): LLM nhỏ không đồng nghĩa với đánh giá chất lượng đáng tin.
Thử mô hình 7B–9B cho tách thành phần, nhận diện vai trò và đánh giá hiệu quả.
Fine-tuning hỗ trợ cấu trúc/vai trò, nhưng bài toán chất lượng vẫn khó.
Gemma 2 9B three-shot, joint + inferred segmentation: recall Ineffective 29,78% (Table 2).
Hạn chế: lỗi suy luận ở một số cấu hình; chỉ dữ liệu tiếng Anh; chưa đánh giá hiệu quả trong lớp học.
Nhóm kế thừa: MVP có ranh giới sẵn; LLM chỉ là mở rộng, không tự chấm thay giáo viên.
Trích dẫn chân slide: Favero et al. (2026), Table 2, CMNA 2025 / CEUR-WS 4166. Không ghi “Favero et al.,
2025” nếu đang dẫn bản kỷ yếu này.
Lời nói gợi ý khoảng 45–60 giây
“Bài thứ hai kiểm tra một hướng hấp dẫn là dùng LLM nhỏ để tự phân tích bài viết. Tuy nhiên, kết quả không
có nghĩa chỉ cần dùng LLM là bài toán đã được giải quyết. Tác giả cho thấy tách thành phần và nhận diện vai
trò có thể được cải thiện, trong khi đánh giá chất lượng vẫn khó. Ở cấu hình Gemma 2 9B three-shot có ranh
giới tự suy ra, recall của lớp Ineffective chỉ khoảng 29,78%. Đây là đúng lớp mà công cụ của nhóm cần chú ý
nếu muốn giúp giáo viên tìm trường hợp cần phản hồi. Vì vậy chúng em chọn phạm vi thận trọng: xác định
thành phần trước, kiểm tra lỗi theo từng lớp, rồi mới xem xét LLM và tự động tách đoạn.”
Những câu dễ bị hỏi
“Recall thấp như vậy thì đề tài có còn khả thi?”
Có thể làm nghiên cứu/ứng dụng hỗ trợ, nhưng không thể hứa đạt chất lượng đủ triển khai chỉ dựa trên paper.
MVP hẹp hơn giúp đo riêng năng lực phân loại, tránh cộng thêm lỗi tách ranh giới. Nếu recall hoặc mức hữu
ích không đạt mục tiêu đặt trước, phải giảm phạm vi sử dụng hoặc dừng tính năng ưu tiên tự động.
“Có phải Gemma tốt nhất nên chọn luôn?”
Không. Con số chỉ thuộc model, prompt, dữ liệu và giao thức của paper. Nhóm phải so sánh trong điều kiện
thực tế của mình. Lựa chọn mô hình cần cân đối chất lượng, độ trễ, bộ nhớ và khả năng đáp ứng yêu cầu môn
học.
“Chạy local là hoàn toàn bảo mật?”
Không. Chạy cục bộ có thể giảm việc truyền bài viết ra dịch vụ ngoài, nhưng vẫn phải quản lý quyền truy cập,
file lưu, log và dữ liệu nhận dạng học sinh. Đó là thiết kế vận hành của nhóm, không phải chứng nhận an toàn
do paper cung cấp.
“Tại sao lại ghi năm 2026 trong khi CMNA 2025?”
2025 là năm workshop và preprint; bản kỷ yếu đang sử dụng được CEUR công bố ngày 09/02/2026. APA trích
theo năm của phiên bản được dẫn; ghi cả hai mốc để tránh hiểu nhầm.
Quyết định nhóm nên nêu: chưa cam kết fine-tune LLM trong MVP; trước hết xây dựng hai họ mô hình phù
hợp môn học và một quy trình đánh giá thống nhất.

## 7
## TOP 3 PAPERS / PERSUADE / 26.09.2026
06 / R06 — Khi metric tổng thể chưa đủ
Analyzing Bias in Large Language Model Solutions for Assisted Writing Feedback Tools
Tác giả: Perpetual Baffour, Tor Saxberg, Scott Crossley. Năm: 2023.
Nguồn: BEA 2023, tr. 242–246, Association for Computational Linguistics.
Trang paper và metadata · Toàn văn PDF
Paper đặt vấn đề gì?
Một hệ thống có thể đạt chất lượng tổng thể tốt nhưng hoạt động khác nhau giữa các nhóm học sinh. Baffour
et al. (2023) kiểm tra điều này ở các giải pháp thắng cuộc trong chuỗi Feedback Prize, sử dụng dữ liệu bài viết
của học sinh lớp 6–12 tại Hoa Kỳ thuộc PERSUADE. Đây là nghiên cứu kiểm tra thiên lệch, không phải đề xuất
một bộ phân loại mới.
Họ đã làm được gì?
Tác giả phân tích các giải pháp của hai cuộc thi: nhận diện thành phần diễn ngôn và dự đoán hiệu quả lập luận.
Các phân tích được tách theo đặc điểm người viết như trạng thái học tiếng Anh (ELL), điều kiện kinh tế và
chủng tộc/sắc tộc. Với nhiệm vụ hiệu quả, bài xem xét các giải pháp dẫn đầu Efficiency Track.
Kết luận chính của paper: các giải pháp ở cuộc thi nhận diện thành phần thể hiện ít thiên lệch hơn trong các
phân tích được thực hiện; các giải pháp dự đoán hiệu quả cho thấy thiên lệch ở mức vừa theo các yếu tố được
khảo sát. Kết quả cho thấy không thể xem một metric tổng thể là đủ để xác nhận hệ thống phù hợp cho mọi
nhóm.
Tác giả còn thử gộp nhãn hậu kiểm: Ineffective và Adequate thành Non-Effective, giữ Effective riêng. Một số
chênh lệch trở nên cân bằng hơn nhưng thiên lệch chưa biến mất. Không nên trình bày đây là một mô hình nhị
phân mới đã được huấn luyện và chứng minh giải quyết fairness.
Limitation — phân biệt điều paper nói với suy luận của nhóm
Phạm vi thực nghiệm của bài: chỉ các giải pháp, các cuộc thi và nhóm dữ liệu được khảo sát; không đại diện
cho mọi mô hình viết bài hiện nay. Phát hiện trên PERSUADE/Feedback Prize không tự suy rộng sang học sinh
Việt Nam. Paper không chứng minh một can thiệp giao diện hay quy trình giáo viên đã cải thiện kết quả học
tập.
Giới hạn diễn giải do nhóm rút ra: quan sát chênh lệch giữa nhóm không tự xác định đầy đủ nguyên nhân
nhân quả. Có thể cần phân tích sâu hơn về phân phối dữ liệu, nhãn và sai số mô hình. Vì vậy không khẳng định
“mô hình chắc chắn phân biệt đối xử vì biến X” chỉ từ các bảng chênh lệch.
Không nên nói: bỏ thuộc tính nhân khẩu học khỏi input là đã hết bias; hoặc R06 chứng minh mô hình của
nhóm chắc chắn có/không có bias. Cần kiểm tra trên mô hình và split của chính nhóm.
Điểm kế thừa: báo cáo hiệu năng phân nhóm khi có dữ liệu hợp lệ và đủ mẫu; cho giáo viên sửa/bác bỏ gợi ý;
không dùng dự đoán để tự quyết định điểm cuối. Nguồn: các phân tích Feedback Prize 1.0/2.0, Tables 4–6 và
mục Discussion.

## 8
## TOP 3 PAPERS / PERSUADE / 26.09.2026
07 / R06 — Nội dung trình bày và phản biện
Khối nội dung có thể đặt lên slide
Baffour et al. (2023): đánh giá hiệu quả cần kiểm tra thiên lệch, không chỉ accuracy.
Audit các giải pháp Feedback Prize trên dữ liệu PERSUADE.
Phát hiện thiên lệch rõ hơn ở dự đoán hiệu quả so với nhận diện thành phần trong các giải pháp được
khảo sát.
Gộp nhãn không loại bỏ hoàn toàn chênh lệch.
Hạn chế: kết luận giới hạn ở mô hình/dữ liệu được khảo sát; không xác định đầy đủ nguyên nhân và
không chứng minh hiệu quả lớp học.
Nhóm kế thừa: kiểm tra theo nhóm đủ mẫu, giáo viên duyệt và không tự chấm điểm cuối.
Trích dẫn chân slide: Baffour et al. (2023). DOI: 10.18653/v1/2023.bea-1.21.
Lời nói gợi ý khoảng 45–60 giây
“Bài thứ ba không dùng để chọn kiến trúc mô hình mà để thiết kế cách sử dụng có trách nhiệm. Tác giả kiểm
tra các giải pháp Feedback Prize và nhận thấy nhiệm vụ dự đoán hiệu quả có thể biểu hiện thiên lệch giữa các
nhóm học sinh. Điểm tổng thể tốt vì vậy chưa đủ để khẳng định công cụ phù hợp cho mọi người. Chúng em kế
thừa bài học này bằng cách kiểm tra hiệu năng theo nhóm nếu dữ liệu cho phép, đồng thời giữ quyền sửa và
bác bỏ gợi ý ở giáo viên. Nhóm không dùng paper để khẳng định mô hình của mình chắc chắn công bằng;
fairness phải được đánh giá trên hệ thống thực tế của nhóm.”
Những câu dễ bị hỏi
“Đây là bài bias, tại sao là top 3 liên quan?”
Dự án không chỉ tối ưu một mô hình; đầu ra sẽ tác động tới cách giáo viên ưu tiên phản hồi cho học sinh. R06
nghiên cứu chính dữ liệu và nhiệm vụ liên quan nên giúp xác định rủi ro sử dụng và kế hoạch đánh giá. Đây là
vai trò bổ sung cho R01 và R02, không thay thế bằng chứng thuật toán.
“Dữ liệu nhóm tải không có thuộc tính nhân khẩu học thì sao?”
Không tự suy đoán thuộc tính nhạy cảm từ tên hoặc bài viết. Có thể kiểm tra theo đề bài, độ dài hay các nhóm
quan sát được một cách hợp lệ; nhưng đó không thay thế audit theo ELL/điều kiện kinh tế. Phải ghi rõ chưa
đánh giá được khía cạnh fairness tương ứng.
“Có giáo viên duyệt là đã an toàn?”
Chưa. Giáo viên có thể bị ảnh hưởng bởi gợi ý sai. Vì vậy giao diện nên hiển thị văn bản gốc, cho phép bác bỏ
dễ dàng và không trình bày nhãn như phán quyết chắc chắn. Cần quan sát mức chấp nhận sai trong thử
nghiệm sử dụng, không chỉ đếm số lần bấm duyệt.
“Nhãn người chấm có phải chân lý tuyệt đối?”
Đó là ground truth vận hành để huấn luyện và đánh giá theo rubric, không phải chân lý khách quan cho mọi
phong cách viết. Nếu có nhiều người chấm và độ đồng thuận, cần báo cáo; không suy ra độ tin cậy của nhãn
từ một cột nhãn cuối cùng.
Quyết định nhóm nên nêu: sử dụng để hỗ trợ phản hồi hình thành, không tự xếp hạng năng lực học sinh;
mọi tuyên bố fairness phải đi kèm phạm vi dữ liệu và lượng mẫu.

## 9
## TOP 3 PAPERS / PERSUADE / 26.09.2026
08 / Bảy nghiên cứu bổ trợ — giới thiệu ngắn
Bảy bài dưới đây bổ sung bối cảnh, dữ liệu và các hướng mở rộng. Không mặc định cả bảy đều huấn
luyện/thử nghiệm trên PERSUADE 2.0. Chỉ cần mention ở phần related work hoặc trang tài liệu tham khảo;
không cần trình bày bảy phương pháp riêng. Thông tin APA đầy đủ và link đọc ở trang 11–13.
Mã / trích dẫnBài viết và ý nghĩa đối với đề tài
R03 — Deshpande et al.
## (2024)
Contextualizing Argument Quality Assessment with Relevant Knowledge. Bổ sung góc
nhìn dùng kiến thức liên quan khi đánh giá chất lượng lập luận; phù hợp để mention
khi nói về vai trò của ngữ cảnh. Không xem là bằng chứng mọi loại truy xuất kiến thức
đều giúp MVP.
R04 — Liu et al. (2024)CASA: Causality-driven Argument Sufficiency Assessment. Gắn với việc đánh giá tính đầy
đủ của lập luận. Hữu ích cho hướng mở rộng từ “mức hiệu quả” sang “lập luận đã đủ
sức hỗ trợ kết luận chưa”; hai nhãn này không đồng nghĩa.
R05 — Crossley et al. (2024)A Large-Scale Corpus for Assessing Written Argumentation: PERSUADE 2.0. Nguồn nền
tảng để giới thiệu corpus và cơ sở gán nhãn. Đây là bài về tài nguyên dữ liệu, không
dùng như bằng chứng một model của nhóm đã hoạt động tốt. Toàn văn lưu trong
project là preprint 2023.
R07 — Schaller et al. (2025)Don’t Score too Early! Evaluating Argument Mining Models on Incomplete Essays. Đặt
vấn đề đánh giá bài đang viết dở. Dùng để giải thích vì sao MVP trước mắt yêu cầu bài
hoàn chỉnh; không suy kết quả trên bài hoàn chỉnh sang phản hồi thời gian thực.
R08 — Stahl et al. (2024)A School Student Essay Corpus for Analyzing Interactions of Argumentative Structure and
Quality. Tài nguyên nghiên cứu quan hệ cấu trúc–chất lượng lập luận trên bài viết học
sinh. Có ích khi nhắc khả năng đối chiếu corpus, không coi là cùng dataset PERSUADE.
R09 — Romberg et al.
## (2025)
Towards a Perspectivist Turn in Argument Quality Assessment. Gợi mở cách nhìn chất
lượng lập luận phụ thuộc góc nhìn đánh giá. Hỗ trợ thảo luận bất đồng người chấm;
không biến một nhãn cuối cùng thành chân lý tuyệt đối.
R10 — Wachsmuth et al.
## (2024)
Argument Quality Assessment in the Age of Instruction-Following Large Language
Models. Cung cấp bối cảnh đánh giá chất lượng lập luận trong thời đại LLM làm theo
chỉ dẫn. Dùng để giới thiệu xu hướng, không thay cho kiểm chứng mô hình trên dữ
liệu của nhóm.
Câu nói gộp khoảng 15 giây
“Ngoài ba bài trọng tâm, chúng em tham khảo thêm các nghiên cứu về corpus PERSUADE, kiến thức ngữ cảnh,
tính đầy đủ của lập luận, bài viết chưa hoàn chỉnh và khác biệt góc nhìn của người chấm. Các bài này giúp xác
định phạm vi và hướng mở rộng, chứ không phải tất cả đều thực nghiệm trên cùng dataset.”
Cách mention trên slide: ghi 7 trích dẫn tác giả–năm ở phần bổ trợ hoặc slide reference. Không dùng bảy
logo/tựa bài dài khiến nội dung chính khó đọc.

## 10
## TOP 3 PAPERS / PERSUADE / 26.09.2026
09 / Ghép ba paper thành lập luận của dự án
Bảng related work rút gọn cho một slide
PaperĐã đóng gópGiới hạn cần nhớNhóm kế thừa
Ding et al. (2023)Nghiên cứu thông tin bổ
sung và học đa nhiệm cho
đánh giá lập luận
Ranh giới gold ở Study 1;
cắt bài dài; dữ liệu tiếng
## Anh
Baseline + kiểm tra tác
dụng ngữ cảnh
Favero et al. (2026)Kiểm tra LLM nhỏ cho ba
bước argument mining
Chất lượng còn thấp; lỗi
suy luận; chưa kiểm tra
trong lớp học
Thu hẹp MVP; đo recall lớp
cần hỗ trợ; LLM là tùy chọn
Baffour et al. (2023)Audit thiên lệch các giải
pháp Feedback Prize
Phạm vi mô hình/dữ liệu cụ
thể; chưa tách đầy đủ
nguyên nhân
Audit phù hợp dữ liệu; giáo
viên quyết định cuối
Khoảng trống nhóm chọn kiểm chứng: Một pipeline phạm vi hẹp, có baseline, có kiểm tra lỗi và có đo
lợi ích cho giáo viên. Đây là khoảng trống triển khai/đánh giá của dự án nhóm, không tuyên bố văn liệu
chưa từng nghiên cứu vấn đề này.
Gợi ý phân bổ 8 slide theo midterm brief
SlideNội dung chínhThời lượng
1Vấn đề, người dùng và tình huống giáo viên cần hỗ trợ45 giây
2Dataset: nguồn, khả năng truy cập, đơn vị dữ liệu, nhãn, quy mô bản dùng, license50 giây
3Pipeline input → model → output → hành động của giáo viên55 giây
4Related work: bảng ba bài trên; bảy bài bổ trợ mention ngắn75 giây
5Kế hoạch mô hình: ít nhất hai họ trong môn, baseline và ablation55 giây
6Split, metric, test set; thử nghiệm hữu ích với giáo viên60 giây
7Rủi ro, limitation của dự án, quyền sửa/bác bỏ của giáo viên45 giây
8Tóm tắt quyết định và references rút gọn20 giây
Tổng 6 phút 45 giây, còn 15 giây dự phòng. Ba đoạn lời nói 45–60 giây ở trang 4/6/8 là tài liệu luyện tập hoặc
Q&A; không đọc nguyên cả ba trong slide related work 75 giây.
Kết luận nên nói với nhóm
“Related work cho thấy bài toán có nền tảng nghiên cứu và dữ liệu liên quan, nhưng chất lượng dự đoán, thiên
lệch và lợi ích lớp học vẫn cần kiểm chứng. Vì vậy nhóm đề xuất công cụ hỗ trợ rà soát, không tự chấm điểm:
làm baseline trước, đánh giá đúng nhiệm vụ, rồi mới mở rộng tự tách đoạn hoặc dùng LLM.”

## 11
## TOP 3 PAPERS / PERSUADE / 26.09.2026
10 / Tài liệu tham khảo APA 7 — A–D
Danh mục sắp theo họ tác giả đầu tiên. Mã R chỉ giúp đối chiếu với thư mục paper; khi viết nội dung dùng tác giả–năm,
ví dụ (Ding et al., 2023). Giữ nguyên tên tiếng Anh của paper và nguồn xuất bản. DOI và đường dẫn toàn văn có thể bấm
trong PDF.
R06 · Baffour et al. (2023)
Baffour, P., Saxberg, T., & Crossley, S. (2023). Analyzing bias in large language model solutions for assisted writing
feedback tools: Lessons from the Feedback Prize competition series. In E. Kochmar, J. Burstein, A. Horbach, R.
Laarmann-Quante, N. Madnani, A. Tack, V. Yaneva, Z. Yuan, & T. Zesch (Eds.), Proceedings of the 18th Workshop on
Innovative Use of NLP for Building Educational Applications (BEA 2023) (pp. 242–246). Association for Computational
Linguistics. https://doi.org/10.18653/v1/2023.bea-1.21
Toàn văn: https://aclanthology.org/2023.bea-1.21.pdf
Bản đã lưu: R06_2023_Feedback_Prize_Bias.pdf.
R05 · Crossley et al. (2024)
Crossley, S. A., Tian, Y., Baffour, P., Franklin, A., Benner, M., & Boser, U. (2024). A large-scale corpus for assessing written
argumentation: PERSUADE 2.0. Assessing Writing, 61, Article 100865. https://doi.org/10.1016/j.asw.2024.100865
Truy cập toàn văn preprint: https://zenodo.org/records/8221504
Bản đã lưu: R05_PERSUADE_2_0_Preprint.pdf.
Lưu ý phiên bản: reference trên dùng metadata của bài tạp chí 2024. Bản toàn văn đang lưu là preprint 2023, không
phải bản xuất bản cuối. Trang đầu preprint ghi thứ tự Crossley, Baffour, Tian, Franklin, Benner, Boser; bản tạp chí ghi
Crossley, Tian, Baffour, Franklin, Benner, Boser. Không ghép năm của bản này với thứ tự tác giả của bản kia. Nếu dẫn
trực tiếp một chi tiết chỉ được kiểm tra trong preprint, phải chỉ rõ đang dẫn preprint. Phần giới thiệu ngắn ở tài liệu này
không dùng số liệu chi tiết để khẳng định hai bản giống hoàn toàn.
R03 · Deshpande et al. (2024)
Deshpande, D., Sourati, Z., Ilievski, F., & Morstatter, F. (2024). Contextualizing argument quality assessment with relevant
knowledge. In K. Duh, H. Gomez, & S. Bethard (Eds.), Proceedings of the 2024 Conference of the North American
Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 2: Short Papers) (pp.
316–326). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.naacl-short.28
Toàn văn: https://aclanthology.org/2024.naacl-short.28.pdf
Bản đã lưu: R03_2024_SPARK_Argument_Quality.pdf.

## 12
## TOP 3 PAPERS / PERSUADE / 26.09.2026
11 / Tài liệu tham khảo APA 7 — D–L
R01 · Ding et al. (2023)
Ding, Y., Bexte, M., & Horbach, A. (2023). Score it all together: A multi-task learning study on automatic scoring of
argumentative essays. In A. Rogers, J. Boyd-Graber, & N. Okazaki (Eds.), Findings of the Association for Computational
Linguistics: ACL 2023 (pp. 13052–13063). Association for Computational Linguistics.
https://doi.org/10.18653/v1/2023.findings-acl.825
Toàn văn: https://aclanthology.org/2023.findings-acl.825.pdf
Bản đã lưu: R01_2023_Score_It_All_Together.pdf.
R02 · Favero et al. (2026)
Favero, L., Pérez-Ortiz, J. A., Käser, T., & Oliver, N. (2026). Leveraging small LLMs for argument mining in education:
Argument component identification, classification, and assessment. In G. D’Agostino, F. Grasso, N. L. Green, R. J.
Scheffers, J. Schneider, & S. Wells (Eds.), Proceedings of the 25th Workshop on Computational Models of Natural
Argument (CEUR Workshop Proceedings, Vol. 4166, pp. 11–30). CEUR-WS.org. https://ceur-ws.org/Vol-
## 4166/paper2.pdf
Metadata và ngày xuất bản: https://ceur-ws.org/Vol-4166/
Bản preprint 2025, phiên bản khác: https://arxiv.org/abs/2502.14389
Bản đã lưu: R02_CMNA25_Small_LLMs_Argument_Mining.pdf.
Lưu ý phiên bản: tên workshop chứa “2025” nhưng tập kỷ yếu xuất bản 09/02/2026. Số trang 11–30 theo mục lục kỷ
yếu, không phải số trang nội bộ bắt đầu từ 1 trong file PDF. Tên đầy đủ tác giả Käser được lấy theo trang đầu paper:
Tanja Käser; mục lục CEUR ghi “Tania”, nhưng dạng APA “Käser, T.” không bị ảnh hưởng.
R04 · Liu et al. (2024)
Liu, X., Feng, Y., & Chang, K.-W. (2024). CASA: Causality-driven argument sufficiency assessment. In K. Duh, H. Gomez, &
S. Bethard (Eds.), Proceedings of the 2024 Conference of the North American Chapter of the Association for
Computational Linguistics: Human Language Technologies (Volume 1: Long Papers) (pp. 5282–5302). Association for
Computational Linguistics. https://doi.org/10.18653/v1/2024.naacl-long.296
Toàn văn: https://aclanthology.org/2024.naacl-long.296.pdf
Bản đã lưu: R04_2024_CASA_Argument_Sufficiency.pdf.
Quy tắc trích dẫn ngắn khi đưa vào slide
Trong câu: “Ding et al. (2023) cho thấy...”; cuối ý: “...cần kiểm chứng riêng (Favero et al., 2026).” Các bài đều có từ ba tác
giả nên dùng et al. ở citation trong nội dung; danh mục reference vẫn ghi đầy đủ tác giả. Nếu chuyển số liệu thành
biểu đồ, ghi thêm Table/Section và thiết lập gốc; không ghi nguồn chung chung là “ACL” hoặc “Kaggle”.

## 13
## TOP 3 PAPERS / PERSUADE / 26.09.2026
12 / Tài liệu tham khảo APA 7 — R–W
R09 · Romberg et al. (2025)
Romberg, J., Maurer, M., Wachsmuth, H., & Lapesa, G. (2025). Towards a perspectivist turn in argument quality
assessment. In L. Chiruzzo, A. Ritter, & L. Wang (Eds.), Proceedings of the 2025 Conference of the Nations of the
Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long
Papers) (pp. 7458–7485). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.naacl-long.382
Toàn văn: https://aclanthology.org/2025.naacl-long.382.pdf
Bản đã lưu: R09_2025_Perspectivist_Argument_Quality.pdf.
R07 · Schaller et al. (2025)
Schaller, N.-J., Ding, Y., Jansen, T., & Horbach, A. (2025). Don’t score too early! Evaluating argument mining models on
incomplete essays. In E. Kochmar, B. Alhafni, M. Bexte, J. Burstein, A. Horbach, R. Laarmann-Quante, A. Tack, V.
Yaneva, & Z. Yuan (Eds.), Proceedings of the 20th Workshop on Innovative Use of NLP for Building Educational
Applications (BEA 2025) (pp. 345–355). Association for Computational Linguistics.
https://doi.org/10.18653/v1/2025.bea-1.27
Toàn văn: https://aclanthology.org/2025.bea-1.27.pdf
Bản đã lưu: R07_2025_Dont_Score_Too_Early.pdf.
R08 · Stahl et al. (2024)
Stahl, M., Michel, N., Kilsbach, S., Schmidtke, J., Rezat, S., & Wachsmuth, H. (2024). A school student essay corpus for
analyzing interactions of argumentative structure and quality. In K. Duh, H. Gomez, & S. Bethard (Eds.), Proceedings
of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human
Language Technologies (Volume 1: Long Papers) (pp. 2661–2674). Association for Computational Linguistics.
https://doi.org/10.18653/v1/2024.naacl-long.145
Toàn văn: https://aclanthology.org/2024.naacl-long.145.pdf
Bản đã lưu: R08_2024_School_Student_Essay_Corpus.pdf.
R10 · Wachsmuth et al. (2024)
Wachsmuth, H., Lapesa, G., Cabrio, E., Lauscher, A., Park, J., Vecchi, E. M., Villata, S., & Ziegenbein, T. (2024). Argument
quality assessment in the age of instruction-following large language models. In N. Calzolari, M.-Y. Kan, V. Hoste, A.
Lenci, S. Sakti, & N. Xue (Eds.), Proceedings of the 2024 Joint International Conference on Computational Linguistics,
Language Resources and Evaluation (LREC-COLING 2024) (pp. 1519–1538). ELRA and ICCL.
https://aclanthology.org/2024.lrec-main.135/
Toàn văn: https://aclanthology.org/2024.lrec-main.135.pdf
Bản đã lưu: R10_2024_Argument_Quality_Age_of_LLMs.pdf.
Các file paper được lưu trong DOCUMENT_DATASET/RESEARCH_PAPERS. Metadata được đối chiếu với ACL Anthology,
CEUR-WS và Crossref; ngày kiểm tra: 26/09/2026. R05 phân biệt rõ bản tạp chí và preprint truy cập được.