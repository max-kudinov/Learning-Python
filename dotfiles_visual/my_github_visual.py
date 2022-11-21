import requests
from plotly import offline

# Make an API call and store the response
url = "https://api.github.com/repos/max-kudinov/dotfiles/languages"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Create 2 lists for visualization
languages_dict = r.json()
languages_list, bytes_list = [], []
for language, bytes in languages_dict.items():
    languages_list.append(language)
    bytes_list.append(bytes)

# Visualize data
data = [
    {
        "type": "pie",
        "labels": languages_list,
        "values": bytes_list,
    }
]

my_layout = {
    "title": "Languages used in my dotfiles",
    "titlefont": {"size": 38},
    "title_x": 0.5,
}

fig = {"data": data, "layout": my_layout}
offline.plot(fig, filename="dotfiles_languages.html")
