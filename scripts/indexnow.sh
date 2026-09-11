#!/usr/bin/env bash
# IndexNow 핑 — 변경된 페이지를 Bing에 즉시 재크롤 요청한다.
#
#   ./scripts/indexnow.sh                 사이트맵의 모든 URL 제출
#   ./scripts/indexnow.sh <url> [url...]  지정한 URL만 제출
#   DRY_RUN=1 ./scripts/indexnow.sh       전송하지 않고 payload만 출력
#
# 키 파일이 사이트 루트가 아니라 /waky-landing/ 하위에 있으므로 keyLocation 을
# 명시한다. 이 경우 해당 디렉터리 하위 URL만 제출할 수 있다.
# 배열/mapfile 을 쓰지 않는 이유: macOS 기본 bash 3.2 호환.
set -eu

HOST="zacolabs.github.io"
BASE="https://${HOST}/waky-landing"
KEY="ae703324639d4cf68799e9db16dce1c0"
KEY_LOCATION="${BASE}/${KEY}.txt"
ENDPOINT="https://api.indexnow.org/indexnow"

if [ "$#" -gt 0 ]; then
  urls=$(printf '%s\n' "$@")
else
  urls=$(curl -fsS --max-time 15 "${BASE}/sitemap.xml" \
    | sed -n 's:.*<loc>\([^<]*\)</loc>.*:\1:p')
fi

count=$(printf '%s\n' "${urls}" | grep -c . || true)
if [ "${count}" -eq 0 ]; then
  echo "제출할 URL이 없습니다." >&2
  exit 1
fi

# 범위 밖 URL은 422를 부르므로 미리 거른다.
outside=$(printf '%s\n' "${urls}" | grep -v "^${BASE}/" || true)
if [ -n "${outside}" ]; then
  echo "keyLocation 범위 밖 URL이 있습니다:" >&2
  printf '%s\n' "${outside}" >&2
  exit 1
fi

list=$(printf '%s\n' "${urls}" | grep . | sed 's:.*:"&",:' | tr -d '\n')
payload=$(printf '{"host":"%s","key":"%s","keyLocation":"%s","urlList":[%s]}' \
  "${HOST}" "${KEY}" "${KEY_LOCATION}" "${list%,}")

if [ -n "${DRY_RUN:-}" ]; then
  printf '%s\n' "${payload}"
  exit 0
fi

# 키 파일이 라이브가 아니면 IndexNow가 요청 전체를 거부한다.
if [ "$(curl -fsS --max-time 10 "${KEY_LOCATION}" 2>/dev/null || true)" != "${KEY}" ]; then
  echo "키 파일이 라이브가 아닙니다: ${KEY_LOCATION}" >&2
  echo "먼저 push 하고 GitHub Pages 배포가 끝난 뒤 다시 실행하세요." >&2
  exit 1
fi

printf '%s개 URL 제출 중...\n' "${count}"
code=$(curl -s -o /tmp/indexnow.out -w '%{http_code}' --max-time 20 \
  -X POST "${ENDPOINT}" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d "${payload}")

case "${code}" in
  200|202) echo "성공 (HTTP ${code}) — 색인 요청이 접수되었습니다." ;;
  400) echo "실패 (400) 잘못된 형식" >&2; cat /tmp/indexnow.out >&2; exit 1 ;;
  403) echo "실패 (403) 키가 유효하지 않음 — 키 파일 내용을 확인하세요." >&2; exit 1 ;;
  422) echo "실패 (422) URL이 host/keyLocation 범위를 벗어났습니다." >&2; exit 1 ;;
  429) echo "실패 (429) 요청이 너무 잦습니다." >&2; exit 1 ;;
  *) echo "실패 (HTTP ${code})" >&2; cat /tmp/indexnow.out >&2; exit 1 ;;
esac
