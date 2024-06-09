import json

# Script used to check the results of the model
# Copyright: Jakub Junkiert 2024
def check_results():

    # Open the files with the results and with actual correct results
    results_file = open("junkiert_jakub.json")
    correct_file = open("correct_results.json")

    results = json.load(results_file)
    correct = json.load(correct_file)

    points = 0
    correct_fives = [0, 0, 0, 0, 0]

    for i in results["first all-nba team"]:
        if i in correct["first all-nba team"]:
            points += 10
            correct_fives[0] += 1
        elif i in correct["second all-nba team"]:
            points += 8
        elif i in correct["third all-nba team"]:
            points += 6
    for i in results["second all-nba team"]:
        if i in correct["second all-nba team"]:
            points += 10
            correct_fives[1] += 1
        elif i in correct["first all-nba team"]:
            points += 8
        elif i in correct["third all-nba team"]:
            points += 8
    for i in results["third all-nba team"]:
        if i in correct["third all-nba team"]:
            points += 10
            correct_fives[2] += 1
        elif i in correct["second all-nba team"]:
            points += 8
        elif i in correct["first all-nba team"]:
            points += 6
    for i in results["first rookie all-nba team"]:
        if i in correct["first rookie all-nba team"]:
            points += 10
            correct_fives[3] += 1
        elif i in correct["second rookie all-nba team"]:
            points += 8
    for i in results["second rookie all-nba team"]:
        if i in correct["second rookie all-nba team"]:
            points += 10
            correct_fives[4] += 1
        elif i in correct["first rookie all-nba team"]:
            points += 8

    for i in correct_fives:
        if i == 5:
            points += 40
        elif i == 4:
            points += 20
        elif i == 3:
            points += 10
        elif i == 2:
            points += 5

    print("Printing the results:")
    print("\nOthers: " + str(correct_fives[0] + correct_fives[1] + correct_fives[2]) + " / 15")
    print("Rookies: " + str(correct_fives[3] + correct_fives[4]) + " / 10")

    print("Points: " + str(points))


if __name__ == "__main__":
    check_results()


