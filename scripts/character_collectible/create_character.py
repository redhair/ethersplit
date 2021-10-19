#!/usr/bin/python3
from brownie import ToKCharacter, accounts, config
from scripts.helpful_scripts import get_race, get_gender, fund_with_link
import time

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    character = ToKCharacter[len(ToKCharacter) - 1]
    fund_with_link(character.address)
    transaction = character.createCollectible("None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)

    requestId = transaction.events["requestedCollectible"]["requestId"]
    token_id = character.requestIdToTokenId(requestId)
    time.sleep(60)
    race = get_race(character.tokenIdToRace(token_id))
    gender = get_gender(character.tokenIdToGender(token_id))

    print("Character of tokenId {} is race: {} and gender: {}".format(token_id, race, gender))
