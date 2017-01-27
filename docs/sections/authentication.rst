.. _authentication:

****************
Uwierzytelnianie
****************

W tym rozdziale opiszemy formy uwierzytelniania, z szczególnym uwzględnieniem dwuskładnikowego uwierzytelniania. Założenia leżące u jego podstaw, korzyści, ryzyko, ograniczenia, a także przeanalizujemy formy dwuskładnikowego dokonując analizy ich słabych i mocnych stron.

W tym rozdziale zostaną także przedstawine doświadczenia autora uzyskane w ramach projektu Koła Naukowego Programistów "Geek" polegającej na stworzeniu i rozwoju strony internetowej `Dwa-Skladniki.pl`_. Zostaną one przedstawione w formie analizy dotychczas wykorzystywanych w Polsce form uwierzytelniania. Zostanie przedstawiona analiza odnosząca się do sektora publicznego, jak również prywatnego, w tym perspektyw rozwoju w sektorze bankowości, który - obecnie - wytycza trendy.

.. todo:: Zapoznać się z:

    * https://pages.nist.gov/800-63-3/sp800-63b.html DRAFT NIST Special Publication 800-63B Digital Authentication Guideline
    * wyjaśnić hasło "Bring Your Own Authentication (BYOA)""
    * https://sekurak.pl/kompendium-bezpieczenstwa-hasel-atak-i-obrona/

.. _Dwa-Skladniki.pl: https://dwa-skladniki.pl/

.. _authentication_intro:

Kontrola dostępu
================

