import requests
import json
import argparse
import configparser
import random as rnd
from models import Endpoint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", action='store_true', default=False, help="Run script with predefined requests.")
    parser.add_argument("-b", "--balance", action='store_true', default=False, help="Print balance on all servers.")
    parser.add_argument("-c", "--credit", required=False, type=int, help="Perform CREDIT operation.")
    parser.add_argument("-d", "--debit", required=False, type=int, help="Perform DEBIT operation.")
    parser.add_argument("-t", "--times", required=False, type=int, help="The number of repetitions.")
    args = parser.parse_args()

    sequencer, _, banks = load_endpoints()

    if args.auto is not False:
        if args.times is not None:
            run_automatic(args.times, sequencer.host, sequencer.port, sequencer.route)
        else:
            parser.error("Expected argument -t/--times for number of repetitions.")
    elif args.balance is not False:
        balance(banks)
    elif args.debit is not None:
        debit(args.debit, sequencer.host, sequencer.port, sequencer.route)
    elif args.credit is not None:
        credit(args.credit, sequencer.host, sequencer.port, sequencer.route)
    else:
        parser.print_help()


def load_endpoints():
    config = configparser.ConfigParser()
    config.read('../endpoints.cfg')

    port = config['DEFAULT']['port']

    host = config['sequencer']['host']
    route = config['sequencer']['route']
    sequencer = Endpoint(host, port, route)

    host = config['shuffler']['host']
    route = config['shuffler']['route']
    shuffler = Endpoint(host, port, route)

    banks = []
    hosts = config['bank_server']['host'].split('\n')
    routes = config['bank_server']['route'].split('\n')
    for host in hosts:
        banks.append(Endpoint(host, port, routes))

    return sequencer, shuffler, banks


def run_automatic(repetitions, host, port, route):
    for i in range(repetitions):
        current_amount = rnd.randint(10000, 50000)
        if rnd.random() < 0.5:
            credit(current_amount, host, port, route)
        else:
            debit(current_amount, host, port, route)


def credit(amount, host, port, route):
    r = requests.post("http://{0}:{1}{2}".format(host, port, route), json={
            "amount": amount,
            "operation": "CREDIT"
    })
    print("Credit response:")
    print(json.dumps(r.json(), indent=4, sort_keys=True))


def debit(amount, host, port, route):
    r = requests.post("http://{0}:{1}{2}".format(host, port, route), json={
            "amount": amount,
            "operation": "DEBIT"
    })
    print("Debit response:")
    print(json.dumps(r.json(), indent=4, sort_keys=True))


def balance(endpoints):
    for endpoint in endpoints:
        r = requests.get("http://{0}:{1}{2}".format(endpoint.host, endpoint.port, endpoint.route[0]))
        print("Balance on server {0}:{1}:".format(endpoint.host, endpoint.port))
        print(json.dumps(r.json(), indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
