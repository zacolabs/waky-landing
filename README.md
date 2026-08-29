# waky-landing

WAKY 앱 다운로드 리디렉션 페이지. 기기(iOS/Android)를 판별해 각 스토어로 자동 이동시킨다.

- **iOS** (iPhone/iPad/iPod) → App Store
- **Android** → Google Play
- **그 외**(데스크톱 등) → 두 스토어 버튼을 보여주는 폴백 화면

## 배포

GitHub Pages(`main` 브랜치 루트)로 서비스된다.

- URL: https://newhyunsu.github.io/waky-landing/

## 스토어 링크 설정

`index.html` 상단 `<script>`의 상수만 실제 값으로 바꾸면 된다.

```js
var IOS_URL     = "https://apps.apple.com/app/idXXXXXXXXXX";                    // App Store 앱 ID
var ANDROID_URL = "https://play.google.com/store/apps/details?id=com.waky.app"; // 실제 패키지명
var FALLBACK_URL = "";                                                          // 데스크톱 등에서 보낼 곳(비우면 이 페이지 유지)
```
