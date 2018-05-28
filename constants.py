from emoji import emojize

# constants

token = "497558459:AAH5MwqMPP25GMADY5tPM_6Ej5PfT3dNHec"
shortener_key = 'AIzaSyBSNqANV8p1tcQkECi6XKD98Ubb-McE9Ns'
shortener_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyBSNqANV8p1tcQkECi6XKD98Ubb-McE9Ns'
translate_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
translate_key = 'trnsl.1.1.20180414T171052Z.35fa0c867cd681d3.88357a14f07b92e4601ac59f6ab10965a51af354'

error_message = "Sorry! But there is something wrong in your input data! (Use the same format as in example)"
tryagain_message = "Input Error! Please Try again! You should use same format as in Examples"


def startMessageGen():
    m1 = "Hello, my dear friend!\nI can find the cheapest airline tickets for you!"
    m2 = "You have to just write some information about destinations and date in the given order:\n"
    m3 = "City from you will fly out"
    m4 = "City where you will fly"
    m5 = "Date of the fly or first day of the interval"
    m6 = "Last day of the interval(optional)"
    m7 = "For example:\n_Moscow - Astana - 19/05/2018_  "
    m8 = "_Almaty - Kazan - 16/04/2018 - 25/04/2018_  "
    m9 = "*You can use any language that you want:3*"
    em1 = emojize(":airplane:", use_aliases=True)
    em2 = emojize(":date:", use_aliases=True)
    em3 = emojize(":small_orange_diamond:", use_aliases=True)
    em4 = emojize(":small_blue_diamond:", use_aliases=True)
    em8 = emojize(":arrow_upper_right:", use_aliases=True)
    em9 = emojize(":arrow_lower_right:", use_aliases=True)
    em5 = emojize(":white_check_mark:", use_aliases=True)
    em6 = emojize(":warning:", use_aliases=True)
    sendtext = m1 + em1 + "\n" + m2 + em3 + m3 + em8 + "\n" + em4 + m4 + em9 + "\n" + em3 + m5 + em2 + "\n" + em4 + m6 + em2 + "\n" + m7 + em5 + "\n" + m8 + em5 + "\n\n" + em6 + m9
    return sendtext

def endMessageGen():
    emn1 = emojize(":wave:", use_aliases=True)
    emn2 = emojize(":pray:", use_aliases=True)
    emn3 = emojize(":sunrise_over_mountains:", use_aliases=True)
    emn4 = emojize(":tent:", use_aliases=True)
    return "GoodBye, my dear friend! " + emn1 + \
           "\nThank you for choosing our service! " + emn2 + \
           "\nWe wish you safe and comfortable flight, and unforgettable travel! " + emn4 + emn3


def homeMessageGen():
    em7 = emojize(":arrow_forward:", use_aliases=True)
    em8 = emojize(":blush:", use_aliases=True)
    em9 = emojize(":pencil2:", use_aliases=True)
    return em9 + "Now you can choose number of passangers and suitable daytime:\n" + em7 + \
           "To add passengers press /addPassengers, please\n" + em7 + \
           "To choose daytime press /choose_time, please\n" + em7 + \
           "If you want another ticket, press /next" + "\nPress /start to choose other cities!"

def addPassengersInstructions():
    em11 = emojize(":man:", use_aliases=True)
    em12 = emojize(":baby:", use_aliases=True)
    em13 = emojize(":family:", use_aliases=True)
    em14 = emojize(":leftwards_arrow_with_hook:", use_aliases=True)
    em15 = emojize(":ballot_box_with_check:", use_aliases=True)
    return "Now add passengers, please! " + em13 + "\nTo add adult passenger, press /addAdult " + em11 + \
           "\nTo add child passenger, press /addChild " + em12 + \
           "\nIf you have already chosen, press /done " + em15 + \
           "\nIf you mistaken, press /reset to reset values " + em14


chooseTimeInstructions = "Now you have to choose suitable time for you:\n" + \
                        "Send time interval by differing them by *hyphen*!\n" + \
                        "_Example: 20:00-23:30_\n" + \
                        "*You can just choose the on of the following variants:*\n" + \
                        "_Morning(6:00-12:00)_\n" + "_Afternoon(12:00-18:00)_\n" + \
                        "_Evening (18:00-24:00)_\n" + "_Night(00:00-6:00)_\n"

