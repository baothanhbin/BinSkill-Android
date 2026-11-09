![BinGen-Skill Banner](assets/readme-banner.png)

# BinGen-Skill

`BinGen-Skill` là bộ sưu tập Codex skill dành cho việc tạo mới và refactor project Android an toàn.

Repository hiện có bốn skill Android:

- `skill-gen-app-compose-multi-module`: tạo project Compose đa module gồm `app`, `core/*`, `feature/*`, `resources` và `build-logic`.
- `skill-gen-app-compose-single-module`: tạo project chỉ có một module `:app`, đồng thời phân tách `app`, `core/*` và `feature/*` bằng package folder.
- `android-suffix-renamer`: thêm suffix do người dùng chỉ định vào tên Kotlin, Java, Room và Android resource không phải string thuộc project mà không làm thay đổi hành vi.
- `android-semantic-renamer`: đặt lại identifier thuộc project bằng tên tương đương theo ngữ cảnh, không dùng suffix và không thay đổi code flow, runtime behavior hoặc UI.

## Cấu trúc repository

```text
skills/
  skill-gen-app-compose-multi-module/
    SKILL.md
    agents/
    references/
    scripts/
  skill-gen-app-compose-single-module/
    SKILL.md
    agents/
    assets/
    references/
    scripts/
  android-suffix-renamer/
    SKILL.md
    agents/
    references/
  android-semantic-renamer/
    SKILL.md
    agents/
    references/
assets/
  readme-banner.png
```

## Nên sử dụng skill nào?

Sử dụng `skill-gen-app-compose-multi-module` khi bạn cần:

- một project nền dành cho ứng dụng lớn;
- ranh giới Gradle module rõ ràng;
- cấu trúc `app / core / feature / resources / build-logic`;
- kiến trúc module gần với project production.

Sử dụng `skill-gen-app-compose-single-module` khi bạn cần:

- một project đơn giản và dễ bắt đầu;
- chỉ có một Android module là `:app`;
- phân tách theo package bên trong `app/src/main/java`;
- cấu trúc dễ tiếp cận cho ứng dụng nhỏ hoặc vừa.

Sử dụng `android-suffix-renamer` khi bạn cần:

- thêm suffix vào các thành phần thuộc một project Android có sẵn;
- đổi đồng bộ file Kotlin/Java, class, function, variable, Room, layout, XML ID và resource;
- giữ nguyên package, luồng xử lý, Android callback, database schema, serialization, API, JNI và reflection contract;
- giữ nguyên toàn bộ string resource, bao gồm key, `R.string.*`, `@string/...`, giá trị và bản dịch;
- kiểm tra build và diff trước khi hoàn tất.

Sử dụng `android-semantic-renamer` khi bạn cần:

- đặt lại class, function, variable, Room declaration và resource bằng tên mới có ý nghĩa tương đương;
- áp dụng một semantic family nhất quán, ví dụ `Movie` thành `Film`, thay vì nối suffix;
- giữ nguyên tuyệt đối code flow, data flow, runtime behavior, UI appearance và UI interaction;
- giữ nguyên package/application identity, contract, persisted data và toàn bộ string resource;
- bỏ qua mọi identifier không thể đổi tên an toàn thay vì chỉnh logic hoặc UI để bù.

## Cài đặt

Cài tất cả skill trong repository:

```powershell
npx skills add https://github.com/baothanhbin/BinGen-Skill
```

Chỉ cài skill Compose đa module:

```powershell
npx skills add https://github.com/baothanhbin/BinGen-Skill --skill "skill-gen-app-compose-multi-module"
```

Chỉ cài skill Compose một module:

```powershell
npx skills add https://github.com/baothanhbin/BinGen-Skill --skill "skill-gen-app-compose-single-module"
```

Chỉ cài skill thêm suffix:

```powershell
npx skills add https://github.com/baothanhbin/BinGen-Skill --skill "android-suffix-renamer"
```

Chỉ cài skill semantic rename:

```powershell
npx skills add https://github.com/baothanhbin/BinGen-Skill --skill "android-semantic-renamer"
```

Sau khi cài đặt, hãy khởi động lại Codex để danh sách skill được tải lại.

## Cài đặt thủ công

Sao chép folder skill muốn sử dụng vào thư mục skill cục bộ của Codex.

Các thư mục đích tương ứng:

```text
%USERPROFILE%\.codex\skills\skill-gen-app-compose-multi-module
%USERPROFILE%\.codex\skills\skill-gen-app-compose-single-module
%USERPROFILE%\.codex\skills\android-suffix-renamer
%USERPROFILE%\.codex\skills\android-semantic-renamer
```

Folder nguồn trong repository:

```text
skills/skill-gen-app-compose-multi-module
skills/skill-gen-app-compose-single-module
skills/android-suffix-renamer
skills/android-semantic-renamer
```

## Cách sử dụng

### Tạo project Compose đa module

Lệnh gọi cơ bản:

```text
Sử dụng $skill-gen-app-compose-multi-module để tạo một project Android mới theo kiến trúc Compose đa module.
```

Prompt gợi ý:

```text
Sử dụng $skill-gen-app-compose-multi-module để tạo một project Android mới.

Project:
- Tên ứng dụng: PlantCareAI
- Package: com.baothanhbin.plantcareai
- Slug: plantcareai

Các feature:
- home
- login
- diagnosis
- reminders
- profile

Các màn hình:
- Splash
- Login
- Home
- DiagnosisHistory
- DiagnosisDetail
- ReminderList
- ReminderDetail
- Profile

Data layer:
- Ktor cho remote API
- Room cho dữ liệu local
- Proto DataStore cho auth/session

Background work:
- Bật WorkManager
- SyncPlantsWorker
- SyncRemindersWorker

Tạo project trong thư mục làm việc hiện tại.
```

