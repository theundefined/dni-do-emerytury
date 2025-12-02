# Dni do Emerytury

Narzędzie CLI (Command Line Interface) do obliczania pozostałych dni i godzin roboczych do emerytury. Program uwzględnia polskie święta oraz pozwala na konfigurowanie wieku emerytalnego.

## Funkcjonalności

- Oblicza dni i godziny robocze pozostałe do emerytury.
- Uwzględnia polskie święta państwowe (za pomocą biblioteki `holidays`).
- Konfigurowalny wiek emerytalny (domyślnie 60 dla kobiet, 65 dla mężczyzn).
- Zapisuje konfigurację (datę urodzenia, datę rozpoczęcia pracy, płeć, wiek emerytalny) w pliku `~/.config/dni-do-emerytury.yaml`.
- Opcja `--reconfigure` do łatwej zmiany ustawień.

## Instalacja

Możesz zainstalować `dni-do-emerytury` za pomocą `pipx` (zalecane dla narzędzi CLI):

```bash
pipx install dni-do-emerytury
```

Jeśli nie masz `pipx`, możesz zainstalować go za pomocą `pip`:

```bash
pip install pipx
pipx ensurepath
pipx install dni-do-emerytury
```

## Użycie

Po zainstalowaniu, uruchom program wpisując:

```bash
dni-do-emerytury
```

Przy pierwszym uruchomieniu zostaniesz poproszony o podanie daty urodzenia, daty rozpoczęcia pracy, płci oraz docelowego wieku emerytalnego. Dane te zostaną zapisane w pliku `~/.config/dni-do-emerytury.yaml`.

### Ponowna konfiguracja

Aby zmienić ustawienia, użyj flagi `--reconfigure`:

```bash
dni-do-emerytury --reconfigure
```

Program wyświetli aktualne wartości jako domyślne, a Ty możesz je zaakceptować (wciskając `Enter`) lub wprowadzić nowe.

## Rozwój

Projekt jest dostępny na GitHubie: [https://github.com/theundefined/dni-do-emerytury](https://github.com/theundefined/dni-do-emerytury)

## Licencja

Ten projekt jest udostępniany na licencji MIT. Zobacz plik [LICENSE](LICENSE) po więcej szczegółów.

## Uwaga

Ten program został stworzony z dużą pomocą sztucznej inteligencji Gemini. Chociaż dołożono wszelkich starań, aby zapewnić jego poprawność, zawsze zachowaj ostrożność i zweryfikuj wyniki, zwłaszcza w kwestiach finansowych lub prawnych. Używasz go na własne ryzyko.