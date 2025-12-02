import datetime
import argparse
from pathlib import Path
import yaml
import holidays
from dateutil.relativedelta import relativedelta

CONFIG_DIR = Path.home() / ".config"
CONFIG_FILE = CONFIG_DIR / "dni-do-emerytury.yaml"
RETIREMENT_AGE_M = 65
RETIREMENT_AGE_W = 60
HOURS_PER_WORK_DAY = 8

def get_config(force_reconfigure=False):
    """
    Reads or creates and returns the configuration.
    If force_reconfigure is True, it prompts the user for all values,
    suggesting the current values as defaults.
    """
    existing_config = {}
    if CONFIG_FILE.is_file():
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            existing_config = yaml.safe_load(f) or {}

    if not force_reconfigure and existing_config:
        return existing_config

    print("Proszę podać dane konfiguracyjne. Wciśnij Enter, aby zaakceptować domyślną wartość w nawiasach.")
    CONFIG_DIR.mkdir(exist_ok=True)
    
    while True:
        try:
            default = existing_config.get('birth_date', '')
            prompt = f"Podaj datę urodzenia (YYYY-MM-DD) [{default}]: "
            birth_date_str = input(prompt) or default
            datetime.datetime.strptime(birth_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Niepoprawny format daty. Proszę użyć YYYY-MM-DD.")
    
    while True:
        try:
            default = existing_config.get('work_start_date', '')
            prompt = f"Podaj datę rozpoczęcia pracy (YYYY-MM-DD) [{default}]: "
            work_start_date_str = input(prompt) or default
            datetime.datetime.strptime(work_start_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Niepoprawny format daty. Proszę użyć YYYY-MM-DD.")

    while True:
        default = existing_config.get('gender', 'M')
        prompt = f"Podaj płeć (M/K) [{default}]: "
        gender = (input(prompt) or default).upper()
        if gender in ["M", "K"]:
            break
        else:
            print("Niepoprawna płeć. Proszę wpisać M lub K.")

    default_age = existing_config.get('retirement_age', RETIREMENT_AGE_M if gender == 'M' else RETIREMENT_AGE_W)
    while True:
        try:
            prompt = f"Podaj docelowy wiek emerytalny [{default_age}]: "
            age_str = input(prompt) or str(default_age)
            retirement_age = int(age_str)
            if retirement_age > 0:
                break
            else:
                print("Wiek musi być liczbą dodatnią.")
        except ValueError:
            print("Niepoprawna wartość. Wpisz liczbę całkowitą.")

    config = {
        "birth_date": birth_date_str,
        "work_start_date": work_start_date_str,
        "gender": gender,
        "retirement_age": retirement_age
    }

    with open(CONFIG_FILE, "w", encoding='utf-8') as f:
        yaml.dump(config, f)
    
    print(f"Konfiguracja zapisana w {CONFIG_FILE}")
    return config

def calculate_working_days(start_date, end_date):
    """
    Calculates the number of working days between two dates,
    excluding weekends and Polish public holidays.
    """
    if start_date > end_date:
        return 0
        
    pl_holidays = holidays.PL()
    working_days = 0
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() < 5 and current_date not in pl_holidays:
            working_days += 1
        current_date += datetime.timedelta(days=1)
        
    return working_days

def main():
    """Main function of the application."""
    parser = argparse.ArgumentParser(description="Oblicz dni do emerytury.")
    parser.add_argument(
        '--reconfigure',
        action='store_true',
        help='Uruchom ponowną konfigurację programu.'
    )
    args = parser.parse_args()

    try:
        config = get_config(force_reconfigure=args.reconfigure)
        
        birth_date = datetime.datetime.strptime(config["birth_date"], "%Y-%m-%d").date()
        work_start_date = datetime.datetime.strptime(config["work_start_date"], "%Y-%m-%d").date()
        gender = config["gender"]

        # Use configured retirement age, with fallback for old configs
        default_statutory_age = RETIREMENT_AGE_M if gender == 'M' else RETIREMENT_AGE_W
        retirement_age = config.get("retirement_age", default_statutory_age)
        
        retirement_date = birth_date + relativedelta(years=retirement_age)
        
        today = datetime.date.today()

        if today >= retirement_date:
            print("Gratulacje, jesteś już na emeryturze!")
            return

        # Replicating shell script logic with precise datetime objects
        days_to_retirement = (retirement_date - today).days
        years_to_retirement = days_to_retirement / 365.25  # More accurate than 365

        days_worked = (today - work_start_date).days
        years_worked = days_worked / 365.25
        
        total_work_period_days = (retirement_date - work_start_date).days
        work_percentage = (days_worked / total_work_period_days) * 100 if total_work_period_days > 0 else 0

        age_in_days = (today - birth_date).days
        life_work_percentage = (days_worked / age_in_days) * 100 if age_in_days > 0 else 0

        # New feature: calculating remaining working days
        working_days_left = calculate_working_days(today, retirement_date)
        working_hours_left = working_days_left * HOURS_PER_WORK_DAY
        
        # --- Output ---
        print("\n--- Podsumowanie Twojej drogi do emerytury ---")
        print(f"Data Twojej emerytury: {retirement_date.strftime('%Y-%m-%d')}")
        print(f"\nPozostało {days_to_retirement} dni ({years_to_retirement:.2f} lat(a)) do emerytury.")
        print(f"W tym {working_days_left} dni roboczych ({working_hours_left:,} godzin roboczych).")
        
        print(f"\nPracujesz już {days_worked} dni ({years_worked:.2f} lat(a)).")
        print(f"Ukończono {work_percentage:.2f}% planowanego okresu pracy.")
        print(f"Praca stanowi {life_work_percentage:.2f}% Twojego dotychczasowego życia.")

    except (TypeError, KeyError, AttributeError) as e:
        print(f"Błąd w pliku konfiguracyjnym: {e}. Uruchom program z flagą --reconfigure, aby go naprawić.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    main()