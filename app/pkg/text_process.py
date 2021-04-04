replace_map = {
    "&#39;": "'"
}
def transform(text):
    for key in replace_map:
        text = text.replace(key, replace_map[key])
    return text

convert_emotion = {
    0: "其它",
    1: "喜歡",
    2: "悲傷",
    3: "噁心",
    4: "憤怒",
    5: "開心"
}