import json


def cleanStr4SQL(s):
    return s.replace("'", "''").replace("\n", " ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    elif value == 2:
        return 'True'
    elif value == 'none':
        return 'False'
    else:
        return 'True'

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute, value))
    return L


def parseBusinessData():
    print("Parsing businesses...")
    # read the JSON file
    with open('../yelp_business.JSON', 'r', encoding='UTF-8') as f:
        outfile = open('../yelp_business.sql', 'w', encoding='UTF-8')
        line = f.readline()
        count_line = 0

        # read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id']  # business id
            business_str = "INSERT INTO business (bid, bname, address, city, state, zip, stars, reviewcount) " \
                           "VALUES ('"  + cleanStr4SQL(data['business_id']) + "','" \
                           + cleanStr4SQL(data['name']) + "'," + \
                           "'" + cleanStr4SQL(data['address']) + "'," + \
                           "'" + cleanStr4SQL(data['city']) + "'," + \
                           "'" + data['state'] + "'," + \
                           "'" + data['postal_code'] + "'," + \
                           str(data['stars']) + "," + \
                           str(data['review_count']) + ");"

            outfile.write(business_str + '\n')

            # process business hours
            # for (day, hours) in data['hours'].items():
            #     hours_str = "'" + business + "','" + str(day) + "','" + str(hours.split('-')[0]) + "','" + str(
            #         hours.split('-')[1]) + "'"
            #     outfile.write(hours_str + '\n')

            line = f.readline()
            count_line += 1
    print(count_line)
    outfile.close()
    f.close()

def parseAttributesData():
    print("Parsing attributes...")
    # read the JSON file
    with open('../yelp_business.JSON', 'r', encoding='UTF-8') as f:
        outfile = open('../yelp_attributes.sql', 'w', encoding='UTF-8')
        line = f.readline()
        count_line = 0

        # read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id']  # business id
            # process business attributes
            for (attr, value) in getAttributes(data['attributes']):
                attr_str = "INSERT INTO attributes (bid, attname, attvalue) " \
                           "VALUES ('" + business + "','" + str(attr) + "','" + int2BoolStr(str(value)) + "');"
                outfile.write(attr_str + '\n')

            line = f.readline()
            count_line += 1
        print(count_line)
        outfile.close()
        f.close()

def parseCategoryData():
    print("Parsing categories...")
    # read the JSON file
    with open('../yelp_business.JSON', 'r', encoding='UTF-8') as f:
        outfile = open('../yelp_categories.sql', 'w', encoding='UTF-8')
        line = f.readline()
        count_line = 0

        # read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id']  # business id
            # process business categories
            for category in data['categories']:
                category_str = "INSERT INTO categories (bid, cname) " \
                               "VALUES ('" + business + "','" + category + "');"
                outfile.write(category_str + '\n')

            line = f.readline()
            count_line += 1
        print(count_line)
        outfile.close()
        f.close()

def parseReviewData():
    print("Parsing reviews...")
    # reading the JSON file
    with open('../yelp_review.JSON', 'r', encoding='UTF-8') as f:
        outfile = open('../yelp_review.sql', 'w', encoding='UTF-8')
        line = f.readline()
        count_line = 0
        while line:
            data = json.loads(line)
            review_str = "INSERT INTO review (reviewid, userid, bid, stars, rdate, useful, funny, cool)" \
                " VALUES ('" + data['review_id'] + "'," + \
                "'" + data['user_id'] + "'," + \
                "'" + data['business_id'] + "'," + \
                str(data['stars']) + "," + \
                "'" + data['date'] + "'," + \
                str(data['useful']) + "," + \
                str(data['funny']) + "," + \
                str(data['cool']) + ");"
            outfile.write(review_str + '\n')
            line = f.readline()
            count_line += 1

    print(count_line)
    outfile.close()
    f.close()



def parseUserData():
    print("Parsing users...")
    # reading the JSON file
    with open('../yelp_user.JSON', 'r', encoding='UTF-8') as f:
        outfile = open('../yelp_user.sql', 'w', encoding='UTF-8')
        line = f.readline()
        count_line = 0
        while line:
            data = json.loads(line)
            user_id = data['user_id']
            user_str = "INSERT INTO users (userid, userreviewcount, useravgstars, funny, useful, cool)"\
                " VALUES ('" + user_id + "'," + \
                str(data["review_count"]) + "," + \
                str(data["average_stars"]) + "," + \
                str(data["funny"]) + "," + \
                str(data["useful"]) + "," + \
                str(data["cool"]) + ");"
            outfile.write(user_str + "\n")
            line = f.readline()
            count_line += 1

    print(count_line)
    outfile.close()
    f.close()

def parseCheckinData():
    print("Parsing checkins...")
    # reading the JSON file
    with open('../yelp_checkin.JSON', 'r',
              encoding='UTF-8') as f:  # Assumes that the data files are available in the current directory. If not,
        # you should set the path for the yelp data files.
        outfile = open('../yelp_checkin.sql', 'w', encoding='UTF-8')
        line = f.readline()
        count_line = 0
        # read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business_id = data['business_id']
            for (dayofweek, time) in data['time'].items():
                for (hour, count) in time.items():
                    checkin_str =  "INSERT INTO checkin (bid, day, hour, checkcount) " \
                        "VALUES ('" + business_id + "'," + \
                                   "'" + dayofweek + "'," + \
                                   "'" + hour + "'," + \
                                   str(count) + ");"
                    outfile.write(checkin_str + "\n")
            line = f.readline()
            count_line += 1
        print(count_line)
    outfile.close()
    f.close()


if __name__ == "__main__":
    parseBusinessData()
    parseAttributesData()
    parseCategoryData()
    parseUserData()
    parseCheckinData()
    parseReviewData()
