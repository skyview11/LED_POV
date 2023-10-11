import argparse    # 1. argparse를 import한다.

parser = argparse.ArgumentParser(description='이 프로그램의 설명(그 외 기타등등 아무거나)')    # 2. parser를 만든다.

# 3. parser.add_argument로 받아들일 인수를 추가해나간다.
parser.add_argument('-nl', '--n_led', type=int, default=16, help='POV 날개에 달린 LED 개수')    # 필요한 인수를 추가
parser.add_argument('-er', '--encoder_resolution', type=float, help='encoder가 얻을 수 있는 각도 회전의 최솟값, 360/해상도')
parser.add_argument('--arg3')    # 옵션 인수(지정하지 않아도 괜칞은 인수를 추가
parser.add_argument('-a', '--arg4')   # 자주 사용하는 인수라면 약칭이 있으면 사용할 때 편리하다

args = parser.parse_args()    # 4. 인수를 분석

