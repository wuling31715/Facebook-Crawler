import facebook
import requests
import csv
import time

arr_personal_id = []
arr_personal_url = []
arr_personal_data = []


def get_personal_id(graph, video_id, path, fieldnames):
    with open(path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        video = graph.get_object(
            id=video_id,
            fields='likes', )
        for row in video['likes']['data']:
            personal_id = row['id']
            writer.writerow({fieldnames[0]: personal_id})
            print(personal_id)
        try:
            next_page_url = video['likes']['paging']['next']
        except:
            print('<= 25')

        while True:
            try:
                next_page = requests.get(next_page_url).json()
                for row in next_page['data']:
                    personal_id = row['id']
                    writer.writerow({fieldnames[0]: personal_id})
                    print(personal_id)
                next_page_url = next_page['paging']['next']
            except:
                break
    print('get_personal_id() done')


def get_personal_url(path, fieldnames):
    with open(path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in arr_personal_id:
            try:
                personal_url = 'https://www.facebook.com/app_scoped_user_id/' + row
                writer.writerow({
                    fieldnames[0]: personal_url,
                })
                print(personal_url)
            except:
                pass
    print('get_personal_url() done')


def csv_write(arr, path, fieldnames):
    with open(path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in arr:
            writer.writerow({fieldnames[0]: row})
            print(row)
    print('csv_write() done')


def csv_read(arr, path, fieldnames):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            arr.append(row[fieldnames[0]])
            print(row[fieldnames[0]])
        arr.pop(0)
        print(len(arr))
    print('csv_read() done')


def main(token, target_id):
    graph = facebook.GraphAPI(access_token=token, version='2.3')
    get_personal_id(graph, target_id, 'data/personal_id.csv', ['id'])
    csv_read(arr_personal_id, 'data/personal_id.csv', ['id'])
    get_personal_url('data/personal_url.csv', ['url'])
    csv_read(arr_personal_url, 'data/personal_url.csv', ['url'])
    print('main() done')


main(
    'EAACEdEose0cBAIolBHvWgb4srZBT0q4zUZBvGkXDL4O6GU1TGp0ulm6A10Q0bGjF7fZAlRjWI4IRnWThH0mtIuJx8spwv2vgmQ4YejKZCakrmLNZAo9k92v64Ofcm2TAWffU9XYHwZBAnnLCWCWb0xM5Oqa0waspAvXgbj5Y2ZCUZAKkqYX68y0k6XnWb0xSk0tKM3lsosFMZAgZDZD',
    '831259973706520')
