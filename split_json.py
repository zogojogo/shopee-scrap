import json
from tqdm import tqdm

with open('users.json', 'r') as f:
    data = json.load(f)

chunk_size = 500000
chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

for i, chunk in enumerate(tqdm(chunks)):
    with open(f'users/users_{i}.json', 'w') as f:
        json.dump(chunk, f, indent=4)