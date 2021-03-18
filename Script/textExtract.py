import cv2 as cv
import baiduOCR
import os


def generateFrameListItem(match_substring, filename):
    # find the frame
    words = []
    tail = filename.find(match_substring)
    try:
        if match_substring != '_pre.jpg':
            frame_count = int(filename[0:tail])
        else:
            frame_count = int(filename[0:tail]) - 1
        print("frame count", frame_count)
    except ValueError:
        print("文件名中数字部分没有提取成功")
    else:
        print("成功从文件名中提取帧数信息")
    # get the src
    src = os.path.join(key_frame_path, filename)
    # compute text
    words_result, words_num = baiduOCR.get_raw_text(src)
    for item in words_result:
        # print(item['words'])
        words.append(item['words'])
    return frame_count, src, words, words_num


def takeForSort(elem):
    return elem[0]


def generateFrameList(key_frame_path):
    pre_frame_list = []
    start_frame_list = []
    end_frame_list = []
    for root, dirs, files in os.walk(key_frame_path):
        for file in files:
            if file.find('_pre.jpg') >= 0:
                frame, src, words, words_num = generateFrameListItem('_pre.jpg', file)
                pre_frame_list.append([frame, src, words, words_num])

            if file.find('_start.jpg') >= 0:
                frame, src, words, words_num = generateFrameListItem('_start.jpg', file)
                start_frame_list.append([frame, src, words, words_num])

            if file.find('_end.jpg') >= 0:
                frame, src, words, words_num = generateFrameListItem('_end.jpg', file)
                end_frame_list.append([frame, src, words, words_num])
    pre_frame_list.sort(key=takeForSort)
    start_frame_list.sort(key=takeForSort)
    end_frame_list.sort(key=takeForSort)
    # print(len(pre_frame_list))
    # print(len(start_frame_list))
    # print(len(end_frame_list))

    for i in range(len(pre_frame_list)):
        print(pre_frame_list[i][0], start_frame_list[i][0], end_frame_list[i][0])
        if pre_frame_list[i][3] < 5 and i > 0:
            pre_frame_list[i].append("loading")
            start_frame_list[i].append("loading")
            end_frame_list[i - 1].append("loading")
        elif abs(pre_frame_list[i][3] - end_frame_list[i][3]) <= 2:
            pre_frame_list[i].append("loading")
            start_frame_list[i].append("loading")
            end_frame_list[i - 1].append("loading")

    pre_frame_list = [item for item in pre_frame_list if len(item) == 4]
    print(len(pre_frame_list))

    start_frame_list = [item for item in start_frame_list if len(item) == 4]
    print(len(start_frame_list))

    end_frame_list = [item for item in end_frame_list if len(item) == 4]
    print(len(end_frame_list))
    return pre_frame_list, start_frame_list, end_frame_list


if __name__ == '__main__':
    key_frame_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'key_frame', 'luping1')
    pre, start, end = generateFrameList(key_frame_path)
