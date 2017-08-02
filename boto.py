"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json

string_types = ['question', 'pstatement', 'botstatement', "nonsense", "unknown", "swears", "name"]


def sentence_type(string):
    if is_name(string) == True:
        current_type = string_types[6]
    elif is_swear(string) == True:
        current_type = string_types[5]
    elif len(string) < 3:
        current_type = string_types[3]
    elif "?" in string[-1]:
        current_type = string_types[0]
    elif string[0] == "i" or string[1] == "i":
        current_type = string_types[1]
    elif string[0] == "you" or string[1] == "you":
        current_type = string_types[2]
    else:
        current_type = string_types[4]
    return current_type


nonsense_resp = "Please elaborate"

names = ['ben', 'daniel', 'josh', 'nath', 'tanya', 'sylvie', 'lorine', 'rifat', 'yan', 'deborah', 'lior', 'guy',
         'lauren', 'gilad', 'roni', 'yael', 'gideon', 'omer']


def is_name(str):
    for w in names:
        if w in str:
            return True


def evaluator(str, value):
    print(value)
    print(len(str))
    print(str)
    if value == 'name' or 'I' in str and len(str) < 4:
        return "Pleased to meet you"
    elif value == "swears":
        return swear_bad_response
    elif value == "nonsense":
        return nonsense_resp
    else:
        return_list = []
        return_list.append(is_weather(str, value))
        return_list.append(is_news(str, value))
        print(return_list)
        for r in return_list:
            if r != None:
                return r


swear_bad_response = "Please avoid using profane language with me"
swear_words = ["fuck", "shit", "damn", "cunt", "dick", "ass", "bitch"]


def is_swear(msg):
    for s in msg:
        if s in swear_words:
            return True


def determines(msg, wordbank):
    new_msg = []
    for s in msg:
        new_s = s.replace("?", "")
        new_msg.append(new_s)
    for w in wordbank:
            if w in new_msg:
                print(new_msg)
                return True



news_words = ["news", "world", "happened", "event", "fake", "cnn", "fox", "msnbc", "abc", "nbc", "cbs", "global",
              "situation", "politics", "business", "sports", "info", "information"]
news_resp = "Sorry, I have not been paying attention recently..."
news_question = "I am glad you asked. But seriously try googling it"
news_avoid = "I am not at liberty to say"
news_statement = "Your feelings are duly noted"


def is_news(msg, types):
    news = determines(msg, news_words)
    if news == True:
        for s in msg:
            if "find" or "search" or "get" in s and types == 'question':
                print('1')
                return news_question
            elif "your" or "opinion" or "think" in s and types == 'question':
                print('2')
                return news_avoid
            elif "like" or "hate" or "love" or "dislike" or "feel" in s and types == 'pstatement':
                print('3')
                return news_statement
            elif "want" and types == 'pstatement':
                print('4')
                return news_question
            else:
                print('5')
                return news_resp


weather_words = ["weather", "temperature", "temp", "celcius", "fahrenheit", "season", "sun", "moon", "sunny", "cloud",
                 "cloudy", "rain", "rainy", "snow", "gray", "storm", "stormy", "storms"]
weather_what = "Very hot and humid where I am. Summer right... late 20s or low 30s"
weather_find = "Google has an api for this - you should check it out"
weather_like = "I guess its nice out. I am in an air-conditioned room"


def is_weather(msg, types):
    weather = determines(msg, weather_words)
    if weather == True:
        for s in msg:
            if 'what' or 'now' or 'today' or 'give' or 'outside' in s and types == 'question':
                return weather_what
            elif 'like' or 'nice' or 'hate' or "feel" in s:
                return weather_like
            else:
                return weather_find


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    string = user_message.lower().split(" ")
    type = sentence_type(string)
    print(type)
    response = evaluator(string, type)
    print(response)
    return json.dumps({"animation": "inlove", "msg": response})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