### Tạo project Compose một module

Lệnh gọi cơ bản:

```text
Sử dụng $skill-gen-app-compose-single-module để tạo một project Android mới theo kiến trúc Compose một module.
```

Prompt gợi ý:

```text
Sử dụng $skill-gen-app-compose-single-module để tạo một project Android mới.

Project:
- Tên ứng dụng: ListeningStarter
- Package: com.example.listeningstarter

Các feature:
- home
- library
- settings

Yêu cầu:
- Giao diện Compose-first
- Cấu hình Hilt
- Bật Room
- Bật Proto DataStore
- Có navigation và app shell cơ bản

Tạo project trong thư mục làm việc hiện tại.
```

Khi dùng một trong hai skill tạo project, prompt tối thiểu nên có:

- tên project;
- package name;
- danh sách feature ban đầu;
- lựa chọn `single-module` hoặc `multi-module`;
- có sử dụng Hilt, Room, DataStore, Ktor và WorkManager hay không.

### Thêm suffix vào project Android có sẵn

Lệnh gọi cơ bản:

```text
Sử dụng $android-suffix-renamer cho project D:\Data\Android\Haiyan\ASD113-ShortDrama21 với suffix Binbao.
```

Prompt đầy đủ được khuyến nghị:

```text
Sử dụng $android-suffix-renamer cho project:
D:\Data\Android\Haiyan\ASD113-ShortDrama21

Suffix cần thêm: Binbao

Hãy đổi tên đồng bộ các file Kotlin/Java, class, interface, function,
variable, Room Entity/DAO/Database/Repository, layout, XML ID và Android
resource thuộc project.

Giữ nguyên toàn bộ string resource: không đổi key `<string>`/`<string-array>`,
`R.string.*`, `@string/...`, nội dung, bản dịch hoặc tên file `strings*.xml`.

Không thay đổi luồng xử lý, package, namespace, applicationId, Android hoặc
library callback, Room table/column/schema, SQL contract, JSON key, API path,
SharedPreferences/DataStore key, JNI, reflection và các contract bên ngoài.

Hãy build project trước và sau khi refactor, kiểm tra các source set liên quan,
Room schema, View Binding/Data Binding, resource reference và git diff trước
khi báo hoàn tất.
```

Ví dụ kết quả với suffix `Binbao`:

```text
MovieDao.kt                  -> MovieDaoBinbao.kt
MovieDao                     -> MovieDaoBinbao
loadMovies()                 -> loadMoviesBinbao()
movieDao                     -> movieDaoBinbao
MAX_COUNT                    -> MAX_COUNT_BINBAO
activity_main.xml            -> activity_main_binbao.xml
R.id.btn_cancel              -> R.id.btn_cancel_binbao
ActivityMainBinding          -> ActivityMainBinbaoBinding
```

### Đặt lại tên theo ngữ nghĩa

Lệnh gọi cơ bản:

```text
Sử dụng $android-semantic-renamer cho project D:\path\to\android-project. Hãy đặt lại các identifier thuộc project bằng tên tương đương theo ngữ cảnh, không thay đổi bất kỳ code flow hoặc UI nào.
```

Ví dụ semantic family:

```text
MovieRepository       -> FilmRepository
MovieDao              -> FilmDao
MovieDetailScreen     -> FilmDetailScreen
movieItems            -> filmEntries
displayMovie          -> showFilm
screen_movie_detail   -> screen_film_detail
```

Skill chỉ được đổi declaration/file/resource name và reference bắt buộc. Nếu một rename có thể làm thay đổi logic, runtime, database, contract hoặc UI, identifier đó phải được giữ nguyên và báo cáo.

## Thành phần của mỗi skill

Tùy theo chức năng, một folder skill có thể gồm:

- `SKILL.md`: hành vi, quy trình, quy tắc thực thi và kết quả mong đợi;
- `references/`: kiến trúc, quy tắc rename, code pattern hoặc checklist kiểm tra;
- `scripts/scaffold_project.py`: script tạo project của hai skill Compose;
- `assets/`: tài nguyên mẫu được skill sử dụng;
- `agents/openai.yaml`: metadata và prompt mặc định của skill.

## Lưu ý

- Skill đa module có nhiều quy ước hơn và hướng đến cấu trúc production.
- Skill một module đơn giản hơn nhưng vẫn giữ ranh giới giữa feature và layer.
- Hai skill Compose tạo file project thực tế, không chỉ sinh nội dung hướng dẫn.
- Skill thêm suffix thực hiện semantic rename, kiểm tra build/diff và giữ nguyên các contract bên ngoài hoặc dữ liệu đã lưu.
- Skill thêm suffix không rename string resource; ví dụ `R.string.title_home` luôn được giữ nguyên.
- Skill semantic rename không nối suffix và không được thay đổi code flow, runtime behavior hoặc bất kỳ đặc điểm UI nào.

## Tài liệu skill

- [Skill Compose đa module](skills/skill-gen-app-compose-multi-module/SKILL.md)
- [Skill Compose một module](skills/skill-gen-app-compose-single-module/SKILL.md)
- [Skill thêm suffix Android](skills/android-suffix-renamer/SKILL.md)
- [Skill semantic rename Android](skills/android-semantic-renamer/SKILL.md)
