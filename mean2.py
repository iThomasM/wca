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
    
def categorize_solves(solves, event):
    def subcategorize_solve(x, y, z):
        sub_x = {f'sub_{i}': 0 for i in range(x, y, z)}
        sub_x["above"] = 0
        sub_x["below"] = 0
        for i in solves:
            i = float(i) / 100
            for j in range(x, y, z):
                if i < j: #11.5 < 12 and 11.5 >= 11
                    if i >= j-z:
                        sub_x[f'sub_{j}'] += 1
                        print(f"{i} is sub-{j}")
                elif i >= x:
                    sub_x['above'] += 1
                    break
        return sub_x
    
    event_types = {'fast_events': ['222', '333', 'skewb', 'pyram'],
                    'medium_events': ['444', '333oh', 'sq1', '333bf', 'minx'],
                    'slow_events': ['666', '777']}
    
    for k, v in event_types.items():
        for i in v:
            if event == i and k == 'fast_events':
                out = subcategorize_solve(12, 3, -1)
                print(f"found category {k}")
                return out
            elif event == i and k == 'medium_events':
                out = subcategorize_solve(120, 10, -15)
                print(f"found category {k}")
                return out
            elif event == i and k == 'slow_events':
                out = subcategorize_solve(300, 90, -30)
                print(f"found category {k}")
                return out

def get_placements(person):
    wins = 0
    comp_count = 0
    for competition in person['competitionIds']:
        comp_count += 1
        try:
            comp_results = person['results'][competition]['333']
            result = [pos['position'] for pos in comp_results]
            if int(result[0]) == 1:
                wins += 1
        except KeyError:
            print(f'{competition} Placement not found')
            continue
    win_rate = (wins / comp_count) * 100
    return win_rate

def get_averages(person, event):
    averages = []
    for competition in person['competitionIds']:
        try:
            comp_results = person['results'][competition][event]
            average = [float(data['average']) / 100 for data in comp_results]
            averages.append(average)
        except KeyError:
            print(f'{competition} did not have 3x3')
            continue
    return averages

def pages(sub_x, mean, solves, podium, averages, person, event, wins):
    page = 1
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nHere's a list of {'x'.join(event)} results for {person["name"]}")
            if page == 1:
                display(1, sub_x)
            elif page == 2:
                display(2, sub_x, mean, solves, podium, averages, event, wins)

            if page == 1:
                page = int(input(f"Page {page} >> "))
            else:
                page = int(input(f"<< Page {page} >> "))

        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print('\nExiting')
            return

def display(n, sub_x=None, mean=None, solves=None, podium=None, averages=None, event=None, wins=None):
    if n == 1:
        table = []
        for x, y in sub_x.items():
            x = x.replace('_', ' ')
            table.append([x.title(), y])
        header = ["Solves Sub X", "Number of Solves"]
        print(tabulate(table, headers=header, tablefmt="fancy_grid"))
    elif n == 2:
        print("\n Mean of total WCA solves: " + str(mean) + "\n")
        print(f"\n Number of podiums: {podium}\n")
        print(f"\n Total {'x'.join(event)} Solves: {str(len(solves))}\n")  
        print(f"\n{averages}\n")
        print(f"Win rate: {round(wins)}%")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    inp = input("Enter WCA ID: ")

    if ' ' in inp:
        wca_id, event = inp.split(' ')
        event = event.replace('x', '')
    else:
        wca_id = inp
        event = '333'

    if len(wca_id) == 10:
        
        person = get_data(wca_id)
        solve_arr = solves(person, event)
        podium = get_podium(person)

        averages = get_averages(person, event)

        mean = calculate_mean(solve_arr)
        sub_x = categorize_solves(solve_arr, event)
        print(sub_x)
        wins = get_placements(person)

        #pages(sub_x, mean, solve_arr, podium, averages, person, event, wins)

    else:
        print("Invalid")

"""

Make the categorize_solves() different for different events
as its not possible for some events to have sub 4 for example 3bld
^^^ maybe it takes the mean of the solves and sets that as the middle ground and generates the rest based off that
    or maybe it takes the fastest and slowest solve for the user and generates it based off that
    but the problem is the chart would be different per person and not universal
"""

if __name__ == "__main__":
    main()