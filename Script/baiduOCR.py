from aip import AipOcr

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def get_raw_text(img_path):
    """ 你的 APPID AK SK """
    APP_ID = '18362444'
    API_KEY = 'Ut7nYPy57iROCHtYOyvf3uww'
    SECRET_KEY = 'pLvjn05zf64LS77ZQgOk1gGkBHePsCyr'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    image = get_file_content(img_path)
    """ 调用通用文字识别, 图片参数为本地图片 """
    # print(client.basicGeneral(image))

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    result_raw = client.basicGeneral(image, options)
    print('words num', result_raw['words_result_num'])
    return result_raw['words_result'], result_raw['words_result_num']


def icon_text(result_raw):
    max_prob = 0
    text = ""
    for item in result_raw['words_result']:
        if (item['probability']['average'] > max_prob):
            max_prob = item['probability']['average']
            text = item['words']
    # print(text)
    # print(max_prob)
    return text
