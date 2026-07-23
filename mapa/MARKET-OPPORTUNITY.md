# Ocena potrzeby rynkowej aplikacji do analizy i planowania działek

Data oceny: 19 lipca 2026 r.

## Wniosek

**Potrzeba rynkowa istnieje, ale nie na „kolejną mapę działek”.** Produkt miałby znacznie większy sens jako **cyfrowa teczka działki — osobisty warsztat do sprawdzania, planowania i monitorowania nieruchomości**.

Wstępna ocena:

- potrzeba rynkowa: **7/10**;
- obecna aplikacja jako produkt gotowy do sprzedaży: **3/10**;
- potencjał po właściwym ukierunkowaniu: **8/10**.

Obecna aplikacja rozwiązuje realny problem konkretnego terenu, ale przed komercjalizacją wymaga automatyzacji tworzenia nowych projektów, dodania interpretacji danych oraz znalezienia wyraźnego powodu, aby użytkownik wracał do niej po pierwszym sprawdzeniu działki.

## Dlaczego rynek istnieje

Kupujący i właściciel działki muszą dziś składać informacje z wielu miejsc:

- Geoportalu;
- BIP-u gminy;
- miejscowego planu zagospodarowania przestrzennego;
- planu ogólnego lub jego projektu;
- map uzbrojenia i budynków;
- map zagrożeń i ograniczeń;
- własnych dokumentów, pomiarów i koncepcji.

Reforma planowania zwiększa niepewność właścicieli i inwestorów. Aktualny termin zastąpienia studiów planami ogólnymi to 31 sierpnia 2026 r., a po tej dacie zmieniają się zasady dotyczące wydawania decyzji o warunkach zabudowy.

Jednocześnie plany ogólne są tworzone jako ustandaryzowane dane przestrzenne, a GUGiK publikuje zbiorczą warstwę WMS projektowanych planów. Ułatwia to budowę produktu, ale oznacza również, że samo pokazanie POG na mapie szybko stanie się powszechną funkcją, a nie trwałą przewagą konkurencyjną.

Źródła:

