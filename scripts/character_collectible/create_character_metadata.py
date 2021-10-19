#!/usr/bin/python3
import os
import requests
import json
from brownie import ToKCharacter, network
from metadata import sample_character_metadata
from scripts.helpful_scripts import get_race, get_gender
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

race_to_image_uri = {
    "HUMAN": "https://ipfs.io/ipfs/QmTfVYj2JRfKkZV6gA99tfzaHdhm27FcGxwzuSnXoi1mmm?filename=human.png",
    "ELF": "https://ipfs.io/ipfs/QmYGD2cR1hFoXxqfhbkSdV4cXZh8SC22fdsJ8PNHVQGbG4?filename=elf.png",
    "DWARF": "https://ipfs.io/ipfs/QmUMTJhW2ezy9PHt99W9yyQSVPxbBTm3AjYy17w4XBXyqd?filename=dwarf.png",
    "HALFLING": "https://ipfs.io/ipfs/QmZpMTjhY2MmbV5vV4QZLNPnLsZqSA73po7dEjoxsNCawp?filename=halfling.jpeg",
    "HALFORC": "https://ipfs.io/ipfs/QmeBHxAQBnYWMxjwsyZeWkyvRGgSHKypNJGxxJiBXWfnVz?filename=orc.png",
}


def main():
    print("Working on " + network.show_active())
    character = ToKCharacter[len(ToKCharacter) - 1]
    number_of_advanced_collectibles = character.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
    )
    write_metadata(number_of_advanced_collectibles, character)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = sample_character_metadata.metadata_template
        race = get_race(nft_contract.tokenIdToRace(token_id))
        metadata_file_name = (
            "./metadata/{}/characters/".format(network.show_active())
            + str(token_id)
            + "_"
            + race
            + ".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(
                    metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["race"] = get_race(
                nft_contract.tokenIdToRace(token_id)
            )
            collectible_metadata["name"] = get_race(
                nft_contract.tokenIdToRace(token_id)
            )
            collectible_metadata["description"] = "A {} warrior of the {} race".format(
                collectible_metadata["gender"], collectible_metadata["race"]
            )
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    race.lower().replace('_', '-'))
                image_to_upload = upload_to_ipfs(image_path)
            image_to_upload = (
                race_to_image_uri[race] if not image_to_upload else image_to_upload
            )
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri
