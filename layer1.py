import facebook
import requests
import csv

arr_client_id = []
arr_client_url = []
arr_client_data = []


def video_like(graph, video_id):
    video = graph.get_object(
        id=video_id,
        fields='likes', )
    for row in video['likes']['data']:
        row = row['id']
        arr_client_id.append(row)
        print(row)
    try:
        next_page_url = video['likes']['paging']['next']
    except:
        print('<= 25')

    while True:
        try:
            next_page = requests.get(next_page_url).json()
            for row in next_page['data']:
                row = row['id']
                arr_client_id.append(row)
                print(row)

            next_page_url = next_page['paging']['next']
        except:
            print('video_like() done')
            break


def video_comment(graph, video_id):
    video = graph.get_object(
        id=video_id,
        fields='comments', )
    for row in video['comments']['data']:
        row = row['from']['id']
        arr_client_id.append(row)
        print(row)
    try:
        next_page_url = video['comments']['paging']['next']
    except:
        print('client_id <= 25')

    while True:
        try:
            next_page = requests.get(next_page_url).json()
            for row in next_page['data']:
                row = row['from']['id']
                arr_client_id.append(row)
                print(row)

            next_page_url = next_page['paging']['next']
        except:
            print('video_comment() done')
            break


def get_client_id(graph, video_id):
    try:
        video_like(graph, video_id)
    except:
        pass
    try:
        video_comment(graph, video_id)
    except:
        pass
    print('get_client_id() done')

def get_client_url(graph):
    for row in arr_client_id:
        try:
            client_url = graph.get_object(
                id=row, )
            arr_client_url.append(client_url['link'])
            print(client_url['link'])
        except:
            pass
    print('get_client_url() done')

def csv_write(arr, path, fieldnames):
    with open(path, 'w') as csvfile:
        fieldnames = [fieldnames]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in arr:
            writer.writerow({fieldnames[0]: row})
            print(row)
        print('csv_write() done')

def csv_read(path, fieldnames):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            arr_client_id.append(row[fieldnames])
            print(row[fieldnames])
        print('csv_read() done')

def main(token, video_id):
    graph = facebook.GraphAPI(access_token=token, version='2.3')
    get_client_id(graph, video_id)
    csv_write(arr_client_id, 'data/client_id.csv', 'client_id')
    csv_read('data/client_id.csv', 'client_id')
    get_client_url(graph)
    csv_write(arr_client_url, 'data/client_url.csv', 'client_url')
    print(len(arr_client_url))
    print(len(arr_client_id))
    print('main() done')


main(
    'EAACEdEose0cBANBtmd371nZCHF0HiC2d94ZA8A9sDUE17zWUme8eOPwMHNZCWwkIkQMuFUcowjAzk3AwZAd04ztBn7OaBBrbXVkZA1J8XViooapXPwiB0oZAqPRD2MQv7JCjUwZAhOMVriLADFKpyyQ9CvjsTg2jObuiCNCnGRIM8G6rBYVPLH6C11sZBScZCl5eC4C28Ret0gtAFUPYETem3',
    '931722383530905')
