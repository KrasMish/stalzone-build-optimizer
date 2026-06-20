name = "Firefly"
rarity = "Epic"
def artifact-info(name, rarity) -> str:
    return f"{name} ({rarity})"

artifacts = [
    "Firefly",
    "Atom",
    "Spiral",
    "Goldfish"
]

for artifact in artifacts:
    print(artifact)


artifact = {
    "name": "Firefly",
    "healing": 8,
    "speed": 3
}

print(f"{artifact['name']} gives {artifact['healing']} healing")

def is_good_artifact(healing):
    if healing > 5:
        return True
    else:
        return False