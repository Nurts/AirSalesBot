import telebot
import requests
import json
import time
import constants
from currency_converter import CurrencyConverter
from emoji import emojize

BOLD = '\033[1m'
END = '\033[0m'
testingVar = 0
bot = telebot.TeleBot(constants.token)

user_database = {}


def make_request(user_id):
    reqvalue = 0
    answer = constants.error_message
    cur_data = {}
    if str(user_id) in user_database:
        cur_data = user_database[str(user_id)]
    #json.load(open('cur_data.json'))
    url = 'https://api.skypicker.com/flights?flyFrom=' + cur_data['cityFrom'] + '&to=' + cur_data['cityTo'] + '&dateFrom=' + cur_data['dateFrom'] + \
          '&dateTo=' + cur_data['dateTo'] + '&partner=picky' + '&adults=' + str(cur_data['adults']) + '&children=' +\
          str(cur_data['children']) + '&dtimefrom=' + cur_data['dtimefrom'] +\
          '&dtimeto=' + cur_data['dtimeto']
    req_dict = requests.get(url).json()
    #write_json(req.json())

    if 'data' in req_dict:
        if len(req_dict['data']) == 0:
            answer = "Sorry! But There is no available tickets"
        else:
            answer = jsontoString(req_dict['data'][0])
            if str(user_id) in user_database:
                user_database[str(user_id)]['tickets'].clear()
            reqvalue = 1;
            counter = 0;
            for each in req_dict['data']:
                if counter == 10:
                    break
                counter += 1
                if str(user_id) in user_database:
                    user_database[str(user_id)]['tickets'].append(each)


    bot.send_message(user_id, answer, parse_mode="Markdown")

    return reqvalue


def jsontoString(each):
    emm1 = emojize(":credit_card:", use_aliases=True)
    emm2 = emojize(":customs:", use_aliases=True)
    emm3 = emojize(":arrow_upper_right:", use_aliases=True)
    emm4 = emojize(":arrow_lower_right:", use_aliases=True)
    emm5 = emojize(":information_source:", use_aliases=True)
    ticket_url = each['deep_link']
    price = each['price']
    c = CurrencyConverter()
    tem1 = emm2 + "*From airport:* " + each['cityFrom'] + "\n" + emm2 + "*To airport:* " + each['cityTo'] + "\n"
    tem2 = emm3 + "*Time leaving:* " + time.strftime("%D %H:%M", time.gmtime(int(each['dTime']))) + "\n" + emm4 + "*Time arriving:* " + time.strftime("%D %H:%M",time.gmtime(int(each['aTime'])))
    tem3 = emm1 + "*The best Price:* €" + str(price) + " (" + str(c.convert(price, 'EUR', 'USD'))[:6] + " USD)" + "\n"
    answer = tem3 + tem1 + tem2 + "\n" + emm5 + "*For more info:*" + goo_shorten_url(ticket_url) + "\n\n"

    return answer


def translate_text(text):
    req_url = constants.translate_url + 'key=' + constants.translate_key + '&text=' + text + "&lang=en"
    r = requests.post(req_url)
    return r.json()['text'][0]


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=True)
        f.close()


def log(message):
    print("\n ----------------")
    from datetime import datetime
    print(datetime.now())
    print("Message from {0} {1}. ( id = {2}) \n Text: {3}".format(message.from_user.first_name, message.from_user.last_name,
                                                                  str(message.from_user.id), message.text))


def goo_shorten_url(url):
    post_url = constants.shortener_url
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    return r.json()['id']


