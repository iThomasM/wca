import requests
from tabulate import tabulate
import os
import termplotlib as tpl

def get_data(wca_id):
    per = requests.get(f'https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{wca_id}.json')
    person = per.json()
    return person

def solves(person, event):
    solve_arr = []

    for competition in person['competitionIds']:
        try:
            comp_results = person['results'][competition][event]
            for result in comp_results:
                solves = result['solves']
                for solve in solves:
                    if int(solve) > 0:
                        solve_arr.append(solve)
        except KeyError:
            print(f'{competition} did not have {event}')
            continue
    return solve_arr

def convert(time): 
    mins = 0
    seconds = time
    while time > 59:
        if time >= 60: 
            if seconds - 60 < 0: 
                break
            else:
                seconds -= 60 
            mins += 1 
    if mins == 0:
        return time
    return f"{mins}:{"%02d" % seconds}"

def calculate_mean(solves):
    nums = [float(i) for i in solves]
    length = len(nums)
    total = sum(nums)
    out = total / length
    mean = round((out / 100), 2)
    if mean > 60:
        mean = convert(mean)
    return mean
    
def categorize_solves(solves, event):
    
    event_types = {'extreme_events': ['222'],
                    'fast_events': ['333', 'skewb', 'pyram'],
                    'medium_events': ['555', '444', '333oh', 'sq1', '333bf', 'minx'],
                    'slow_events': ['666', '777']}
    
    for k, v in event_types.items():
        for i in v: 
            if event == i and k == 'extreme_events':
                x, y, z = 12, 0, -1
            if event == i and k == 'fast_events':
                x, y, z = 12, 3, -1
            elif event == i and k == 'medium_events':
                x, y, z = 180, 10, -15
            elif event == i and k == 'slow_events':
                x, y, z = 300, 90, -30
     
    sub_x = {f'sub_{convert(i)}': 0 for i in range(x, y, z)}
    sub_x["above"] = 0
    sub_x["below"] = 0
    for i in solves:
        i = float(i) / 100
        for j in range(x, y, z):
            if i < j and i >= j+z:
                sub_x[f'sub_{convert(j)}'] += 1
            elif i >= x:
                sub_x['above'] += 1
                break
    return sub_x

def get_placements(person, event):
    wins = 0
    podiums = 0
    comp_count = 0
    for competition in person['competitionIds']:
        comp_count += 1
        try:
            comp_results = person['results'][competition][event]
            result = [pos['position'] for pos in comp_results]
            if int(result[0]) == 1:
                wins += 1
            if int(result[0]) <= 3:
                podiums += 1
        except KeyError:
            print(f'{competition} Placement not found')
            continue
    win_rate = (wins / comp_count) * 100
    return win_rate, podiums, wins

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

def pages(sub_x, mean, solves, averages, person, event, win_rate, podiums, wins):
    page = 1
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nHere's a list of {'x'.join(event)} results for {person["name"]}")
            if page == 1:
                display(1, sub_x)
            elif page == 2:
                display(2, sub_x, mean, solves, averages, event, win_rate, podiums, wins)
            elif page == 3:
                display(3)
            if page == 1:
                page = int(input(f"Page {page} >> "))
            else:
                page = int(input(f"<< Page {page} >> "))

        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print('\nExiting')
            return

def display(n, sub_x=None, mean=None, solves=None, averages=None, event=None, win_rate=None, podiums=None, wins=None):
    if n == 1:
        table = []
        for x, y in sub_x.items():
            x = x.replace('_', ' ')
            table.append([x.title(), y])
        header = ["Solves Sub X", "Number of Solves"]
        print(tabulate(table, headers=header, tablefmt="fancy_grid"))
    elif n == 2:
        try:
            print(f"\n Mean of total WCA solves: {mean}\n" )
        except:
            print(f"\n Mean of total WCA solves: {mean}\n" )
        print(f"\n Number of podiums: {podiums}\n")
        print(f"\n Total {'x'.join(event)} Solves: {str(len(solves))}\n")  
        print(f"\nWin count: {wins}\n")
        print(f"\nWin rate: {round(win_rate, 1)}%\n")
    elif n == 3:
        print("WIP")

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
        solve_arr =  solves(person, event)

        averages = get_averages(person, event)

        mean = calculate_mean(solve_arr)
        sub_x = categorize_solves(solve_arr, event)
        win_rate, podiums, wins = get_placements(person, event)

        pages(sub_x, mean, solve_arr, averages, person, event, win_rate, podiums, wins)

    else:
        print("Invalid")

if __name__ == "__main__":
    main()