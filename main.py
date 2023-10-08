# Importing libraries
from bot import run_api
from db_handler import add_following_users, get_members


# Main function
def main():
    add_following_users(get_members())
    run_api()


# Start program
if __name__ == '__main__':
    main()