@bot.message_handler(commands=['start', 'help'])
def start_function(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/end')
    msg = bot.send_message(message.from_user.id, constants.startMessageGen(), reply_markup=user_markup, parse_mode="Markdown")
    bot.register_next_step_handler(msg, initial_case_step)


def home_buttons(user_id):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.add('/start', '/end', '/addPassengers')
    user_markup.row('/next', '/choose_time')
    bot.send_message(user_id, constants.homeMessageGen(), reply_markup=user_markup)


@bot.message_handler(commands=['end'])
def end_function(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    id = str(message.from_user.id)
    if id in user_database:
        del user_database[id]
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, constants.endMessageGen(), reply_markup=hide_markup)


@bot.message_handler(commands=['addPassengers'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/addAdult', '/addChild')
    user_markup.row('/done', '/reset')
    bot.send_message(message.from_user.id, constants.addPassengersInstructions(), reply_markup=user_markup)


def cur_state_of_passengers(user_id):
    if str(user_id) in user_database:
        bot.send_message(user_id, 'Adults: ' + str(user_database[str(user_id)]['adults']) +
                         "; Children: " + str(user_database[str(user_id)]['children'])+";")


@bot.message_handler(commands=['addAdult'])
def handle_text(message):
    id = str(message.from_user.id)
    if id in user_database:
        user_database[id]['adults'] += 1
    cur_state_of_passengers(message.from_user.id)


@bot.message_handler(commands=['addChild'])
def handle_text(message):
    id = str(message.from_user.id)
    if id in user_database:
        user_database[id]['children'] += 1
    cur_state_of_passengers(message.from_user.id)


@bot.message_handler(commands=['reset'])
def handle_text(message):
    id = str(message.from_user.id)
    if id in user_database:
        user_database[id]['children'] = 0
        user_database[id]['adults'] = 1
    cur_state_of_passengers(message.from_user.id)


@bot.message_handler(commands=['done'])
def handle_text(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    id = str(message.from_user.id)
    if id in user_database:
        user_database[id]['id'] = 0
    answer = make_request(message.from_user.id)
    home_buttons(message.from_user.id)


@bot.message_handler(commands=['next'])
def handle_text(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    answer = "No more tickets to search! Please press /start button";
    id = str(message.from_user.id)
    if id in user_database:
        user_database[id]['id']+=1
        if len(user_database[id]['tickets']) <= user_database[id]['id']:
            pass
        else:
            answer = jsontoString(user_database[id]['tickets'][user_database[id]['id']])
    bot.send_message(message.from_user.id, answer, parse_mode="Markdown")


@bot.message_handler(commands=['choose_time'])
def choosing_function(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('morning', 'afternoon')
    user_markup.row('evening', 'night')
    user_markup.row('/start', '/end')
    msg = bot.send_message(message.from_user.id, constants.chooseTimeInstructions, reply_markup=user_markup, parse_mode="Markdown")
    bot.register_next_step_handler(msg, choose_time_step)


def choose_time_step(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    if message.text == "/start":
        home_buttons(message.from_user.id)
    elif message.text == "/end":
        end_function(message)
    else:
        if message.text == "morning":
            timefrom = '06:00'
            timeto = '12:00'
        elif message.text == "afternoon":
            timefrom = '12:00'
            timeto = '18:00'
        elif message.text == "evening":
            timefrom = '18:00'
            timeto = '00:00'
        elif message.text == "night":
            timefrom = '00:00 '
            timeto = '06:00'
        elif len(message.text.split('-')) != 2:
            bot.send_message(message.from_user.id, constants.error_message + "\nThe daytime was reset!")
            timefrom = '00:00'
            timeto = '00:00'
        else:
            timefrom, timeto = message.text.split('-')

        timefrom = " ".join(timefrom.split())
        timeto = " ".join(timeto.split())
        id = str(message.from_user.id)
        if id in user_database:
            user_database[id]['dtimefrom'] = timefrom
            user_database[id]['dtimeto'] = timeto
        result = make_request(message.from_user.id)
        if result == 0 and (id in user_database):
                user_database[id]['dtimefrom'] = '00:00'
                user_database[id]['dtimeto'] = '00:00'
        home_buttons(message.from_user.id)


def initial_case_step(message):
    bot.send_chat_action(message.from_user.id,'typing')
    if message.text == "/start":
        start_function(message)
    elif message.text == "/end":
        end_function(message)
    elif len(message.text) > 10:
        inputData = message.text.split("-")
        if len(inputData) == 4 or len(inputData) == 3 :
            cityFrom = " ".join(inputData[0].split())
            cityFrom = translate_text(cityFrom)
            cityTo = " ".join(inputData[1].split())
            cityTo = translate_text(cityTo)
            dateFrom = " ".join(inputData[2].split())
            dateTo = dateFrom
            if len(inputData) == 4:
                dateTo = " ".join(inputData[3].split())

            data = {"cityFrom": cityFrom, "cityTo": cityTo, "dateFrom": dateFrom, "dateTo": dateTo,
                    "dtimefrom": '00:00', "dtimeto": "00:00", "adults": 1, "children": 0,
                    "id": 0, "tickets": []}

            user_database[str(message.from_user.id)] = data
            result = make_request(message.from_user.id)
            if result == 1:
                home_buttons(message.from_user.id)
            else:
                start_function(message)
    else:
        bot.send_message(message.from_user.id, constants.tryagain_message)
        start_function(message)
    #log(message, answer)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
