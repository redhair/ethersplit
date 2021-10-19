#!/usr/bin/python3
from brownie import StarterPack, accounts, config
from scripts.helpful_scripts import fund_with_link
import time

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    starterpack = StarterPack[len(StarterPack) - 1]
    fund_with_link(starterpack.address)
    transaction = starterpack.createCollectible("None", {"from": dev})
    # print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)

    # requestId = transaction.events["requestedCollectible"]["requestId"]
    # token_id = starterpack.requestIdToTokenId(requestId)
    # time.sleep(60)

