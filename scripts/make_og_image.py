"""공유 미리보기(og:image, 1200x630)를 언어별 스토어 스크린샷에서 조합한다.

waky-android `tools/make_feature_graphic.py`(Play 피처 그래픽 1024x500)와 같은 구성을 1200x630 에 맞춘 것.

새로 그리지 않고 waky-ios `screenshots/<lang>/` 의 01(인트로)·03(알람) 원본에서
헤드라인·폰 화면·해 캐릭터·구름을 잘라 붙인다. 글꼴과 번역이 스크린샷과 그대로 맞는다.

    python3 scripts/make_og_image.py ../waky-ios/screenshots introduce/zacolabs-assets de=de pt-BR=pt ...

인자는 <스크린샷 폴더>=<og 그림 코드>. kr·en·jp 그림은 예전에 만든 것을 그대로 둔다.

원본 스크린샷(1290x2796)의 배치가 바뀌면 아래 좌표도 같이 고쳐야 한다.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 630
K = W / 1024           # 피처 그래픽 배치를 이 배율로 키운다
DY = int((H - 500 * K) / 2)  # 남는 세로는 위아래로 나눈다
BG = (253, 252, 247)  # 스크린샷 배경 크림색


def soft_ellipse(size, blur):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).ellipse([blur * 2, blur * 2, size[0] - 1 - blur * 2, size[1] - 1 - blur * 2], fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur))


def soft_corner(size, corner):
    w, h = size
    cx = {'tl': 0, 'bl': 0, 'br': w}[corner]
    cy = {'tl': 0, 'bl': h, 'br': h}[corner]
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).ellipse([cx - w * 0.95, cy - h * 0.95, cx + w * 0.95, cy + h * 0.95], fill=255)
    return m.filter(ImageFilter.GaussianBlur(12))


def headline_box(alarms):
    """03 스크린샷 위쪽(폰 위)에서 글자·광선이 있는 영역. 언어마다 길이가 달라 매번 잰다."""
    top, bottom = 120, 745
    arr = np.asarray(alarms.crop((40, top, 1250, bottom))).astype(int)
    ink = np.abs(arr - np.array(BG)).max(axis=2) > 60
    ys = np.where(ink.any(axis=1))[0]
    xs = np.where(ink.any(axis=0))[0]
    return (max(0, xs[0] + 40 - 14), max(0, ys[0] + top - 14),
            min(1290, xs[-1] + 40 + 14), min(bottom, ys[-1] + top + 14))


def ink_mask(im):
    """크림 배경과 옅은 구름은 투명, 글자·광선만 남긴다."""
    d = np.abs(np.asarray(im).astype(int) - np.array(BG)).max(axis=2)
    return Image.fromarray((np.clip((d - 38) / 50.0, 0, 1) * 255).astype('uint8'))


def build(intro_path, alarms_path, out_path):
    intro = Image.open(intro_path).convert('RGB')
    alarms = Image.open(alarms_path).convert('RGB')
    canvas = Image.new('RGB', (W, H), BG)

    # 구름: 인트로 모서리
    for box, size, pos, corner in (
        ((0, 0, 420, 380), (293, 265), (0, 0), 'tl'),
        ((820, 2430, 1290, 2796), (352, 274), (W - 352, H - 274), 'br'),
        ((0, 2500, 380, 2796), (270, 210), (0, H - 210), 'bl'),
    ):
        c = intro.crop(box).resize(size)
        canvas.paste(c, pos, soft_corner(size, corner))

    # 해 캐릭터: 폰 뒤에서 얼굴만 보이게
    sun = intro.crop((95, 1015, 1220, 2085))
    sun = sun.resize((int(sun.width * 0.24 * K), int(sun.height * 0.24 * K)), Image.LANCZOS)
    canvas.paste(sun, (int(515 * K), int(262 * K) + DY), soft_ellipse(sun.size, 6))

    # 폰: 03 스크린샷의 폰 테두리를 둥근 사각형으로 따낸다. 아래는 캔버스 밖으로 잘린다
    s = 0.37 * K
    phone = alarms.crop((255, 786, 1140, 2796))
    phone = phone.resize((int(phone.width * s), int(phone.height * s)), Image.LANCZOS)
    m = Image.new('L', phone.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([2, 2, phone.width - 3, phone.height + 300], radius=int(172 * s), fill=255)
    canvas.paste(phone, (int(690 * K), int(62 * K) + DY), m.filter(ImageFilter.GaussianBlur(0.8)))

    # 헤드라인: 왼쪽 아래 해 캐릭터의 광선 조각은 지우고 자른다
    alarms = alarms.copy()
    ImageDraw.Draw(alarms).rectangle([0, 590, 150, 760], fill=BG)
    head = alarms.crop(headline_box(alarms))
    k = min(560 * K / head.width, 330 * K / head.height)
    head = head.resize((int(head.width * k), int(head.height * k)), Image.LANCZOS)
    canvas.paste(head, (int(40 * K) + (int(560 * K) - head.width) // 2, (H - head.height) // 2 - 5), ink_mask(head))

    canvas.save(out_path, optimize=True)


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for arg in sys.argv[3:]:
        lang, code = arg.split('=')
        suffix = '' if lang == 'en' else '_' + lang
        build(src / lang / f'01_waky_intro{suffix}_1290x2796.png',
              src / lang / f'03_alarms{suffix}_1290x2796.png',
              out / f'og-image-{code}-{W}x{H}.png')
        print(lang, '->', code)


if __name__ == '__main__':
    main()
