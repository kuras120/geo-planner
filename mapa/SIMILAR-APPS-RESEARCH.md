# Research podobnych aplikacji mapowych

Data researchu: 19 lipca 2026 r.

## Krótka odpowiedź

**Tak — istnieją aplikacje robiące podobne rzeczy, ale nie znalazłem jednego gotowego produktu, który odwzorowuje cały obecny sposób pracy.** Najbliższe są:

1. **PLANIA** — najbliższa prostotą pracy z działkami, GML-em, rysowaniem i eksportem;
2. **Geoportal.gov.pl** — najbliższy zakresem polskich danych urzędowych;
3. **QGIS + QField** — najbliższy pełnym zakresem technicznym, także offline, ale znacznie bardziej złożony;
4. **Scribble Maps lub Felt** — najbliższe wygodą rysowania własnych obiektów i zarządzania warstwami;
5. **OnGeo.pl i Działki360** — lepsze w automatycznym badaniu ryzyk działki, lecz nie są osobistym edytorem mapy.

Obecna aplikacja ma sens jako osobne rozwiązanie, jeżeli ważne są jednocześnie: konkretny zestaw działek, kontrola nad warstwami, własne oznaczenia, zapis danych w lokalnych plikach, brak konta i możliwość zachowania gotowej mapy jako jednego HTML-a.

## Co przyjąłem jako punkt odniesienia

Na podstawie `PORTABILITY-AUDIT.md` porównywana aplikacja zapewnia:

- wybrane działki ewidencyjne i ich metadane;
- ortofotomapę, budynki, numery działek, opcjonalnie adresy i poglądowy GESUT;
- warstwy projektu planu ogólnego z pliku GML;
- przełączanie warstw i wybieranie obiektów;
- ręczne rysowanie punktów, linii i obszarów;
- trwały zapis własnych szkiców do lokalnego pliku oraz eksport GeoJSON;
- wygenerowany, prawie samodzielny plik HTML;
- działanie bez konta i bez wysyłania własnych szkiców do obcej chmury.

To ważne rozróżnienie: serwis może świetnie **analizować działkę**, ale nie być dobrym **osobistym warsztatem mapowym**, albo odwrotnie.

## Najważniejsze wyniki

| Aplikacja | Dane działek i polskie warstwy urzędowe | Planowanie przestrzenne | Własne rysowanie | Eksport danych | Lokalnie/offline | Podobieństwo do naszej mapy |
|---|---:|---:|---:|---:|---:|---:|
| PLANIA | wysokie | ograniczone / przez własny GML | wysokie | bardzo wysokie | częściowo, w przeglądarce | **8/10** |
| Geoportal.gov.pl | bardzo wysokie | wysokie | podstawowe narzędzia i pomiary | średnie | niskie; aplikacja mobilna ma zapis tras | **7/10** |
| QGIS + QField | zależy od konfiguracji źródeł | bardzo wysokie | bardzo wysokie | bardzo wysokie | bardzo wysokie | **9/10 funkcjonalnie, 4/10 prostotą** |
| Scribble Maps | brak polskich danych urzędowych „z pudełka” | tylko po imporcie | bardzo wysokie | wysokie | głównie chmura | **6/10** |
| Felt | brak polskich danych urzędowych „z pudełka” | tylko po imporcie | wysokie | wysokie | głównie chmura; offline zależny od planu | **6/10** |
| OnGeo.pl | bardzo wysokie | wysokie | niskie | raport PDF | nie | **6/10** |
| Działki360 | bardzo wysokie | wysokie | niskie | raport / wyniki analizy | nie | **6/10** |
| Geoportal Krajowy / Na Mapie | wysokie | średnie | rysowanie do selekcji | CSV/XLS danych działek | nie | **5/10** |

Oceny są oceną dopasowania do naszego konkretnego zastosowania, a nie ogólną oceną jakości produktu.

## Omówienie kandydatów

