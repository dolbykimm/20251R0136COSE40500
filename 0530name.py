# 문자열 목록이 들어있는 변수 (여러 줄로 구분된 문자열)
input_string = """50% UAV4_1.jpg
50% UAV4_2.jpg
50% UAV4_3.jpg
50% UAV4_4.jpg
50% UAV4_5.jpg
50% UAV4_6.jpg
50% UAV4_7.jpg
50% UAV4_8.jpg
50% UAV4_9.jpg
100% UAV4_1.jpg
100% UAV4_2.jpg
100% UAV4_3.jpg
100% UAV4_4.jpg
100% UAV4_5.jpg
100% UAV4_6.jpg
100% UAV4_7.jpg
100% UAV4_8.jpg
100% UAV4_9.jpg
130% UAV4_1.jpg
130% UAV4_2.jpg
130% UAV4_3.jpg
130% UAV4_4.jpg
130% UAV4_5.jpg
130% UAV4_6.jpg
130% UAV4_7.jpg
130% UAV4_8.jpg
130% UAV4_9.jpg
150% UAV4_1.jpg
150% UAV4_2.jpg
150% UAV4_3.jpg
150% UAV4_4.jpg
150% UAV4_5.jpg
150% UAV4_6.jpg
150% UAV4_7.jpg
150% UAV4_8.jpg
150% UAV4_9.jpg"""

# 문자열을 줄바꿈(\n) 기준으로 분리하여 리스트로 변환
string_list = input_string.split('\n')

# 각 문자열의 끝에 있는 '.jpg'를 제거
cleaned_list = [s.rstrip('.jpg') for s in string_list]

# 알파벳 순서로 정렬
sorted_list = sorted(cleaned_list)

# 리스트를 튜플로 변환
result_tuple = tuple(sorted_list)

# 결과 출력
print(result_tuple)