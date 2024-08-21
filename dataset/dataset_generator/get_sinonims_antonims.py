import fasttext
from collections import defaultdict
from tqdm import tqdm
import time
import requests
import json

ft = fasttext.load_model("../../cc.id.300.bin")
words = [word.lower() for word in ft.get_words()]

seen = defaultdict(set)

antonims: list[list[str]] = []
sinonims: list[list[str]] = []

for word in tqdm(words):
    time.sleep(0.5)
    if len(antonims) == 1587:
        break
    try:
        url = f"http://kateglo.lostfocus.org/api.php?format=json&phrase={word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                sinonim: dict[str, str] = data["kateglo"]["relation"]["s"]
                for key in sinonim.keys():
                    if key.isdigit():
                        word2 = sinonim[key]["related_phrase"].lower()
                        if word not in seen[word2] and word2 not in seen[word]:
                            sinonims.append([word, word2])
                            seen[word2].add(word)
                            seen[word].add(word2)
            except KeyError:
                pass
            try:
                antonim: dict[str, str] = data["kateglo"]["relation"]["a"]
                for key in antonim.keys():
                    if key.isdigit():
                        word2 = antonim[key]["related_phrase"].lower()
                        if word not in seen[word2] and word2 not in seen[word]:
                            antonims.append([word, word2])
                            seen[word2].add(word)
                            seen[word].add(word2)
            except KeyError:
                pass
    except:
        continue

    with open("antonims.json", "w") as f:
        json.dump(antonims, f, indent=4)
    with open("sinonims.json", "w") as f:
        json.dump(sinonims, f, indent=4)
