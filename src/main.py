import json

def load_usernames(filename: str, key: str) -> set:
    """Load Instagram usernames from JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        accounts = data.get(key, [])
        usernames = {entry["string_list_data"][0]["value"] for entry in accounts}
    return usernames

def main():
    # Ganti path jika file-nya berbeda
    followers_file = 'data/followers.json'
    following_file = 'data/following.json'

    followers = load_usernames(followers_file, 'relationships_followers')
    following = load_usernames(following_file, 'relationships_following')

    not_following_back = following - followers

    print(f"\nKamu mengikuti {len(following)} akun.")
    print(f"{len(not_following_back)} akun tidak follow kamu balik:\n")
    for username in sorted(not_following_back):
        print(f"• {username}")

if __name__ == "__main__":
    main()
