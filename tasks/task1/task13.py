import json

def solution(data):
    nodes = {item["id"]:item for item in data}

    result = []

    for i in data:
        i["child"] = []

    for item in data:
        if item["parentId"] == 0 or item["parentId"] == None:
            result.append(item)
        else:
            parent_id = item["parentId"]
            parent = nodes.get(parent_id)
            if parent:
                parent['child'].append(item)
    
    return result

data = [{
  "id": 1,
  "parentId": 0
}, {
  "id": 2,
  "parentId": 0
}, {
  "id": 3,
  "parentId": 1
}, {
  "id": 4,
  "parentId": 1
}, {
  "id": 5,
  "parentId": 2
}, {
  "id": 6,
  "parentId": 4
}, {
  "id": 7,
  "parentId": 5
}]

result = solution(data)
print(json.dumps(result, indent=1))