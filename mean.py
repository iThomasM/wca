import requests
from tabulate import tabulate
import csv


def get_data(wca_id):
    per = requests.get(f'https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{wca_id}.json')
    person = per.json()
    return person

def solves(person):
    #get comp ids
    solve_arr = []

    for competition in person['competitionIds']:
        try:
            comp_results = person['results'][competition]['333']
            for result in comp_results:
                solves = result['solves']
                for solve in solves:
                    solve_arr.append(solve)
        except Exception:
            print(f'{competition} did not have 3x3')
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
    sub_x = {f'sub_{i}': 0 for i in range(12, 4, -1)}
    sub_x["above"] = 0

    for i in solves:
        i = float(i) / 100
        for j in range(12, 4, -1):
            if i < j and i >= j-1:
                sub_x[f'sub_{j}'] += 1
            elif i >= 12:
                sub_x['above'] += 1
                break
    return sub_x

def print_res(sub_x, mean, solves):
    table = []
    for x, y in sub_x.items():
        table.append([x, y])
    header = ["Solves Sub X", "Number of Solves"]
    print(tabulate(table, headers=header, tablefmt="fancy_grid"))
    print("\n Mean of total WCA solves: " + str(mean) + "\n")
    print("Total 3x3 Solves: " + str(len(solves)))    

def main():
    wca_id = input("Enter ID: ")
    
    person = get_data(wca_id)
    solve_arr = solves(person)

    print(f"\nHere's a list of 3x3 results for {person["name"]}")

    mean = calculate_mean(solve_arr)
    sub_x = categorize_solves(solve_arr)
    print_res(sub_x, mean, solve_arr)

if __name__ == "__main__":
    main()