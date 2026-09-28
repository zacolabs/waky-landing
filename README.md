# waky-landing

**Waky** — 미션을 풀어야 꺼지는 알람, 직접 녹음한 알람음, 아침 습관을 담은 알람 앱의 랜딩 사이트.
Zaco Labs 회사 소개는 도메인 맨 앞(https://zacolabs.github.io/, `zacolabs/zacolabs.github.io` 저장소)으로 옮겼다.

- 배포: GitHub Pages (`main` 브랜치 루트)
- URL: https://zacolabs.github.io/waky-landing/

## 구조

```
/                        → introduce/<언어>/ 로 바로 리디렉트
/introduce/              → 기기 언어에 맞는 랜딩으로 리디렉트 (아래 참고)
/introduce/<언어>/       → Waky 제품 랜딩 18개 언어 (히어로·기능·사용법·FAQ)
/about/, /about/{kr,en,jp}/ → https://zacolabs.github.io/ 로 넘긴다 (옛 회사 소개 주소)
/introduce/zacolabs-assets/
    illustration/        → 랜딩 일러스트 SVG (3개 언어 공용, 글자 없음)
    screenshot/          → 스토어 원본 + 랜딩용으로 자른 app-*.webp
    og-image-*.png       → 공유 미리보기 이미지
/store-assets/           → 스토어 등록용 feature graphic
```

자산이 `introduce/zacolabs-assets/` 아래에 있는 것은 과거 경로다.
이미 공유된 OG 이미지 URL이 깨지지 않도록 그대로 두었다.

## 언어

`kr` `en` `jp` `zh-hans` `zh-hant` `es` `fr` `de` `it` `pt` `nl` `da` `pl` `ru` `ar` `id` `vi` `fil`

- `kr`·`jp` 는 표준 코드(ko·ja)가 아니지만 이미 색인된 URL 이라 유지한다
- 포르투갈어(`pt`)는 브라질 표현 기준, 아랍어(`ar`)는 RTL
- 히어로 그림은 한국어·일본어만 전용, 나머지는 영어 그림(`wake-en.webp`)과 영어 스크린샷을 쓴다
- 사용법 3컷은 글자가 없어 모든 언어 공용

### 앱에서 링크할 때

진입 주소(`/`, `/introduce/`)는 아래 순서로 언어를 고른다. 언어별 페이지는 강제로 이동시키지 않는다.

1. `?lang=` 값 — 폴더 코드(`de`)와 로케일 태그(`pt-BR`, `zh-TW`, `in-ID`) 모두 받는다
2. 사용자가 언어 선택기에서 직접 고른 언어 (localStorage `waky-lang`)
3. 기기 선호 언어 목록 `navigator.languages` 를 앞에서부터
4. 전부 해당 없으면 `en`

앱 언어를 그대로 넘기면 기기 설정과 달라도 앱과 같은 언어로 열린다.

```
https://zacolabs.github.io/waky-landing/?lang=<앱 로케일>
```

중국어는 `zh-TW`·`zh-HK`·`zh-MO`·`Hant` 가 번체, 나머지가 간체. 구형 안드로이드의 `in`(인도네시아어)과 `tl`(필리핀어)도 인식한다.

### 언어 추가

`scripts/landing/i18n/<코드>.json` 을 만들고 `build.py` 의 `ORDER` 에 코드를 넣은 뒤 빌드한다.
hreflang·언어 선택기·사이트맵·리디렉트가 모두 `ORDER` 를 따라 갱신된다.

## 페이지를 고칠 때

`introduce/<언어>/index.html` 은 **생성 결과물이다. 직접 고치지 않는다.**

```
scripts/landing/i18n/<언어>.json   문구 (제목·본문·기능·사용법·FAQ·alt·메타)
scripts/landing/style.css          공통 CSS ({{FONT}} 자리에 언어별 폰트)
scripts/landing/build.py           템플릿 + 빌드
```

문구를 고치면 JSON 을 수정하고 다시 생성한다. `sitemap.xml`, `index.html`, `introduce/index.html` 도 같이 생성된다.

```
python3 scripts/landing/build.py
```

FAQ·사용법 문구는 페이지 본문과 `FAQPage`·`HowTo` JSON-LD 에 함께 들어가므로
JSON 한 곳만 고치면 둘 다 반영된다.

## 스토어 링크

각 랜딩 페이지 안에 직접 들어 있다.

```
Google Play  https://play.google.com/store/apps/details?id=com.waky.android
App Store    https://apps.apple.com/app/id6797402938
```

## 검색엔진 등록 시 주의

`robots.txt` 는 저장소 루트에 있지만, GitHub Pages 프로젝트 사이트라
실제 주소가 `/waky-landing/robots.txt` 가 된다. 크롤러는 도메인 루트
(`zacolabs.github.io/robots.txt`) 만 읽으므로 이 파일은 참고용이다.
**사이트맵은 Search Console 에 직접 제출해야 한다.**

```
https://zacolabs.github.io/waky-landing/sitemap.xml
```
