# waky-landing

**Waky** — 다양한 AI 목소리가 원하는 문구로 깨워 주는 알람 앱의 랜딩 사이트.
Zaco Labs 소개 페이지도 같은 저장소에서 서비스한다.

- 배포: GitHub Pages (`main` 브랜치 루트)
- URL: https://zacolabs.github.io/waky-landing/

## 구조

```
/                        → introduce/ 로 리디렉트
/introduce/              → 브라우저 언어에 따라 kr·en·jp 로 리디렉트
/introduce/{kr,en,jp}/   → Waky 제품 랜딩 (히어로·기능·사용법·FAQ)
/about/                  → 브라우저 언어에 따라 kr·en·jp 로 리디렉트
/about/{kr,en,jp}/       → Zaco Labs 회사 소개
/introduce/zacolabs-assets/
    illustration/        → 랜딩 일러스트 SVG (3개 언어 공용, 글자 없음)
    screenshot/          → 스토어 원본 + 랜딩용으로 자른 app-*.webp
    og-image-*.png       → 공유 미리보기 이미지
/store-assets/           → 스토어 등록용 feature graphic
```

자산이 `introduce/zacolabs-assets/` 아래에 있는 것은 과거 경로다.
이미 공유된 OG 이미지 URL이 깨지지 않도록 그대로 두었다.

## 페이지를 고칠 때

`introduce/<언어>/index.html` 은 **생성 결과물이다. 직접 고치지 않는다.**

```
scripts/landing/i18n/<언어>.json   문구 (제목·본문·기능·사용법·FAQ·alt·메타)
scripts/landing/style.css          공통 CSS ({{FONT}} 자리에 언어별 폰트)
scripts/landing/build.py           템플릿 + 빌드
```

문구를 고치면 JSON 을 수정하고 다시 생성한다.

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
