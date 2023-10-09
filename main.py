# Importing libraries
from bot import run_api
from db_handler import add_following_users, get_members
from background import keep_alive


# Main function
def main():
    add_following_users(get_members())
    run_api()


# Start program
if __name__ == '__main__':
    keep_alive()
    main()
