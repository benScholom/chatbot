"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random

string_types = ['question', 'pstatement', 'botstatement', "nonsense", "unknown", "swears", "name"]
animation = ""

def sentence_type(string):
    if is_name(string) == True:
        current_type = string_types[6]
    elif is_swear(string) == True:
        current_type = string_types[5]
    elif len(string) < 3:
        current_type = string_types[3]
    elif "?" in string[-1]:
        current_type = string_types[0]
    elif is_bstatement(string) == True:
        current_type = string_types[2]
    elif string[0] == "i" or string[1] == "i":
        current_type = string_types[1]
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


def is_bstatement(str):
    str_new = []
    for s in str:
        s_new = s.replace("?", "").replace("!", "")
        str_new.append(s_new)
    if ('you' or 'your') in str_new:
        return True
    else:
        return False

swear_bad_response = "Please avoid using profane language with me"
swear_words = ["fuck", "shit", "damn", "cunt", "dick", "ass", "bitch", 'cock', 'pussy', 'douchebag', 'douche']


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
              "situation", "politics", "business", "sports", "info", "information", "national", "local"]
news_resp = "Sorry, I have not been paying attention recently..."
news_question = "I am glad you asked. But seriously try googling it"
news_avoid = "I am not at liberty to say"
news_statement = "Your feelings are duly noted. How can I help you?"


def is_news(msg, types):
    news = determines(msg, news_words)
    global animation
    if news == True:
        for s in msg:
            if (s == "find" or s == "search" or s == "get") and types == 'question':
                animation = "giggling"
                return news_question
            elif (s == "your" or s == "opinion" or s == "think") and types == 'question':
                animation = "afraid"
                return news_avoid
            elif (s == "like" or s == "hate" or s == "love" or s == "dislike" or s == "feel") and types == 'pstatement':
                animation = "ok"
                return news_statement
            elif s == "want" and types == 'pstatement':
                animation = "ok"
                return news_question
        animation = 'bored'
        return news_resp


weather_words = ["weather", "temperature", "temp", "celcius", "fahrenheit", "season", 'hot', 'cold', "sun", "moon", "sunny", "cloud",
                 "cloudy", "rain", "rainy", "snow", "gray", "storm", "stormy", "storms"]
weather_what = "Very hot where I am. Summer right... late 20s or low 30s but still quite a blast!"
weather_find = "Google has an api for this - you should go check there"
weather_like = "I am in an air-conditioned room, so I have no opinion"
weather_neutral = "Maybe. Check online to be sure."


def is_weather(msg, types):
    weather = determines(msg, weather_words)
    global animation
    if weather == True:
        for s in msg:
            print(s)
            if (s == 'what' or s == "what's" or s == 'now' or s == 'today' or s == 'give' or s == 'outside') and types == 'question':
                animation = "dancing"
                return weather_what
            elif (s == 'like' or s == 'nice' or s == 'hate' or s == "feel") and types == 'pstatement':
                animation = "ok"
                return weather_like
            elif (s == "where" or s == "find" or s == "see" or s == 'look') and types == 'question':
                animation = "takeoff"
                return weather_find
        return weather_neutral

pet_words = ['dog', 'cat', 'snake', 'pet', 'pets', 'puppy', 'puppies', 'dogs', 'cats', 'kittens', 'kitty', 'leash' 'collar', 'kitten', 'fur', 'fuzzy']
pet_want = "You got me thinking about owning a pet - too bad bots cannot do that"
pet_cute = "I think animals are adorable!"
pet_hate = "I don't understand, they are so cute!"

def is_pet(msg, types):
    pets = determines(msg, pet_words)
    global animation
    if pets == True:
        for s in msg:
            if (types == 'question' or types == "pstatement") and (s == "own" or s == "have" or s == "want"):
                animation = 'heartbroke'
                return pet_want
            elif (types == 'pstatement' or 'unknown') and s in insults:
                animation = "confused"
                return pet_hate
        animation = "dog"
        return pet_cute


