#!/usr/bin/python3
from brownie import ToKCharacter, accounts, network, config
from metadata import sample_character_metadata
from scripts.helpful_scripts import get_race, get_gender, OPENSEA_FORMAT


# cereate urls.json in metadata folder that keeps track of each metadata url created for each particular nft
char_metadata_dic = {
    "MALE_DWARF": "https://ipfs.io/ipfs/QmUT5DmqLXsyTSdWviZUAa8k2bQGjRaeRxUkjm9esaqzVe?filename=0-MALE_DWARF.json",
    "FEMALE_DWARF": "https://ipfs.io/ipfs/QmNa5RHD7xBWBaY3qZpcA9tcS27cm1M6YaeNLsZDrSZAez?filename=1-FEMALE_DWARF.json",
    "MALE_ELF": "https://ipfs.io/ipfs/QmRNxakoFUNgA1neggxJDrriVLToAYSE9dVcPJ7G3oVngw?filename=2-MALE_ELF.json",
    "MALE_HUMAN": "https://ipfs.io/ipfs/QmcbgXHugqdocKLBZq1nqgS2PCnh1S99w4iWNGBFvZj2Ym?filename=3-MALE_HUMAN.json"
}

def main():
    print("Working on " + network.show_active())
    character = ToKCharacter[len(ToKCharacter) - 1]
    number_of_characters = character.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_characters)
    )
    for token_id in range(number_of_characters):
        race = get_race(character.tokenIdToRace(token_id))
        gender = get_gender(character.tokenIdToGender(token_id))
        if not character.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, character,
                         char_metadata_dic[gender+"_"+race])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
