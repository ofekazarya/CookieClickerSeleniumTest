from TimeUtils import timer
from CookieClickerInfra import CookieDriverHandler


def main():
    with CookieDriverHandler() as cdh:
        cdh.change_bakery_name("selenium")
        try:
            while True:
                for _ in timer(20):
                    cdh.click_cookie()
                cdh.spend_all_money()

        except KeyboardInterrupt:
            print("User stopped the program, press Enter to quit")


if __name__ == "__main__":
    main()