- [MRiT — wydłużony termin sporządzania planów ogólnych](https://www.gov.pl/web/rozwoj-technologia/wydluzony-termin-sporzadzania-planow-ogolnych);
- [MRiT — reforma planowania przestrzennego](https://www.gov.pl/web/rozwoj-technologia/reforma-planowania-przestrzennego-2);
- [GUGiK — projektowane plany ogólne w Geoportalu](https://www.gov.pl/web/gugik/projektowane-plany-ogolne-gmin-pog-w-serwisie-wwwgeoportalgovpl);
- [standard danych planu ogólnego](https://www.gov.pl/web/zagospodarowanieprzestrzenne/szybki-start--pog).

Konkurenci tacy jak OnGeo, Działki360, Parcela AI i aplikacje do analizy chłonności potwierdzają, że istnieje popyt na uproszczoną ocenę działki. Pokazują też, że rynek narzędzi raportowych zaczyna się zagęszczać.

Przykłady:

- [OnGeo](https://ongeo.pl/);
- [Działki360](https://www.dzialki360.pl/);
- [Parcela AI](https://zanda.eu/);
- [AnalizaChlonnosci.ai](https://analizachlonnosci.ai/).

## Luka rynkowa

Najciekawsze miejsce na rynku znajduje się pomiędzy trzema kategoriami produktów:

1. **Geoportale** pokazują dane, ale nie prowadzą użytkownika przez decyzję.
2. **Serwisy raportowe** przygotowują jednorazową diagnozę, ale nie są długoterminowym warsztatem pracy.
3. **QGIS i narzędzia profesjonalne** pozwalają zrobić prawie wszystko, ale są zbyt trudne dla większości właścicieli, agentów i małych inwestorów.

Proponowane pozycjonowanie:

> Cyfrowa teczka działki, która łączy urzędowe dane, własną koncepcję i monitoring zmian.

Alternatywne krótkie określenia:

- centrum dowodzenia działką;
- workspace dla nieruchomości gruntowej;
- narzędzie do sprawdzania, planowania i pilnowania działki;
- cyfrowy dziennik inwestycji gruntowej.

## Najbardziej obiecujące grupy klientów

### 1. Mali inwestorzy gruntowi

Mają kilka lub kilkanaście terenów, regularnie wracają do analiz i chcą wiedzieć, co zmieniło się w planowaniu. Mogą być zainteresowani abonamentem oraz monitoringiem wielu nieruchomości.

### 2. Architekci i doradcy pomagający kupującym działki

Potrzebują szybko przygotować czytelną analizę i wstępną koncepcję bez rozpoczynania pełnego projektu CAD/GIS. Mogą wykorzystywać aplikację jako narzędzie do rozmowy z klientem.

### 3. Agenci specjalizujący się w gruntach

Potrzebują szybkiego zebrania danych, atrakcyjnej prezentacji terenu oraz odpowiedzi na podstawowe pytania kupującego.

### 4. Właściciele większych terenów rodzinnych

Chcą analizować podział, dojazd, media, potencjalne budynki i wpływ zmian planistycznych na wartość nieruchomości.

### Klient mniej atrakcyjny dla abonamentu

Osoba prywatna kupująca jedną działkę raz w życiu ma realny problem, ale rzadko będzie regularnym użytkownikiem. Dla niej właściwszy jest płatny jednorazowy raport lub krótkoterminowy dostęp do projektu.

## Co należy dodać do produktu

### 1. Utworzenie projektu działki w minutę

Użytkownik podaje numer działki, adres albo wskazuje obszar na mapie. Aplikacja automatycznie:

- wybiera właściwy układ współrzędnych;
- pobiera granice działki i działek sąsiednich;
- dopasowuje kadr;
- dodaje ortofotomapę, budynki i dostępne warstwy;
- odnajduje MPZP, POG albo projekt POG;
- tworzy odrębny projekt z unikalnym identyfikatorem;
- zapisuje źródła i daty pobrania danych.

To najważniejszy warunek skalowania. Obecna ocena przenaszalności 4/10 uniemożliwia oferowanie aplikacji większej liczbie użytkowników.

### 2. Automatyczny status działki

Aplikacja nie powinna ograniczać się do pokazania warstw. Powinna odpowiadać prostym językiem:

- czy obowiązuje MPZP;
- czy istnieje projekt lub uchwalony plan ogólny;
- w jakiej strefie planistycznej znajduje się działka;
- jaki procent działki znajduje się w każdej strefie;
- jakie ograniczenia widoczne są w dostępnych źródłach;
- czy działka ma widoczny dostęp do drogi;
- jakie sieci znajdują się w pobliżu;
- z jakiej daty pochodzi każda informacja;
- które informacje są urzędowe, projektowane albo wyłącznie poglądowe.

Kluczowa zasada produktu:

> Nie tylko pokazywać dane, lecz tłumaczyć ich możliwe znaczenie dla decyzji użytkownika.

### 3. Monitoring zmian

Monitoring może być najmocniejszą i najbardziej trwałą przewagą produktu.

Użytkownik powinien dostać powiadomienie, gdy:

- opublikowano nowy projekt planu ogólnego;
- zmieniła się strefa planistyczna obejmująca działkę;
- rozpoczęły się konsultacje społeczne;
- zmienił się MPZP;
- pojawiła się nowa wersja pliku GML;
- zmiana dokumentu obejmuje obserwowaną nieruchomość;
- pojawiły się nowe dokumenty lub komunikaty gminy związane z obszarem.

Jednorazowy raport jest zdjęciem sytuacji. Monitoring tworzy powód, aby użytkownik wracał do produktu i opłacał abonament.

### 4. Scenariusze zagospodarowania

Obecne ręczne szkice można rozwinąć w narzędzia do wstępnego testowania pomysłów:

- budynek o podanych wymiarach;
- automatyczne odsunięcia od granic;
- droga o określonej szerokości;
- propozycja podziału nieruchomości;
- bufory od sieci, cieków, lasu i innych obiektów;
- obliczanie powierzchni zabudowy;
- porównywanie wariantów A, B i C;
- szacunkowa liczba działek możliwych do uzyskania po podziale;
- powierzchnia pozostająca po wydzieleniu drogi;
- proste szacunki długości przyłączy.

Funkcje te powinny być wyraźnie opisane jako analiza wstępna, a nie projekt budowlany, prawny lub geodezyjny.

### 5. Porównywanie działek

Kupujący powinien móc zestawić kilka ofert w jednym projekcie.

Przykładowe kryteria:

| Kryterium | Działka A | Działka B |
|---|---:|---:|
| MPZP/POG | obowiązujący MPZP | projekt POG |
| Dostęp do drogi | bezpośredni | niepewny |
| Odległość do mediów | 30 m | 140 m |
| Nachylenie | małe | duże |
| Widoczne ryzyka | brak | obszar osuwiskowy |
| Szacowana powierzchnia użyteczna | 82% | 54% |

Taka funkcja odpowiada na rzeczywistą decyzję użytkownika: „którą działkę wybrać?”, a nie tylko „co znajduje się na mapie?”.

### 6. Źródła, wersje i wiarygodność

Każda informacja powinna mieć:

- nazwę źródła;
- datę pobrania;
- link do dokumentu lub usługi;
- status: obowiązujące, projektowane, archiwalne albo poglądowe;
- wersję dokumentu;
- ostrzeżenie, czego nie wolno traktować jako pomiaru geodezyjnego lub opinii prawnej.

Powinna istnieć historia zmian pokazująca, co i kiedy zmieniło się w projekcie.

### 7. Udostępnianie i raportowanie

Oprócz interaktywnej mapy warto generować:

- czytelny raport PDF;
- prywatny link do projektu;
- wersję tylko do oglądania;
- zaproszenia dla klienta lub współpracownika;
- eksport GeoJSON, KML i DXF;
- paczkę projektu offline;
- komentarze i historię decyzji;
- zestaw źródeł wykorzystanych do analizy.

## Czego nie budować na początku

Nie należy od razu próbować konkurować z największymi raportami liczbą kilkudziesięciu analiz. Utrzymanie wielu źródeł danych może pochłonąć większość pracy, zanim zostanie potwierdzone zainteresowanie produktem.

Na początku nie warto również budować:

- pełnego systemu GIS;
- rozbudowanego CAD-u;
- systemu obsługi ksiąg wieczystych;
- automatycznej analizy prawnej;
- jednoznacznego werdyktu „można/nie można budować” bez zastrzeżeń;
- systemu dla administracji publicznej;
- portalu społecznościowego z publicznymi mapami;
- własnej kompletnej bazy wszystkich danych przestrzennych w Polsce.

## Proponowany pierwszy produkt

Pierwsza sprzedawalna wersja powinna realizować jeden spójny proces:

1. Użytkownik wpisuje numer działki.
2. System automatycznie tworzy projekt.
3. Użytkownik widzi granice, ortofoto, budynki, MPZP/POG i podstawowe ograniczenia.
4. System przedstawia prostą listę potencjalnych czerwonych flag wraz ze źródłami.
5. Użytkownik może narysować budynek, drogę i propozycję podziału.
6. System oblicza podstawowe powierzchnie i odległości.
7. Użytkownik generuje PDF albo prywatny link.
8. Użytkownik może włączyć monitoring zmian planistycznych.

## Proponowany model biznesowy

### Jednorazowa analiza

Dla osoby prywatnej sprawdzającej jedną działkę. Wynikiem jest raport oraz czasowy dostęp do interaktywnego projektu.

### Abonament profesjonalny

Dla agentów, architektów, doradców i małych inwestorów. Obejmuje wiele projektów, własne oznaczenia, eksporty i udostępnianie klientom.

### Monitoring portfela

Dla osób posiadających lub obserwujących wiele terenów. Najważniejszą wartością są automatyczne powiadomienia o zmianach planistycznych.

Nie należy ustalać ostatecznych cen przed rozmowami z użytkownikami. W pierwszych testach można porównywać gotowość do zapłaty za trzy osobne wartości: raport, narzędzia scenariuszowe i monitoring.

## Walidacja przed dalszym programowaniem

Pierwszy test rynku nie powinien polegać na wielomiesięcznej rozbudowie aplikacji.

### Etap 1 — rozmowy problemowe

Przeprowadzić rozmowy z co najmniej:

- 5 małymi inwestorami gruntowymi;
- 5 agentami nieruchomości specjalizującymi się w gruntach;
- 5 architektami lub doradcami;
- 5 osobami, które niedawno kupowały działkę.

Pytania powinny dotyczyć ich ostatniego realnego procesu, a nie opinii o hipotetycznej aplikacji:

- Jak sprawdzali ostatnią działkę?
- Z jakich stron i dokumentów korzystali?
- Co zajęło najwięcej czasu?
- Gdzie bali się popełnić błąd?
- Za co już zapłacili?
- Do jakich informacji wracali później?
- Jak dowiadują się o zmianach planistycznych?

### Etap 2 — usługa wykonywana ręcznie

Przygotować ręcznie 10 kompletnych projektów działek dla realnych użytkowników. Obserwować:

- za którą część chcą zapłacić;
- czego nie rozumieją;
- czy bardziej cenią raport, mapę, scenariusze czy monitoring;
- czy wracają do projektu po pierwszym użyciu;
- czy wysyłają projekt architektowi, współwłaścicielowi lub agentowi.

### Etap 3 — test oferty

Zbudować prostą stronę opisującą trzy możliwe produkty:

1. sprawdzenie jednej działki;
2. interaktywny projekt i warianty zagospodarowania;
3. stały monitoring nieruchomości.

Mierzyć oddzielnie zainteresowanie każdą ofertą. Nie zakładać z góry, że wszystkie muszą trafić do jednego pakietu.

### Etap 4 — automatyzacja

Dopiero po potwierdzeniu najważniejszego zastosowania automatyzować:

- zakładanie projektu;
- pobieranie i wersjonowanie danych;
- interpretację podstawowych warstw;
- generowanie raportu;
- monitoring zmian.

## Ryzyka

### Dane i kompletność

Dostępność i jakość danych różnią się pomiędzy gminami. Produkt musi umieć jasno powiedzieć „brak danych” zamiast sugerować brak zjawiska.

### Odpowiedzialność

Automatyczne wnioski mogą zostać potraktowane jako porada prawna, projektowa lub geodezyjna. Każdy wynik powinien wskazywać źródło, poziom pewności i potrzebę weryfikacji przez właściwego specjalistę.

### Konkurencja publiczna

Geoportal i przyszły Rejestr Urbanistyczny mogą stopniowo dodawać funkcje dostępne dziś tylko w prywatnych aplikacjach. Przewaga produktu nie może opierać się wyłącznie na wyświetlaniu publicznych warstw.

### Konkurencja komercyjna

Serwisy raportowe mogą szybko dodać część funkcji mapowych. Trudniejsza do skopiowania będzie historia projektu, monitoring konkretnych nieruchomości oraz przepływ pracy od analizy do własnych scenariuszy.

### Produkt jednorazowego użycia

Jeżeli aplikacja kończy się na raporcie, większość klientów użyje jej raz. Monitoring, portfel działek i współpraca z klientem lub projektantem tworzą szansę na powtarzalne użycie.

## Rekomendacja strategiczna

Nie budować „lepszego Geoportalu”. Budować produkt prowadzący użytkownika przez trzy kolejne potrzeby:

```text
SPRAWDŹ → ZAPLANUJ → PILNUJ ZMIAN
```

- **Sprawdź:** automatyczna diagnoza działki z wiarygodnymi źródłami.
- **Zaplanuj:** proste scenariusze budynku, drogi i podziału.
- **Pilnuj zmian:** monitoring planów, konsultacji i nowych wersji danych.

Najmocniejszym punktem wejścia może być **monitoring wpływu planów ogólnych na konkretne nieruchomości**, a najbardziej naturalnym rozwinięciem — stała cyfrowa teczka działki.

## Ostateczny werdykt

Jako sama warstwowa mapa produkt będzie zbyt łatwy do zastąpienia przez Geoportal, PLANIA, QGIS albo serwisy raportowe.

Jako **centrum dowodzenia działką**, łączące automatyczną analizę, własne scenariusze, dokumentację źródeł i monitoring zmian, ma realny sens rynkowy.

Najbliższy następny krok to nie rozbudowa kodu, lecz przeprowadzenie rozmów z potencjalnymi klientami i ręczne dostarczenie kilku kompletnych projektów w celu sprawdzenia, która część rozwiązania ma dla nich największą wartość.
