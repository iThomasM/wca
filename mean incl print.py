import requests
from tabulate import tabulate
import os

def get_data(wca_id):
    per = requests.get(f'https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{wca_id}.json')
    person = per.json()
    return person

def get_podium(person):
    podium = 0
    medals = person['medals']
    x = medals.values()
    for i in x:
        if i > 0:
            podium += i
    if podium == 0:
        return podium
    else:
        return podium - 1

def solves(person, event):
    solve_arr = []

    for competition in person['competitionIds']:
        try:
            comp_results = person['results'][competition][event]
            for result in comp_results:
                solves = result['solves']
                for solve in solves:
                    solve_arr.append(solve)
        except KeyError:
            print(f'{competition} did not have {event}')
            continue
    return solve_arr
    
def calculate_mean(solves):
    nums = [float(i) for i in solves]
    length = len(nums)
    total = sum(nums)
    out = total / length
    mean = round((out / 100), 2)
    return mean
    
def categorize_solves(solves):
    sub_x = {f'sub_{i}': 0 for i in range(12, 3, -1)}
    sub_x["above"] = 0

    for i in solves:
        i = float(i) / 100
        for j in range(12, 3, -1):
            if i < j and i >= j-1:
                sub_x[f'sub_{j}'] += 1
            elif i >= 12:
                sub_x['above'] += 1
                break
    return sub_x

def get_averages(person, event):
    averages = []
    for competition in person['competitionIds']:
        try:
            comp_results = person['results'][competition][event]
            average = [float(data['average']) / 100 for data in comp_results]
            averages.append(average)
        except Exception:
            print(f'{competition} did not have 3x3')
            continue
    return averages

def pages(sub_x, mean, solves, podium, averages, person, event):
    page = 1
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nHere's a list of {event} results for {person["name"]}")
            if page == 1:
                display(1, sub_x)
            elif page == 2:
                display(2, sub_x, mean, solves, podium, averages, event)

            if page == 1:
                page = int(input(f"Page {page} >> "))
            else:
                page = int(input(f"<< Page {page} >> "))

        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print('\nExiting')
            return

def display(n, sub_x=None, mean=None, solves=None, podium=None, averages=None, event=None):
    if n == 1:
        table = []
        for x, y in sub_x.items():
            table.append([x, y])
        header = ["Solves Sub X", "Number of Solves"]
        print(tabulate(table, headers=header, tablefmt="fancy_grid"))
    elif n == 2:
        print("\n Mean of total WCA solves: " + str(mean) + "\n")
        print(f"\n Number of podiums: {podium}\n")
        print(f"\n Total {event} Solves: {str(len(solves))}\n")  
        print(f"\n{averages}\n")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    wca_id, event = input("Enter ID: ").split(" ")
    event = event.replace('x', '')
    if len(wca_id) == 10:
        
        person = get_data(wca_id)
        solve_arr = solves(person, event)
        podium = get_podium(person)

        averages = get_averages(person, event)

        mean = calculate_mean(solve_arr)
        sub_x = categorize_solves(solve_arr)

        pages(sub_x, mean, solve_arr, podium, averages, person, event)

    else:
        print("Invalid")

if __name__ == "__main__":
    main()