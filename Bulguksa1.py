import pyautogui as pyg
import win32api
import time
import pandas as pd

position = 0
size = 40


n = 31
while True:

    df = pd.DataFrame(index = range(size),columns=["x1","y1","x2","y2","x3","y3","x4","y4"])

    while True:
        # 첫 줄(빨강)
        i = 0
        while True:
            time.sleep(0.05)

            # 기록(W : Write)

            w = win32api.GetKeyState(0x57)
            if w < 0:
                print("w", i)
                position = pyg.position()

                x = int(position.x)
                y = int(position.y)

                df.iloc[i,0] = x
                df.iloc[i,2] = x
                df.iloc[i,4] = x
                df.iloc[i,6] = x
                
                i += 1

                time.sleep(0.3)

            e = win32api.GetKeyState(0x45)
            if e < 0:
                print("e")
                for s in range(size):
                    df.iloc[s,1] = y
                time.sleep(0.3)
                break
            else:
                pass

            q = win32api.GetKeyState(0x51)
            if q < 0:
                print("q")
                time.sleep(0.3)
                break
            else:
                pass

        # 둘쨰 줄(노랑)
        i = 0
        j = 3

        while True:
            time.sleep(0.05)

            # 기록(W : Write)

            w = win32api.GetKeyState(0x57)
            if w < 0:
                print("w", i, j)
                position = pyg.position()

                y = int(position.y)

                if j >= 7:
                    for s in range(size):
                        df.iloc[s,j] = y
                elif j < 7:
                    df.iloc[i,j] = y
                
                i += 1
                
                time.sleep(0.3)

            e = win32api.GetKeyState(0x45)
            if e < 0:
                print("e")
                j += 2
                i = 0
                time.sleep(0.3)
            else:
                pass

            q = win32api.GetKeyState(0x51)
            if q < 0:
                print("q")
                time.sleep(0.3)
                break
            else:
                pass

        # 매크로 종료(Q : Quit)
        q = win32api.GetKeyState(0x51)
        if q < 0:
            print("q")
            break
        else:
            pass

    print('한 장 끝 고생햇슈 ㅋ q는 더 누르지 마 !!!!!')
    print(df)

    df.to_excel(f'D:\\LAB&COMPETITION\\불국사\\짝수 엑셀\\output{n}.xlsx', index = False)

    n += 1
    time.sleep(0.5)
    print("다음장 시작")