jokes = ["A guy walks into a bar and says....Ouch!", "What do you call", "My girldriend and I laugh about how competitive we are. I laugh more.",
         "I hate russian dolls, they are so full of themselves.", "I recently decided to sell my vacuum cleaner as all it was doing was gathering dust.",
         "I've just written a song about tortillas; actually, it’s more of a rap.", "I was at the bank the other day, and an elderly woman asked me to check her balance. So I pushed her over."
         , "I'm great at multitasking. I can waste time, be unproductive, and procrastinate all at once.", "I would lose weight, but I hate losing.", "My girlfriend told me she was leaving me because I keep pretending to be a Transformer. I said, 'No, wait! I can change.'"
         , "Is your refrigerator running? Cause I might vote for it.", "Standing in the park, I was wondering why a Frisbee gets larger the closer it gets. Then it hit me.",
         "I got an odd-job man in. He was useless. Gave him a list of eight things to do and he only did numbers one, three, five and seven.",
         "My dad said, always leave them wanting more. Ironically, that’s how he lost his job in disaster relief.", "My dad suggested I register for a donor card. He's a man after my own heart."]
insults = ['suck', 'blow', 'stupid', 'dumb', 'jerk', 'meanie', 'evil', 'slimey', 'slimeball', 'coward', 'boring',
           'lame', 'lazy', 'illiterate', 'primitive', 'hate']
compliments = ['cool', 'best', 'rule', 'smart', 'amazing', 'wonderful', 'love', 'like', 'great', 'nice', 'pleasant',
               'interesting']
rw_bstatement_pos = ['Excellent!', 'Awesome', 'I appreciate it', 'lovely', "I love it", 'thank you']
re_bstatement_neg = ["I'm sorry you feel that way", 'your attitude needs work',
                     "what's wrong with you?", 'stop being so negative', 'why are you like this?', 'stop it']
rw_questions = ["I don't know", "I cannot help you", "I don't understand the question",
                "Can't say, I am not omniscent", "Not sure", "Try another question"]
rw_generic = ['whatever', "that's cool", "and...?", 'tell me more', 'gnarly', 'sounds interesting']


def is_random(msg, value):
    global animation
    for s in msg:
        if s in insults and (value == 'botstatement' or value ==  'pstatement' or value == 'question'):
            bot_resp = random.choice(re_bstatement_neg)
            animation = "crying"
            return bot_resp
        elif value == 'bstatement' and s in compliments:
            bot_resp = random.choice(rw_bstatement_pos)
            animation = "inlove"
            return bot_resp
        elif value == 'question':
            animation = "ok"
            bot_resp = random.choice(rw_questions)
            return bot_resp
    bot_resp = random.choice(rw_generic)
    return bot_resp

def evaluator(str, value):
    print(value)
    print(len(str))
    print(str)
    global animation
    if value == "swears":
        animation = "no"
        return swear_bad_response
    elif (value == "unknown" or value == "pstatement" or value == "botstatement") or (
        ("jokes" or "joke" or "funny") in str):
        print('joke')
        funny =  "You want a joke!? Here's one: " + random.choice(jokes) + "...lol get it!"
        animation = "laughing"
        return funny
    elif value == 'name' and (('I' or 'my' in str) or (len(str) < 4)):
        animation  = "excited"
        return "Pleased to meet you "
    elif value == 'name':
        animation = 'confused'
        return "I do not know to whom you are referring"
    elif value == "nonsense":
        animation = 'confused'
        return nonsense_resp
    else:
        return_list = []
        return_list.append(is_weather(str, value))
        return_list.append(is_news(str, value))
        return_list.append(is_pet(str, value))
        print(return_list)
        for r in return_list:
            if r != None:
                return r
        return is_random(str, value)

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
    return json.dumps({"animation": animation, "msg": response})


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
