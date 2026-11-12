
from country import get_country_info


def main():

    print("=" * 40)
    print("   COUNTRY INFORMATION SYSTEM")
    print("=" * 40)

    country = input("Enter country name: ")

    try:

        result = get_country_info(country)

        print("\n===== COUNTRY INFORMATION =====")

        for key, value in result.items():
            print(f"{key:<12}: {value}")

        print("=" * 40)

    except ValueError as e:
        print("Input Error:", e)

    except LookupError as e:
        print("Search Error:", e)

    except RuntimeError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
