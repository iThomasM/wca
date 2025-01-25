import requests
#get NR avg from each country and rank them
country = requests.get('https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/countries.json')
countries = country.json()
new_ranks = {}

for c in countries["items"]:
    print('.')
    try:
        rank = requests.get(f'https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/rank/{c["iso2Code"]}/average/333.json')
        ranks = rank.json()

        wr = ranks["items"][0]["best"]
        new_ranks[c["name"]] = wr
    except Exception as e:
        continue

sorted_ranks = {k: v for k, v in sorted(new_ranks.items(), key=lambda item: item[1])}

count = 1
for k in sorted_ranks:
    t = sorted_ranks.get(k)
    print(f"{count}) {k}: {float(t) / 100}")
    with open("ranks.txt", "a") as file:
        file.write(f"{count}) {k}: {float(t) / 100}\n")
    count += 1