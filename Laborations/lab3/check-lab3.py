#!/usr/bin/env python

import json
import re
import requests


HOST="localhost"
PORT=7007


def url(resource):
    return f"http://{HOST}:{PORT}{resource}"


def response_to_dicts(r):
    return (dict(d) for d in r.json()['data'])


def abort(msg):
    print(f"Error: {msg}")
    exit(1)


def check_ping():
    try:
        resource = url('/ping')
        r = requests.get(resource)
        if r.text.strip() == 'pong':
            print("ping OK")
        else:
            print("Your server seems to be running, but does not return pong on /ping")
    except:
        abort(f'curl -X GET {resource} does not return pong -- is your server running?')


def check_reset():
    resource = url('/reset')
    r = requests.post(resource)
    if r.text.strip() == 'OK':
        print("reset OK")
    else:
        abort(f'curl -X POST {resource} does not return OK')
        

def check_all_movies():
    try:
        r = requests.get(url('/movies'))
        found = response_to_dicts(r)
        print("======== Found movies ========")
        for d in found:
            title = d['title']
            year = d['year']
            print(f"{title} ({year})")
            print("==============================")
    except Exception as e:
        abort(f"curl -X GET {url('/movies')} does not work: {e}")


def check_movie_title(title, year):
    resource = url(f'/movies?title={title}&year={year}')
    try:
        r = requests.get(resource)
        found = list(response_to_dicts(r))
        if len(found) != 1:
            abort(f"curl -X GET {resource} returns {len(found)} movies (should have been 1)")
        for d in found:
            assert d['title'] == title
            assert d['year'] == year
            print(f"Could get {title} ({year}) using title and year")
    except Exception as e:
        abort(f"curl -X GET {resource} does not work: {e}")


def check_movie_imdb(imdb_key):
    resource = url(f'/movies/{imdb_key}')
    try:
        r = requests.get(resource)
        found = list(response_to_dicts(r))
        if len(found) != 1:
            abort(f"{resource} returns {len(found)} movies (should have been 1)")
        for d in found:
            title = d['title']
            year = d['year']
            print(f"Could get {title} ({year}) using imdb-key")
    except Exception as e:
        abort(f"curl -X GET {resource} does not work: {e}")


def add_performances(imdb, theaters, dates):
    print("======== Adding performances ========")
    for theater in theaters:
        for date in dates:
            resource = url(f'/performances?imdb={imdb}&theater={theater}&date={date}&time=19:30')
            try:
                r = requests.post(resource)
                m = re.search('/performances/(.+)', r.text.strip())
                if m:
                    print(f"{imdb} at {theater} on {date}: {m.group(1)}")
            except Exception as e:
                abort(f"curl -X POST {url} does not work: {e}")
                print("-------------------------------------")
                print("See performances at:")
                print(f"curl -GET {url('/performances')}")
                print("=====================================")


def buy_tickets(user_id):
    print("======== Buying tickets ========")
    try:
        for _ in range(2):
            resource = url('/performances')
            r = requests.get(resource)
            performance = next(p for p in response_to_dicts(r) if p['theater'] == 'Kino' and p['remainingSeats'] > 0)
            perf_id = performance['performanceId']
            seats_left = performance['remainingSeats']
            print("================================")
            print(f"Buying tickets to {performance['title']} on {performance['date']}")
            buy_url = url(f'/tickets?user={user_id}&performance={perf_id}&pwd=dobido')
            print("--------------------------------")
            print(f"curl -X POST {buy_url}")
            print("--------------------------------")
            for _ in range(seats_left):
                r = requests.post(buy_url)
                print(r.text)
                m = re.search('/tickets/(.+)', r.text.strip())
                if not m:
                    abort('Got no ticket when trying to buy available seat')
                    # now fail once:
            r = requests.post(buy_url)
            if not r.text.strip() == "No tickets left":
                abort("Could buy too many tickets")
                print("================================")
    except Exception as e:
        abort(f'Got error when trying to buy tickets: {e}')


def see_tickets(user_id):
    try:
        resource = url(f'/customers/{user_id}/tickets')
        print(f"curl -X GET {resource}")
        r = requests.get(resource)
        print(r.text)
    except Exception as e:
        abort(f"Could not see the tickets bought by {user_id}: {e}")


def main():
    check_ping()
    check_reset()
    check_all_movies()
    check_movie_title("Spotlight", 2015)
    check_movie_imdb("tt5580390")
    add_performances(
        'tt5580390',
        ['Kino', 'Skandia'],
        ['2019-02-22', '2019-02-23']
    )
    add_performances(
        'tt2562232',
        ['Kino', 'Skandia'],
        ['2019-02-24', '2019-02-25']
    )
    buy_tickets('alice')
    see_tickets('alice')
    print("=========================")
    print("I found no obvious errors")
    print("=========================")


if __name__ == '__main__':
    main()