Aplikacje zakładające interakcję z użytkownikiem wymagają zwykle przeprowadzenia procesu składającego zasadniczo z trzech etapów  [#f1]_:

* identyfikacji (ang. `identification`) użytkownika, czyli uzyskania od użytkownika deklaracji co do swojej tożsamości np. w postaci nazwy użytkownika, w sposób umożliwiający zidnetyfikowanie tożsamości użytkownika w danym środowisku,
* uwierzytelnienia (ang. `authentication`) użytkownika, czyli dostarczenia dowodów, że użytkownik jest właśnie tą zidentyfikowaną osobą (nikt się nie podszywa), a dane uzyskane w etapie identyfikacji są autentyczne,
* autoryzacji (ang. `authorization`), czyli przyznaniu przez system komputerowy dostępu do określonego zasobu.

Proces ten przeprowadzony łącznie jest nazywany logowaniem (ang. `logging in` or `signing in`). Każdy z tych etapów może być przeprowadzony w odmienny sposób w zależności od wymogów systemu komputerowego. Najpopularniejszą formą identyfikacji i uwierzytelniania użytkowników w systemach komputerowych jest wykorzystanie nazwa użytkownika (ang. `login`) i hasła [#citation_needed]_ . Jednak tradycyjne podejście nie jest wystarczająco bezpieczne w dzisiejszym świecie, w którym co dzień zdarzają się ataki szkodliwego oprogramowania i inne formy kradzieży haseł wykazujące słabość tego mechanizmu.

Największym wyzwaniem w projektowaniu procesu uwierzytelniania systemów komputerowych pracujących w sieci Internet wydaje się stanowić uwierzytelnianie. Musi ono zapewnić adekwatny do charakteru systemu komputerowy poziom bezpieczeństwa systemu komputerowego przy zachowaniu użyteczność (ang. `usability`) akceptowalnej przez użytkownaia. Twie te wartości pozostają niezwykle często w napięciu.

Jeśli mechanizmy bezpieczeństwa są zbyt skomplikowane w obsłudze, użytkownicy często wybierają, aby nie używać ich w ogóle, albo poszukują metod na ich obejście. 

Przykładowo uwierzytelnienie z wykorzystaniem hasła wymaga współdzielonego pomiędzy użytkownikiem i systemem komputerowym sekretu. Dane te powinny zostać zapamiętane przez użytkownika w umyśle. Jednak nieprawidłowe wymogi odnośnie takiego sekretu skłaniają użytkowników do ich zapisywania narażając poufność sekretu (zob. :ref:`password_policy`). Wymaga to ostrożnego doboru sposobów (form) w jakich uwierzytelnianie ma przebiegać. Nieprawidłowy dobór, nawet mechanizmów, które technicznie zapewniają wyższy poziom bezpieczeństwa - ze względu na niezrozumienie użytkownika i nie stosowanie się do nich przez użytkowania (czynnik ludzki) - może paradoksalnie zwiększać zagrożenie dla danych osobowych.

.. todo:: Rozbudować bibliografie:

    * Google hasła "Security and Usability"
    * publikacja  Lorrie Faith Cranor; Simson Garfinkel, "Security and Usability : Designing Secure Systems that People Can Use.", O'Reilly Media, Inc.

Formy uwierzytelniania
======================

Wykorzystanie hasła nie jest jedyną możliwą formą uwierzytelniania, która może zostać wykorzystana w systemie komputerowym, aczkolwiek najpopularniejszą. Ponadto możliwe jest złożenie wielu form w ramach jednego procesu uwierzytelniania, co szczegółowo zostało omówione :ref:`2factor`.

W dalszych rozważaniach będzie wykorzystywana następująca klasyfikacja podstawowych form uwierzytelniania:

* coś co wiesz (*something you know*) – informacja będąca w wyłącznym posiadaniu uprawnionego podmiotu, na przykład hasło lub klucz prywatny;
* coś co masz (*something you have*) – przedmiot będący w posiadaniu uprawnionego podmiotu, na przykład generator kodów elektronicznych (token), telefon komórkowy (kody SMS, połączenie autoryzacyjne) lub klucz analogowy,
* coś czym jesteś (*something you are*) – metody biometryczne.

Hasło
-----

W przypadku wielu systemów komputerowych do uwierzytelniania wykorzystywane jest wyłącznie hasło. Jest to najpopularniejszą forma uwierzytelniania. Stanowi ona formę uwierzytelniania typu *coś co wiesz*. 

Ten proces uwierzytelniania wymaga wcześniejszego zindywidualnego dla każdego użytkownika skonfigurowania polegajacego na wymianie hasła pomiędzy użytkownikiem a systemem komputerowym. W zależności od decyzji projektanta systemu współdzielone hasło może zostać wygenerowane przez system komputerowy, albo być wprowadzane przez użytkownika. W przypadku dużej części aplikacji internetowych wymiana współdzielonego hasła ma miejsce podczas rejestracji. Powszechnie tworzone są dedykowane formularze służące do zmiany haseł i odzyskania zdolności do uwierzytelniania ("Przypomnij hasło").

Proces konfiguracji współdzielonego hasła wymaga, aby uprzednio użytkownik został uwierzytelniony w inny sposób.

W przypadku wykorzystania wyłącznie tej formy uwierzytelnianie polega ona na wprowadzeniu hasła użytkownika. W związku z ograniczonym bezpieczeństwem tej formy uwierzytelniania wdrażane są w systemach komputerowych liczne metody, które mają ograniczyć jej wady. Działania te są podejmowane na poziomie organizacyjnym i technicznym.

.. seqdiag::
   :desctable:
   :caption: Podstawowe uwierzytelnienie hasłem

   seqdiag {
      A -> B -> C [label="nowe hasło"];
      D -> C [label="stare hasło"];
      C -> C [label="porównanie haseł"];
      C -> B [label="wynik weryfikacji"]
      A [description = "użytkownik"];
      B [description = "przeglądarka"]
      C [description = "aplikacja"];
      D [description = "baza danych"];
   }

Funkcje hashujące
^^^^^^^^^^^^^^^^^

Wartm odnotowania mechanizmem na poziomie technicznym jest tzw. *hashowanie* haseł. Polega ono na ograniczeniu dostępności w systemie komputerowmy hasła w postaci jawnej poprzez zapisanie wyłącznie danych stanowiących wynik jednokierunkowej funkcji skrótu kryptograficznego tzw. `hash`. Bezpieczne funkcje hashujące h(x) = hash są funkcjami hashującymi z następującymi właściwościami [#sekurak_kompedium1]_:

    Jednokierunkowość – na podstawie wyjścia (hash) nie możemy w żaden sposób określić wejścia (x).
    Wysoka odporność na kolizje – bardzo trudna generacja tego samego wyjścia (hash) przy użyciu dwóch różnych wejść (x1, x2).
    Duża zmienność wyjścia – duża różnica wyjść (hash1, hash2) wygenerowanych przez bardzo podobne wejścia (x1, x2).

W przypadku zastosowania takiego rozwiązania proces uwierzytelniania polega na porównaniu danych stanowiących wynik funkcji. 
Można to przedstawić następująco:

.. seqdiag::
   :desctable:
   :caption: Uwierzytelnianie hasłem z wykorzystaniem funkcji skrótu

   seqdiag {
      A -> B -> C [label="nowe hasło"];
      C -> C [label= "nowe hasło -> nowy hash"];
      D -> C [label="stary hash"];
      C -> C [label="porównanie hashy"];
      C -> B [label="wynik weryfikacji"]
      A [description = "użytkownik"];
      B [description = "przeglądarka"]
      C [description = "aplikacja"];
      D [description = "baza danych"];
   }

Dzięki wykorzystaniu funkcji skrótu zostało ograniczone ryzyko, że po włamaniu do bazy danych użytkownik będzie od razu zagrożony [#f_dropbox]_. Wykorzystanie takich danych wymaga odnalezienie słabości funkcji hashującej, co zazwyczaj wymaga zaangażowania znacznych mocy obliczeniowych. W wielu wypadkach zastosowanie funkcji skrótu zwiększa zasoby wymaganie do wykorzystania danych, ale tego nie uniemożliwia. Może to jednak być wystarczające, aby zneutralizować zagrożenie.

Projektowane są dedykowane algorytmy funkcji skrótu kryptograficznego, które przeznaczeniem jest hashowania haseł statycznych, a nie dowolnych danych binarnych. Określane są one mianem PKF (ang. `key derivation function`). Do najbardziej znaczących należą PBKDF2, bcrypt i scrypt. Oferują one m. in. mechanizm `key stretching` stanowiącą konfigurowalną wartość wpływającą na złożoność obliczeniową funkcji zapewniając stanowi opór dla prawa Moore’a, a także elastyczność wobec ataków wymyślonym w przyszłości (future-proof).

Uwierzytelnienie wyzwanie-odpowiedź
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hasło musi stanowić sekret znany wyłącznie przez użytkownika i system komputerowy zagrożeniem dla uwierzytelniania hasłem jest rownież przesyłanie go w postaci jawnej poprzez sieć. W celu ograniczenia tego zagrożenia wykorzystywane są odpowiednie mechanizmy. Warto w tym miejscu zwrócić uwagę na grupę algorytmów wyzwanie-odpowiedź, które zapewniają ochronę przed prostym podsłuchaniem hasła.

.. seqdiag::
   :desctable:
   :caption: Uwierzytelnianie z wykorzystaniem mechanizmu wyzwanie-odpowiedź

   seqdiag {
      U; C; S; D;
      C -> S [label="żadanie wyzwania"];
      S -> S [label="wygenerowanie losowej wartości X"];
      S -> C [label="przekazanie losowej wartosci X"];
      C -> U [label="zapytanie o hasło"];
      U -> C [label="wprowadzenie hasła Z"];
      C -> C [label="obliczenie funkcji skrótu f(X, Z) = D"]
      C -> S [label="przekazanie skrótu D"];
      S -> D [label="żądanie hasła"];
      D -> S [label="przekazanie hasła Z'"];
      S -> S [label="obliczenie funkcji skrótu f(X, Z') = D'"];
      S -> S [label="porównianie D i D'"];
      S -> C [label="przekazanie wyniku weryfikacji"];
      C -> U [label="komunikat o weryfikacji"];
      U [description = "użytkownik"];
      C [description = "klient"]
      S [description = "serwer"];
      D [description = "baza danych"];
   }

Po pierwsze wykorzystywane są algorytmy szyfrowania całej komunikacji w architekturze klient-serwer np. HTTPS (ang. `Hypertext Transfer Protocol Secure`). 

Należy zaznaczyć, że szyfrowanie komunikacji klient-serwer nie zabezpiecza przed przypadkami, gdy hasło zostanie podsłuchane pomiedzy użytkownikiem, a przeglądarką np. na skutek wykorzystania `keyloggerów` lub innego złośliwego oprogramowania pracujące na komputerze użytkownika. 

Zagrożeniem dla tego mechanizmu jest również celowo wywołane błędne przeświadcze co do tożsamości strony, które jest wykorzystywane podczas ataków typu .phishing  Zabezpieczenie hasła przed tym wymaga podejmowania znacznych nakładów na zabezpieczenie urządzeń użytkownika.

W aspekcie technicznym podejmowane są działania, które mogą ograniczyć skuteczność keyloggerów. Należą w tym zakresie m. in. hasła maskowane, które polegają na oczekiwaniu od użytkownika jednorazowo tylko wybranych znaków z hasła i z każdą zmianą zmienianie tego zestawu znaków. W takiej sytuacji nie jest wystarczające jednorazowe podsłuchanie wprowadzonych danych, gdyż podczas kolejnego uwierzytelniania wymagane będzie inny zestaw znaków.

.. figure:: ../img/authentication/masked-password.png

    Przykładowy ekran uwierzytelniania z wykorzystaniem hasła maskowanego (T-Mobile Usługi bankowe, styczeń 2016 roku) (opr. własne)



.. _password_policy:

Polityki haseł
^^^^^^^^^^^^^^

W zakresie organizacyjnym, który często wspierany jest także odpowiednimi rozwiązaniami technicznymi wprowadzone są polityki haseł. Obejmują one najczęsciej zagadnienia dotyczącego ponownego wykorzystania tych samych haseł w tym i innych systemach komputerowych, złożoność haseł i częstotliwość ich zmiany.

Warto w tym miejscu dostrzec, że nieadekwatna polityka haseł może prowadzić do ograniczenia bezpieczeństwa, a nie jego poprawy. Moim zdaniem dotyczy to w szczególności wymogu częstej zmiany haseł bez wdrożenia alternatywnych rozwiązań. Częsta zmiana haseł rodzi kilka zasadniczych problemów. Nie wszyscy posiadają zdolność zapamiętania złożonych haseł, co prowadzi do ponownego używania haseł w wielu miejscach lub stosowania haseł schematycznych z wykorzystaniem prostych transformacji. W takim wypadku zbyt skomplikowane i często zmieniane hasła prowadzą do zapisywania ich w jawnej formie, co może narażać na ich kradzież.

Odnośnie schematycznych haseł warto w tym miejscu dostrzec uwagi Lorrie Cranor z amerykańskiej Federalnej Komisji Handlu (FTC), która opisała na stronie FTC badania przeprowadzone na University of North Carolina (w Chapel Hill). Badacze pozyskali ponad 51 tys. hashy haseł do 10 tys. nieaktywnych kont studentów i pracowników, na których wymuszano zmianę hasła co 3 miesiące. Po ich analizie stwierdzono, że dla 17% kont znajomość poprzedniego hasła pozwalała na zgadnięcie kolejnego hasła w mniej niż 5 próbach [#f7]_ [#f8]_.

Podobne wątpliwości co do skuteczności polityki zmiany haseł wyrażono w badaniach tego problemu przeprowadzonych na Carleton University [#f9]_ . Dostrzeżono w nich, że w przypadku wielu ataków jednorazowy dostęp do systemu umożliwia natychmiastowe pozyskanie plików docelowych, założenie tylnych drzwi, zainstalowanie  oprogramowania typu keylogger lub innego trwałego, złośliwego oprogramowania, które późniejsze zmiany hasła uczyni nieskutecznymi. Autorzy nawet stawiają tezę, że prawdziwe korzyści z wymuszania zmiany haseł nie rekompensują związanych z tym uciążliwości.

Sytuacja ta oznacza, że nie można wprowadzić generalnej reguły, która uzasadniałaby określoną politykę haseł, wymaga to każdorazowo indywidualnej analizy administratora systemu komputerowego.

Powyższa analiza pokazuje tylko niektóre z słabości uwierzytelniania z wykorzystaniem haseł i uzasadnia konieczność poszukiwania bezpieczniejszych form uwierzytelniania.

.. _2factor:

Dwuskładnikowe uwierzytelnienie
*******************************

W nowoczesnych systemach komputerowych przed uzyskaniem dostępu często stosuje się jednak uwierzytelniani wieloskładnikowe (*multi-factor authentication*), w szczególności dwuskładnikowe (*two-factor authentication*), czyli łączące dwie różne metody uwierzytelniania.

Jest to praktykowane, ponieważ w komunikacji elektronicznej stosowanie samego hasła wiąże się z różnego rodzaju ryzykiem, a wykorzystanie kilku form uwierzytelnienia może ograniczać skutki przechwycenia (keylogger), albo podsłuchania (sniffer) hasła po którym przestaje ono być wówczas znane wyłącznie osobie uprawnionej, zaś kradzież może pozostać niezauważona. Ryzyko to można ograniczyć, wprowadzając dodatkowy składnik uwierzytelniania wykorzystując kilka form autoryzacji jednocześnie np.:

* token istniejący w jednym, unikatowym egzemplarzu, więc jego użycie wymaga fizycznego dostępu lub kradzieży, która zostanie zauważona (cecha coś co masz);
* użycie tokenu wymaga dodatkowo podania hasła (np. w postaci kodu PIN), więc bez jego znajomości token będzie nieprzydatny, nawet w razie kradzieży (cecha coś co wiesz).

Uwierzytelnienie dwuskładnikowe stosuje większość banków internetowych, usługa poczty Gmail, Facebook, Apple, platformy gier (Battle.net) i wiele innych. Powszechnie dostępne są interfejsy programistyczne do jednorazowych haseł przesyłanych za pomocą SMS, tokeny sprzętowe, jak i programowe generatory haseł TOTP (Time-based One-Time Password Algorithm) np. Google Authenticator.

Warto zwrócić uwagę, że standardy regulacyjne dotyczące dostępu do systemów rządu federalnego USA wymagają nawet używania uwierzytelniania wieloskładnikowego, aby uzyskać dostęp do krytycznych zasobów IT, na przykład podczas logowania do urządzeń sieciowych podczas wykonywania zadań administracyjnych oraz przy dostępie do uprzywilejowanego konta. Również publikacja „The Critical Security Controls for Effective Cyber Defense”, wydana przez instytut SANS, przygotowana przez rządowe agencje i komercyjnych ekspertów śledczych i d/s bezpieczeństwa stanowczo zaleca wykorzystanie takich rozwiązań [#f2]_.

.. rubric:: Footnotes

.. [#citation_needed] Potrzebne źródło

.. [#f1] Tomasz Mielnicki, Franciszek Wołowski, Marek Grajek, Piotr Popis, Identyfikacja i uwierzytelnianie w usługach elektronicznych, Przewodnik Forum Technologii Bankowych przy Związku Banków Polskich, Warszawa, 2013, http://zbp.pl/public/repozytorium/dla_bankow/rady_i_komitety/technologie_bankowe/publikacje/Przewodnik_Identyfikacja_i_uwierzytelnianie_strona_FTB.pdf [dostęp 23 grudnia 2016 roku]

.. [#f2] CIS Controls for Effective Cyber Defense Version 6.0, SANS Institute, https://www.cisecurity.org/critical-controls.cfm [dostęp 16 marca 2016 roku]

.. [#f7] Lorrie Cranor, Time to rethink mandatory password changes, 2 marca 2016 roku, Federalna Komisja Handlu, ftc.gov, https://www.ftc.gov/news-events/blogs/techftc/2016/03/time-rethink-mandatory-password-changes [dostęp 16 marca 2016 roku]

.. [#f8] Brian Barrett, Want Safer Passwords? Don’t Change Them So Often, Wired.com 3.10.2016, http://www.wired.com/2016/03/want-safer-passwords-dont-change-often/ [dostęp 16 marca 2016 roku]

.. [#f9] Sonia Chiasson, P. C. van Oorschot, Quantifying the security advantage of password expiration policies, Designs, Codes and Cryptography, 2015, Volume: 77, Issue 2-3, 401-4

.. [#f_dropbox] Devdatta Akhawe, How Dropbox securely stores your passwords, Dropbox Tech blog, https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/ [dostęp 2 stycznia 2016 roku]

.. [#sekurak_kompedium1] Adrian Vizzdoom Michalczyk, Kompendium bezpieczeństwa haseł – atak i obrona (część 1.), Sekurak.pl 1 lutego 2013 roku, https://sekurak.pl/kompendium-bezpieczenstwa-hasel-atak-i-obrona/ (online: 27 stycznia 2017 roku)
