import re
import pyautogui
import time

#offset needs 3seconds to me
offset = [0, 0, -14]
#index for skip 
skip_index = 0

# 1:30:40 -> [1, 30, 40]
def timestampToList(timestamp : str) -> list :
    time_split = timestamp.split(':')
    result = []
    for time in time_split:
        result.append(int(time.strip()))
    return result

# add [hour, minute, time] + [hour, minute, time]
def add_time(time1, time2):
    new_time = []
    for i in range(0, len(time1)):
        new_time.append(time1[i] + time2[i])

    for i in range(1, len(time1)):
        r_index = len(time1) - i
        if new_time[r_index] > 60:
            new_time[r_index] -= 60
            new_time[r_index-1] += 1
        elif new_time[r_index] < 0:
            new_time[r_index] += 60
            new_time[r_index-1] -= 1
            if new_time[r_index-1] < 0 :
                new_time[r_index-1] += 60
                new_time[r_index-2] -= 1
    return new_time

def time_to_seconds(time1) :
    result = time1[0] * 3600
    result += time1[1] * 60
    result += time1[2]

    return result

def time_to_string(time1) :
    return str(time1[0]) + ":" + str(time1[1])  + ":" + str(time1[2])

time_list = []
with open('time.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines() :
        m = re.search(r'\d{1}:\d{2}:\d{2} ~ \d{1}:\d{2}:\d{2}', line)
        time_string = m.group(0)
        #[[[start_hour, start_minute, start_seconds] , diff_time_seconds],  ]
        time_split = time_string.split('~')
        time_list.append([timestampToList(time_split[0]), timestampToList(time_split[1])])


print("program will be start after 3 seconds later")
time.sleep(3)
pyautogui.click(x=200, y= 200)

for index in range(skip_index, len(time_list)):
    time_list[index][1] = time_to_seconds(time_list[index][1]) - time_to_seconds(time_list[index][0])
    time_list[index][0] = add_time(time_list[index][0], offset)
    print(index, time_list[index][0], time_list[index][1])
    pyautogui.press('g')
    pyautogui.typewrite(time_to_string(time_list[index][0]))
    pyautogui.press('enter')
    pyautogui.press('esc')
    pyautogui.press('space')
    time.sleep(time_list[index][1])
    pyautogui.press('space')
    
    
