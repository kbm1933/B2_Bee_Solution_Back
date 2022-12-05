import json

with open('solution.json', 'r') as f:
    ratings = json.load(f)
    
new_list = []
for rating in ratings:
    new_data = {"model":"article.Solution"}
    new_data["fields"]=rating
    new_list.append(new_data)

with open('sol_data.json','w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)