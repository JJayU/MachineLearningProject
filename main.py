import json
from pathlib import Path

filename = "junkiert_jakub.json"
results_file = Path(filename)


def main():
    print('Hi')

    results = {"first all-nba team": [], "second all-nba team": [], "third all-nba team": [],
               "first rookie all-nba team": [], "second rookie all-nba team": []}

    # Data processing here
    #
    # End of data processing

    with results_file.open('w') as output_file:
        json.dump(results, output_file, indent=4)


if __name__ == '__main__':
    main()