### 1. PLANIA — najbliższa gotowa aplikacja przeglądarkowa

PLANIA łączy mapę satelitarną z granicami i numerami działek, identyfikację działki, rysowanie linii i poligonów, pomiary oraz import GML i DXF. Deklaruje eksport do DXF, DWG, SHP, PDF, KML/KMZ, GeoJSON i WKT oraz obsługę polskich układów PUWG 2000 i PUWG 1992.

**Co zastępuje dobrze:** oglądanie działek, szybkie szkicowanie, pomiary, otwieranie GML i wymianę danych z CAD/GIS. Pod względem interakcji to najbliższa pojedyncza aplikacja znaleziona w researchu.

**Czego nie potwierdziłem:** automatycznego zestawu warstw projektu planu ogólnego, KIEG/GESUT i metadanych skonfigurowanych dokładnie dla jednej inwestycji; lokalnego repozytorium szkiców; eksportu kompletnej, samodzielnej mapy HTML. Publiczna strona opisuje produkt, ale pełnego przepływu nie testowałem na koncie.

**Wniosek:** warto potraktować jako pierwszą aplikację do praktycznego testu porównawczego.

Źródło: [PLANIA — funkcje, formaty i obsługiwane układy współrzędnych](https://plania.pl/).

### 2. Geoportal.gov.pl — najlepsze źródło i przeglądarka danych urzędowych

Państwowy Geoportal udostępnia moduły m.in. geodezji i kartografii, planowania przestrzennego, ochrony środowiska oraz Rejestru Cen Nieruchomości. Pozwala dodawać usługi, identyfikować obiekty, tworzyć raport o działce, korzystać z ortofotomapy i pobierać część danych PZGiK. Aplikacja mobilna wyszukuje działki, dodaje zewnętrzne WMS-y, mierzy długość i powierzchnię oraz zapisuje trasę GPS do KML.

**Co zastępuje dobrze:** przeglądanie aktualnych danych państwowych i szybkie sprawdzanie działki bez utrzymywania własnych kopii rastrów.

**Czego brakuje względem naszej mapy:** prostego projektu ograniczonego do kilku działek, własnych trwałych obiektów z nazwą/statusami/opisem, zapisu szkiców do lokalnego repozytorium i jednego archiwalnego HTML-a. Jest to duży portal ogólnokrajowy, a nie osobista teczka konkretnego terenu.

Źródła: [pomoc Geoportalu — moduły, raport o działce i narzędzia](https://mapy.geoportal.gov.pl/imapnext/pomoc/aplikacja/geoportal/3_podst_narzedzia_mapy.html), [Geoportal Mobile — funkcje aplikacji](https://www.geoportal.gov.pl/pl/aplikacje/aplikacje-mobilne/).

### 3. QGIS + QField — pełny techniczny zamiennik

QGIS może połączyć WMS/WFS, GML, GeoPackage, rastry i warstwy wektorowe, obsłużyć różne CRS-y, edycję geometrii, atrybuty, style, analizy i eksporty. QField przenosi przygotowany projekt na telefon lub tablet; obsługuje pracę online i offline, a QFieldSync może spakować obszar zainteresowania, raster podkładowy i edytowalne warstwy.

**Co zastępuje dobrze:** praktycznie wszystkie funkcje naszej aplikacji, a ponadto daje dokładniejsze narzędzia GIS, walidację geometrii, georeferencję i pracę terenową.

**Cena tej elastyczności:** konfiguracja jest wyraźnie trudniejsza, interfejs mniej przyjazny dla okazjonalnego użytkownika, a udostępnienie komuś mapy nie jest tak proste jak wysłanie jednego HTML-a. QFieldCloud jest opcjonalną usługą chmurową; wariant kablowy/lokalny pozwala obyć się bez niej.

**Wniosek:** najlepszy kierunek, jeżeli projekt urośnie w profesjonalny system GIS lub potrzebna będzie prawdziwa praca terenowa offline. Dla kilku działek może być przerostem formy.

Źródła: [QField — praca online i offline z projektami QGIS](https://docs.qfield.org/get-started/), [QFieldSync — pakowanie warstw i podkładu offline](https://docs.qfield.org/get-started/tutorials/get-started-qfs/), [obsługiwane formaty QField](https://docs.qfield.org/reference/data-format/).

### 4. Scribble Maps — dobry osobisty edytor szkiców

Scribble Maps służy do rysowania punktów, linii, poligonów i innych kształtów, tworzenia warstw, etykietowania, importu danych oraz eksportu m.in. GeoJSON i KML. Ma darmowy plan z ograniczeniami oraz płatne plany rozszerzające liczbę map, eksport i współpracę.

**Co zastępuje dobrze:** ręczne oznaczanie dróg, budynków i planowanych obszarów oraz dzielenie obiektów na warstwy.

**Czego nie daje od razu:** polskich działek, planu ogólnego, KIEG/GESUT i metadanych terenu. Trzeba najpierw przygotować i zaimportować dane, a projekt jest zależny od zewnętrznego serwisu.

Źródła: [Scribble Maps — rysowanie, warstwy i import/eksport](https://www.scribblemaps.com/pl), [Scribble Maps dla GIS — obsługiwane dane i eksport](https://www.scribblemaps.com/roles/gis-analysts).

### 5. Felt — nowoczesna mapa chmurowa do warstw i współpracy

Felt importuje liczne formaty GIS, styluje warstwy, tworzy interaktywne opisy i umożliwia współdzielenie map z różnymi uprawnieniami. Adnotacje — punkty, linie i poligony — można eksportować jako GeoJSON. Produkt jest nastawiony na chmurę i współpracę; import własnych danych do zastosowań biznesowych należy do płatnych zastosowań, a dostęp offline zależy od planu i wdrożenia.

**Co zastępuje dobrze:** estetyczną warstwową mapę, własne adnotacje, komentarze i udostępnianie innym osobom.

**Czego nie daje od razu:** automatycznej integracji z polskimi usługami dla konkretnego zestawu działek ani lokalnej, samowystarczalnej kopii projektu.

Źródła: [Felt — tworzenie, stylowanie i udostępnianie map](https://help.felt.com/getting-started/create-your-first-map), [eksport warstw i adnotacji](https://help.felt.com/sharing-and-collaboration/exporting/exporting-data), [plany i ograniczenia zastosowań](https://felt.com/pricing).

### 6. OnGeo.pl — automatyczna analiza działki zamiast ręcznej mapy

OnGeo tworzy płatny Raport o Terenie dla wskazanej działki lub obszaru. Zakres obejmuje m.in. EGiB, MPZP, uzbrojenie, ukształtowanie terenu, zagrożenia, ograniczenia formalnoprawne, otoczenie i ceny nieruchomości.

**Przewaga nad naszą aplikacją:** znacznie więcej gotowych analiz ryzyka, bez samodzielnego pobierania i składania danych.

**Różnica:** wynikiem jest diagnoza/raport, nie stale edytowana osobista mapa ze szkicami i lokalnymi warstwami. OnGeo uzupełnia nasze narzędzie bardziej, niż je zastępuje.

Źródło: [OnGeo — zakres Raportu o Terenie](https://ongeo.pl/).

### 7. Działki360 — raport i interaktywna analiza 3D

Działki360 agreguje informacje o geometrii i EGiB, planowaniu, dostępie do drogi i mediów, fizjografii, nasłonecznieniu, geologii, zagrożeniach oraz otoczeniu. Serwis deklaruje także interaktywną mapę 3D.

**Przewaga nad naszą aplikacją:** szeroki, gotowy pakiet analityczny dla decyzji inwestycyjnej.

**Różnica:** podobnie jak OnGeo, jest to produkt raportowy, a nie prywatny edytor przestrzenny do nanoszenia własnej koncepcji.

Źródło: [Działki360 — zawartość raportu i mapa 3D](https://www.dzialki360.pl/).

### 8. Geoportal Krajowy / Na Mapie — wygodne wyszukiwanie i selekcja działek

Serwis umożliwia wyszukiwanie działek, wskazywanie wielu działek przez narysowanie okręgu, prostokąta, kwadratu lub linii oraz eksport tabeli wybranych działek do CSV/XLS.

**Co zastępuje dobrze:** szybkie znalezienie i zebranie podstawowych danych o grupie działek.

**Różnica:** narysowana geometria służy przede wszystkim do selekcji działek; nie jest odpowiednikiem własnej trwałej warstwy projektu z drogami, budynkami i opisami.

Źródło: [Geoportal Krajowy — selekcja wielu działek i eksport](https://geoportal-krajowy.pl/pomoc/selekcja-dzialek).

## Czy warto zastąpić naszą aplikację?

### Jeżeli celem jest tylko sprawdzenie działki przed zakupem

Najwygodniejsze będą **OnGeo albo Działki360**, uzupełnione bezpłatnym Geoportalem. Dadzą więcej automatycznych informacji o ryzykach niż obecna mapa.

### Jeżeli celem jest rysowanie koncepcji na działkach

Najpierw warto przetestować **PLANIA**. Jeżeli wystarczy jej sposób zapisu projektów i da się wygodnie wczytać potrzebne GML-e, może zastąpić dużą część ręcznego warsztatu.

### Jeżeli potrzebna jest dokładna, długoterminowa baza przestrzenna

Najlepszy będzie **QGIS**, ewentualnie z **QField** do pracy w terenie. Jest to funkcjonalny następca, ale wymaga nauczenia się GIS-u i przygotowania projektu.

### Jeżeli najważniejsze są prostota i pełna kontrola nad plikami

Warto zachować i uogólnić obecną aplikację zgodnie z `PORTABILITY-AUDIT.md`. Jej przewaga nie polega na liczbie analiz, tylko na dopasowaniu do konkretnej nieruchomości, lokalnym zapisie, prostym interfejsie i braku zależności od konta usługodawcy.

## Rekomendacja końcowa

1. **Nie porzucać obecnej aplikacji wyłącznie dlatego, że istnieją geoportale.** Żaden z przejrzanych produktów nie łączy równie prosto wszystkich naszych warstw, własnych opisanych szkiców i lokalnego archiwum HTML.
2. **Wykonać praktyczny test PLANII** na tym samym GML-u i tych samych 2–3 szkicach. To kandydat najbliższy bezpośredniemu zamiennikowi.
3. **Korzystać z OnGeo lub Działki360 jako jednorazowego źródła dodatkowego raportu ryzyk**, nie jako zamiennika mapy roboczej.
4. **Rozważyć QGIS/QField dopiero wtedy**, gdy pojawi się drugi teren, pomiary terenowe, większa liczba obiektów, potrzeba poprawnej obsługi wielu CRS-ów lub współpraca z projektantem/geodetą.
5. Przy uogólnianiu własnej aplikacji warto skopiować z rynku dwie idee: obsługę wielu formatów i układów z PLANII oraz pakowanie projektu offline dla wybranego obszaru z QField.

## Ograniczenia researchu

- Porównanie wykonano na podstawie publicznych stron produktów i oficjalnej dokumentacji dostępnych 19 lipca 2026 r.; nie zakładano płatnych kont i nie wykonywano pełnych testów każdego interfejsu.
- Dostępność konkretnych warstw urzędowych może zależeć od gminy, kompletności usług źródłowych i aktualności publikacji.
- Cenniki i zakres planów chmurowych mogą się zmieniać; dlatego raport opisuje model dostępu, a nie utrwala kwot.
- Mapa działek, uzbrojenie i ręczne szkice w każdym z tych narzędzi mają charakter informacyjny. Nie zastępują dokumentów urzędowych, mapy do celów projektowych ani pomiaru geodety.
