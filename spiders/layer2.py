import scrapy
import requests
import csv
import time

from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest


class FacebookSpider(scrapy.Spider):
    csv_personal_information = 'data/personal_information.csv'
    with open(csv_personal_information, 'a') as csvfile:
        fieldnames = [
            'name', 'work', 'education', 'live_now', 'live', 'gender',
            'gender_like', 'relationship', 'religion', 'blood', 'birthday', 'website', 'email',
            'url'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    url_test = [
        'https://m.facebook.com/profile.php?v=info&id=4',
        'https://m.facebook.com/profile.php?v=info&id=100017247636008',
        'https://m.facebook.com/profile.php?v=info&id=100005420655227',
        'https://m.facebook.com/profile.php?v=info&id=100002379548465',
    ]

    def get_personal_url(path, fieldnames):
        arr_personal_url = []
        with open(path, 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in reader:
                arr_personal_url.append(row[fieldnames[0]])
            arr_personal_url.pop(0)
            return arr_personal_url

    name = 'deep_crawling'
    email = ''
    password = ''
    arr_personal_url = get_personal_url('data/personal_url.csv', ['url'])

    def start_requests(self):
        return [
            Request(
                "https://m.facebook.com/login.php",
                meta={'cookiejar': 1},
                callback=self.post_login)
        ]

    def post_login(self, response):
        return [
            FormRequest.from_response(
                response,  #"https://m.facebook.com/login.php",
                meta={'cookiejar': response.meta['cookiejar']},
                formdata={'email': self.email,
                          'pass': self.password},
                callback=self.after_login, )
        ]

    def after_login(self, response):
        #for row in self.url_test:
        for row in self.arr_personal_url:
            yield scrapy.Request(
                row,
                meta={'cookiejar': response.meta['cookiejar']},
                callback=self.get_global_url)

    def get_global_url(self, response):
        url = response.url
        try:
            url.index('id')
            global_url = 'https://m.facebook.com/profile.php?v=info&id=' + url[
                40:]
        except:
            global_url = 'https://m.facebook.com/' + url[25:] + '?v=info'

        return scrapy.Request(
            global_url,
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.get_personal_information)

    def get_personal_information(self, response):
        body = BeautifulSoup(response.body.decode())
        about = {}

        name = body.find_all("strong")
        for row in name:
            about['name'] = row.text
            print(row.text)

        work = body.find_all("div", {"id": 'work'})
        for row in work:
            about['work'] = row.text[4:]
            print(row.text[4:])

        education = body.find_all("div", {"id": 'education'})
        for row in education:
            about['education'] = row.text[2:]
            print(row.text[2:])

        live_now = body.find_all("div", {"title": '現居城市'})
        for row in live_now:
            about['live_now'] = row.text[4:]
            print(row.text[4:])

        live = body.find_all("div", {"title": '家鄉'})
        for row in live:
            about['live'] = row.text[2:]
            print(row.text[2:])

        gender = body.find_all("div", {"title": '性別'})
        for row in gender:
            about['gender'] = row.text[2:]
            print(row.text[2:])

        gender_like = body.find_all("div", {"title": '戀愛性向'})
        for row in gender_like:
            about['gender_like'] = row.text[4:]
            print(row.text[4:])

        relationship = body.find_all("div", {"id": 'relationship'})
        for row in relationship:
            about['relationship'] = row.text[4:]
            print(row.text[4:])

        religion = body.find_all("div", {"title": '宗教信仰'})
        for row in religion:
            about['religion'] = row.text[4:]
            print(row.text[4:])

        blood = body.find_all("div", {"title": '血型'})
        for row in blood:
            about['blood'] = row.text[2:-1]
            print(row.text[2:-1])

        birthday = body.find_all("div", {"title": '生日'})
        for row in birthday:
            about['birthday'] = row.text[2:]
            print(row.text[2:])

        website = body.find_all("div", {"title": '網站'})
        for row in website:
            about['website'] = row.text[2:]
            print(row.text[2:])

        email = body.find_all("div", {"title": '電子郵件'})
        for row in email:
            about['email'] = row.text[4:]
            print(row.text[4:])

        about['url'] = response.url
        print(response.url)

        try:
            about['name']
        except:
            about['name'] = None
        try:
            about['work']
        except:
            about['work'] = None
        try:
            about['education']
        except:
            about['education'] = None
        try:
            about['live_now']
        except:
            about['live_now'] = None
        try:
            about['live']
        except:
            about['live'] = None
        try:
            about['gender']
        except:
            about['gender'] = None
        try:
            about['gender_like']
        except:
            about['gender_like'] = None
        try:
            about['relationship']
        except:
            about['relationship'] = None
        try:
            about['religion']
        except:
            about['religion'] = None
        try:
            about['blood']
        except:
            about['blood'] = None
        try:
            about['birthday']
        except:
            about['birthday'] = None
        try:
            about['website']
        except:
            about['website'] = None
        try:
            about['email']
        except:
            about['email'] = None
        try:
            about['url']
        except:
            about['url'] = None

        with open(self.csv_personal_information, 'a') as csvfile:
            fieldnames = [
                'name', 'work', 'education', 'live_now', 'live', 'gender',
                'gender_like', 'relationship', 'religion', 'blood', 'birthday', 'website',
                'email', 'url'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader()
            writer.writerow({
                fieldnames[0]: about['name'],
                fieldnames[1]: about['work'],
                fieldnames[2]: about['education'],
                fieldnames[3]: about['live_now'],
                fieldnames[4]: about['live'],
                fieldnames[5]: about['gender'],
                fieldnames[6]: about['gender_like'],
                fieldnames[7]: about['relationship'],
                fieldnames[8]: about['religion'],
                fieldnames[9]: about['blood'],
                fieldnames[10]: about['birthday'],
                fieldnames[11]: about['website'],
                fieldnames[12]: about['email'],
                fieldnames[13]: about['url'],
            })
