.. _authentication:

****************
Uwierzytelnianie
****************

W tym rozdziale opiszemy formy uwierzytelniania, z szczególnym uwzględnieniem dwuskładnikowego uwierzytelniania. Założenia leżące u jego podstaw, korzyści, ryzyko, ograniczenia, a także przeanalizujemy formy dwuskładnikowego dokonując analizy ich słabych i mocnych stron.

W tym rozdziale zostaną także przedstawine doświadczenia autora uzyskane w ramach projektu Koła Naukowego Programistów polegającej na stworzeniu i rozwoju strony internetowej `Dwa-Skladniki.pl`_. Zostaną one przedstawione w formie analizy dotychczas wykorzystywanych w Polsce form uwierzytelniania. Zostanie przedstawiona analiza odnosząca się do sektora publicznego, jak również prywatnego, w tym perspektyw rozwoju w sektorze bankowości, który - obecnie - wytycza trendy.

.. todo:: Zapoznać się z:

    * https://pages.nist.gov/800-63-3/sp800-63b.html DRAFT NIST Special Publication 800-63B Digital Authentication Guideline
    * wyjaśnić hasło "Bring Your Own Authentication (BYOA)""
    * https://sekurak.pl/kompendium-bezpieczenstwa-hasel-atak-i-obrona/

.. _Dwa-Skladniki.pl: https://dwa-skladniki.pl/

.. _authentication_intro:

Kontrola dostępu
================

Aplikacje zakładające interakcję z użytkownikiem wymagają przeprowadzenia logowania (ang. `logging in` lub `signing in`), czyli procesu składającego się zasadniczo z trzech etapów  [#f1]_:

* identyfikacji (ang. `identification`) użytkownika, czyli uzyskania od użytkownika deklaracji co do swojej tożsamości np. w postaci nazwy użytkownika, w sposób umożliwiający zidnetyfikowanie tożsamości użytkownika w danym środowisku,
* uwierzytelnienia (ang. `authentication`) użytkownika, czyli dostarczenia dowodów, że użytkownik jest właśnie tą zidentyfikowaną osobą (nikt się nie podszywa), a dane uzyskane w etapie identyfikacji są autentyczne,
* autoryzacji (ang. `authorization`), czyli przyznaniu przez system komputerowy dostępu do określonego zasobu.

Proces ten przeprowadzony łącznie jest nazywany logowaniem. Każdy z tych etapów może być przeprowadzony w odmienny sposób w zależności od wymogów systemu komputerowego. Najpopularniejszą formą identyfikacji i uwierzytelniania użytkowników w systemach komputerowych jest wykorzystanie nazwa użytkownika (ang. `login`) i hasła [#citation_needed]_ . Jednak tradycyjne podejście nie jest wystarczająco bezpieczne w dzisiejszym świecie, w którym co dzień zdarzają się ataki szkodliwego oprogramowania i inne formy kradzieży haseł wykazujące słabość tego mechanizmu.

Wygoda użytkowania a bezpieczeństwo
===================================

Największym wyzwaniem w projektowaniu procesu logowania w systemach komputerowych pracujących w sieci Internet wydaje się stanowić uwierzytelnianie. Musi ono zapewnić adekwatny do charakteru systemu komputerowy poziom bezpieczeństwa systemu komputerowego przy zachowaniu użyteczność (ang. `usability`) akceptowalnej przez użytkownaia. Twie te wartości pozostają niezwykle często w napięciu.

Jeśli mechanizmy bezpieczeństwa są zbyt skomplikowane w obsłudze, użytkownicy często wybierają, aby nie używać ich w ogóle, albo poszukują metod na ich obejście. 

Przykładowo uwierzytelnienie z wykorzystaniem hasła wymaga współdzielonego pomiędzy użytkownikiem i systemem komputerowym sekretu. Dane te powinny zostać zapamiętane przez użytkownika w umyśle. Jednak nieprawidłowe wymogi odnośnie takiego sekretu skłaniają użytkowników do ich zapisywania narażając poufność sekretu (zob. :ref:`password_policy`). Wymaga to ostrożnego doboru sposobów (form) w jakich uwierzytelnianie ma przebiegać. Nieprawidłowy dobór, nawet mechanizmów, które technicznie zapewniają wyższy poziom bezpieczeństwa - ze względu na niezrozumienie użytkownika i nie stosowanie się do nich przez użytkowania (czynnik ludzki) - może paradoksalnie zwiększać zagrożenie dla danych osobowych.

.. todo:: Rozbudować sekcje i bibliografie:

    * Google hasła "Security and Usability"
    * publikacja  Lorrie Faith Cranor; Simson Garfinkel, "Security and Usability : Designing Secure Systems that People Can Use.", O'Reilly Media, Inc.

.. _authentication_form:

Formy uwierzytelniania
======================

Wykorzystanie hasła nie jest jedyną możliwą formą uwierzytelniania, która może zostać wykorzystana w systemie komputerowym, aczkolwiek najpopularniejszą. Ponadto możliwe jest złożenie wielu form w ramach jednego procesu uwierzytelniania, co szczegółowo zostało omówione w rozdziale :ref:`2factor`.

W dalszych rozważaniach będzie wykorzystywana następująca klasyfikacja podstawowych form uwierzytelniania:

* coś co wiesz (*something you know*) – informacja będąca w wyłącznym posiadaniu uprawnionego podmiotu, na przykład hasło lub klucz prywatny;
* coś co masz (*something you have*) – przedmiot będący w posiadaniu uprawnionego podmiotu, na przykład generator kodów elektronicznych (token), telefon komórkowy (kody SMS, połączenie autoryzacyjne) lub klucz analogowy,
* coś czym jesteś (*something you are*) – metody biometryczne.

Współdzielony sekret
--------------------

W przypadku wielu systemów komputerowych do uwierzytelniania wykorzystywane jest wyłącznie współdzielony sekret potocznie określony hasłem. Jest to najpopularniejszą forma uwierzytelniania. Stanowi ona formę uwierzytelniania typu *coś co wiesz*. 

Ten proces uwierzytelniania wymaga wcześniejszego zindywidualnego dla każdego użytkownika inicjalizacji polegajacej na wymianie hasła pomiędzy użytkownikiem a systemem komputerowym. W zależności od decyzji projektanta systemu współdzielone hasło może zostać wygenerowane przez system komputerowy, albo być wprowadzane przez użytkownika. W przypadku dużej części aplikacji internetowych wymiana współdzielonego hasła ma miejsce podczas rejestracji. Powszechnie tworzone są dedykowane formularze służące do zmiany haseł i odzyskania zdolności do uwierzytelniania ("Przypomnij hasło").

Proces wymianiy współdzielonego hasła wymaga, aby uprzednio użytkownik został uwierzytelniony w inny sposób.

W przypadku wykorzystania wyłącznie tej formy uwierzytelnianie polega ona na wprowadzeniu hasła użytkownika i wymiany komunikatów zgodnie z przedstawionym schematem: 

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

W związku z ograniczonym bezpieczeństwem tej formy uwierzytelniania wdrażane są w systemach komputerowych liczne metody, które mają ograniczyć jej słabość. Działania te są podejmowane na poziomie organizacyjnym i technicznym.

.. _hashing:

Funkcje skrótu
^^^^^^^^^^^^^^

Wartm odnotowania mechanizmem na poziomie technicznym jest tzw. *hashowanie* haseł. Polega ono na ograniczeniu dostępności w systemie komputerowmy hasła w postaci jawnej poprzez zapisanie wyłącznie danych stanowiących wynik jednokierunkowej funkcji skrótu kryptograficznego tzw. `hash`. Bezpieczne funkcje hashujące h(x) = hash są funkcjami hashującymi z następującymi właściwościami [#sekurak_kompedium1]_:

    Jednokierunkowość – na podstawie wyjścia (hash) nie możemy w żaden sposób określić wejścia (x).
    Wysoka odporność na kolizje – bardzo trudna generacja tego samego wyjścia (hash) przy użyciu dwóch różnych wejść (x1, x2).
    Duża zmienność wyjścia – duża różnica wyjść (hash1, hash2) wygenerowanych przez bardzo podobne wejścia (x1, x2).

W przypadku zastosowania takiego rozwiązania proces uwierzytelniania polega na porównaniu danych stanowiących wynik funkcji skrótu krytograficznego. 
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

Projektowane są dedykowane algorytmy funkcji skrótu kryptograficznego, które przeznaczeniem jest hashowania haseł statycznych, a nie dowolnych danych binarnych. Określane są one mianem PKF (ang. `key derivation function`). Do najbardziej znaczących należą PBKDF2, bcrypt i scrypt. Oferują one m. in. mechanizm `key stretching` stanowiącą konfigurowalną wartość wpływającą na złożoność obliczeniową funkcji zapewniając opór dla prawa Moore’a, a także elastyczność wobec ataków wymyślonym w przyszłości (future-proof).

.. _challenge_response:

Uwierzytelnienie wyzwanie-odpowiedź
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hasło musi stanowić sekret znany wyłącznie przez użytkownika i system komputerowy, a więc zagrożeniem dla uwierzytelniania hasłem jest również przesyłanie go w postaci jawnej poprzez sieć. W celu ograniczenia tego zagrożenia wykorzystywane są odpowiednie mechanizmy. Warto w tym miejscu zwrócić uwagę na grupę algorytmów wyzwanie-odpowiedź, które zapewniają ochronę przed prostym podsłuchaniem hasła podczas komunikacji sieciowej. Proces uwierzytelniania można wówczas przedstawić następująco:

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

Należy objaśnić, że sam mechanizm wyzwania ma na celu ochronę przed atakiem powtórzenia (ang. `replay attack` lub `playback attack`), który polega na skopiowaniu komunikatu i powtórki go do jednego lub większej liczby stron. Ochrona jest zapewniona, ponieważ w przypadku ponownej próby uwierzytelniania zostanie wykorzystanie inne wyzwanie (wartość X na diagramie), która lawinowo zmieni wartość kryptograficznej funkcji skrótu f(X,Z) (zob. `hashing`_ ).

Zbliżony mechanizm stanowi podstawę dla uwierzytelniania z wykorzystaniem kryptografii asymetrycznej.

Inne środki techniczne wzmocnienia uwierzytelniania hasłem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coraz większą popularnością cieszą się algorytmy szyfrowania całej komunikacji w architekturze klient-serwer np. HTTPS (ang. `Hypertext Transfer Protocol Secure`). Zabezpieczają one hasło (a także całą komunikacje sieciową) przez podsłuchem. Ogólne dostępne statystyki użytkowania przeglądarki Chrome wskazują, że 14 marca 2015 roku na platformie Windows 39% stron była wczytywana z wykorzystaniem HTTPS. Natomiast 1 października 2016 roku wskaźnik ten przekroczył 50% i wciąż systematycznie rośnie [#HTTPS_Usage]_. 

Należy w tym miejscu zwrócić także uwagę na presje płynącą z strony twórców przeglądarek internetowych. Od stycznia 2017 roku w przeglądarce Chrome w przypadku formularza zawierającego pole hasła i transmisji nieszyfrowej wyświetlane jest ostrzeżenie, a presja ta ma być rozszeszana także na inne sytuacje komunikacji nieszyfrowanej [#HTTPS_Warning]_. Podobne mechanizmy są wdrażane w aktualnych wydaniach przeglądarki Firefox [#HTTPS_Firefox]_ 

Należy zaznaczyć, że szyfrowanie komunikacji klient-serwer nie zabezpiecza przed przypadkami, gdy hasło zostanie podsłuchane pomiedzy użytkownikiem, a przeglądarką np. na skutek wykorzystania `keyloggerów` lub innego złośliwego oprogramowania pracujące na komputerze użytkownika. 

Zagrożeniem dla tego mechanizmu jest również celowo wywołane błędne przeświadcze co do tożsamości strony, które jest wykorzystywane podczas ataków typu "phishing". Zabezpieczenie hasła przed tym wymaga podejmowania znacznych nakładów na zabezpieczenie urządzeń użytkownika, a także edukacji użytkowników.

W aspekcie technicznym podejmowane są działania, które mogą ograniczyć skuteczność keyloggerów. Należą w tym zakresie m. in. hasła maskowane, które polegają na oczekiwaniu od użytkownika jednorazowo tylko wybranych znaków z hasła i z każdą zmianą zmienianie tego zestawu znaków. W takiej sytuacji nie jest wystarczające jednorazowe podsłuchanie wprowadzonych danych, gdyż podczas kolejnego uwierzytelniania wymagane będzie inny zestaw znaków.

.. figure:: ../img/authentication/masked-password.png

    Przykładowy ekran uwierzytelniania z wykorzystaniem hasła maskowanego (T-Mobile Usługi bankowe, styczeń 2016 roku) (opr. własne)

.. _password_policy:

Polityki haseł
^^^^^^^^^^^^^^

W zakresie organizacyjnym, który często wspierany jest także odpowiednimi rozwiązaniami technicznymi wprowadzone są polityki haseł. Obejmują one najczęsciej zagadnienia dotyczącego ponownego wykorzystania tych samych haseł w różnych systemach komputerowych, złożoność haseł i częstotliwość ich zmiany.

Warto w tym miejscu dostrzec, że nieadekwatna polityka haseł może prowadzić do ograniczenia bezpieczeństwa, a nie jego poprawy. Moim zdaniem dotyczy to w szczególności wymogu częstej zmiany haseł bez wdrożenia alternatywnych rozwiązań. Częsta zmiana haseł rodzi kilka zasadniczych problemów. Nie wszyscy posiadają zdolność zapamiętania złożonych haseł, co prowadzi do ponownego używania haseł w wielu miejscach lub stosowania haseł schematycznych z wykorzystaniem prostych transformacji. W takim wypadku zbyt skomplikowane i często zmieniane hasła prowadzą do zapisywania ich w jawnej formie, co może narażać na ich kradzież.

Odnośnie schematycznych haseł warto w tym miejscu dostrzec uwagi Lorrie Cranor z amerykańskiej Federalnej Komisji Handlu (FTC), która opisała na stronie FTC badania przeprowadzone na University of North Carolina (w Chapel Hill). Badacze pozyskali ponad 51 tys. hashy haseł do 10 tys. nieaktywnych kont studentów i pracowników, na których wymuszano zmianę hasła co 3 miesiące. Po ich analizie stwierdzono, że dla 17% kont znajomość poprzedniego hasła pozwalała na zgadnięcie kolejnego hasła w mniej niż 5 próbach [#f7]_ [#f8]_.

Podobne wątpliwości co do skuteczności polityki zmiany haseł wyrażono w badaniach tego problemu przeprowadzonych na Carleton University [#f9]_ . Dostrzeżono w nich, że w przypadku wielu ataków jednorazowy dostęp do systemu umożliwia natychmiastowe pozyskanie plików docelowych, założenie tylnych drzwi, zainstalowanie  oprogramowania typu keylogger lub innego trwałego, złośliwego oprogramowania, które późniejsze zmiany hasła uczyni nieskutecznymi. Autorzy nawet stawiają tezę, że prawdziwe korzyści z wymuszania zmiany haseł nie rekompensują związanych z tym uciążliwości.

Sytuacja ta oznacza, że nie można wprowadzić generalnej reguły, która uzasadniałaby określoną politykę haseł, wymaga to każdorazowo indywidualnej analizy z strony administratora systemu komputerowego.

Powyższa analiza pokazuje tylko niektóre z słabości uwierzytelniania z wykorzystaniem haseł i uzasadnia konieczność poszukiwania bezpieczniejszych form uwierzytelniania w celu zrealizowania współcześnie procesu uwierzytelniania na adekwatnym poziomie. Utrata poufności haseł - związana zarówno z atakimi po stronie użytkownika i serwera, a także procesu samej komunikacji - stanowią codzienność.

Kryptografia asymetryczna
-------------------------

Dość powszechnie - stosowane zarówno w środowisku przemysłowym i domowym - zwłaszcza w środowisku systemu operacyjnego Linux jest uwierzytelnianie z wykorzystaniem klucza publicznego. Ma to miejsce m. in. dzięki powszechnemu wykorzystaniu protokołu SSH2, którego standard wymaga implementacji tej formy uwierzytelniani [#SSH_public_key]_. Uwierzytelnienie klienta odbywa się po negocjacji warunków połączenia i uwierzytelnienie serwera. Polega na przesłaniu pakietu o następującej strukturze::

  byte      SSH_MSG_USERAUTH_REQUEST
  string    user name
  string    service name
  string    "publickey"
  boolean   TRUE
  string    public key algorithm name
  string    public key to be used for authentication
  string    signature

Zawarty podpis cyfrowy składany jest na następującej wiadomości::

  string    session identifier
  byte      SSH_MSG_USERAUTH_REQUEST
  string    user name
  string    service name
  string    "publickey"
  boolean   TRUE
  string    public key algorithm name
  string    public key to be used for authentication

Po odebraniu tak sformułowanego pakietu serwer musi zweryfikować czy przedstawiony klucz publiczny jest właściwy do uwierzytelnia, co najczęściej odbywa się poprzez weryfikacje bazy uprawnionych kluczy zawartej w pliku ``.ssh/authorized_keys``. Jak również serwer musi zweryfikować czy złożony podpis jest prawidłowy. 

Należy objaśnić, że przedstawiony identyfikator sesji (``session identifier``) został ustalony podczas wcześniejszych etapów negocjacji połączenia. Wartość ta ulega zmianie wraz z każdym połączeniem lub częściej. Dzięki czemu ten jeden pakiet stanowi całą komunikacje uwierzytelniania, która jest odporna na atak powtórzenia.

Klucz publiczny jest składowany często na komputerze użytkownika, co oznacza że ten sposób uwierzytelniania należy sklasyfikować jako oparty na "czymś co masz" (`authentication_form`_). Należy od razu jednak podkreślić, że często klucz prywatny jest przechowywany w formie cyfrowej i wymaga wprowadzenia hasła przed tym jak wygenerowanie podpisu cyfrowego stanie się ożliwe.

Ta forma uwierzytelniania nie jest wrażliwa na sytuacje, gdy poufność klucza prywatnego użytkownika zostanie naruszona. Może to mieć miejsce w sytuacji ataku złoślwiego oprogramowania na komputer użytkownika. Niedostateczne w takim przypadku może okazać się szyfrowanie hasła, gdyż podczas próby użycia klucza hasło lub sam klucz może zostać przejęta przez złośliwe oprogramowanie z pamięci komputera.

Pozbawiona jest natomiast zagrożenia, że użycie tych samych danych dostępowych stanowić będzie zagrożenie dla samego użytkownika. Nie ma zatem konieczności - analogicznie do współdzielonego sekretu - wprowadzenia rozwiązań, które chroniłyby poufność kluczy po stronie system uwierzytelniającego, a w szczególności przechoywanie danych z wykorzystaniem funkcji skrótu (:ref:`hashing`).

Istotne jest jedynie zagwarantowanie integralności bazy uprawnionych kluczy, gdyż jego modyfikacja, w szczególności dopisanie kluczy obcych może prowadzić do obejścia zabezpieczeń. 

.. todo:: 
  Trusted Platform Module - przeanalizować znaczenie dla przechowywania kluczy publicznych
  Karty chipowe z kluczami kryptograficznymi

Universal 2nd Factor
^^^^^^^^^^^^^^^^^^^^

Jedną z form ochrony kluczy prywatnych wykorzystywanych do uwierzytalniania przed atakim złośliwego oprogramowania może stanowić wykorzystanie do tego celu dedykowanych układów elektronicznych, które stanowić będą sprzętowe zabezpieczenie przed naruszeniem poufności zawartego w układzie klucza prywatnego. Wykorzystanie ich jednak wymaga odpowiedniego sprzętu, oprogramowania (sterowników), a w przypadku aplikacji działających w przeglądarce także wsparcie z strony przeglądarki internetowej.

W ostatnim czasie rosnącą popularność zyskuje otwarty standard `Universal 2nd Factor` (U2F). Opisuje sposób komunikacji stron internetowych z dedykowanym tokenem (kluczem sprzętowych) podłączonym z wykorzystaniem powszechnie dostępnego w komputerach portu USB bez wykorzystania dodatkowych sterowników za pośrednictwem przeglądarki w celu przeprowadzenia procesu uwierzytelniania. Stanowi zatem kompleksowe rozwiązanie umożliwiające przechowywanie kluczy kryptograficznych w sprzętowym tokenie i wykorzystanie ich w aplikacjach działających w przeglądarce internetowej w celu uwierzytelniania.

Standard ten został początkowo zaprojektowany przez firmę Google, lecz teraz jest zarządzany przez FIDO (Fast Identity Online) Alliance. Członkami FIDO Alliance są także m. in. Microsoft, Mastercard, Visa, PayPal, Discover, Samsung i BlackBerry [#yubico_pcworld]_. 

Standard ten został wdrożony przez czołowych dostawców usług sieciowych, a jego popularność rośnie. Google ogłosiło jego obsługę w październiku 2014 roku [#u2f_google]_, w sierpniu 2015 roku Dropbox [#u2f_dropbox]_, w październiku 2015 roku GitHub [#u2f_github]_, w czerwcu 2016 roku BitBucket [#u2f_bitbucket]_,w lutym 2017 roku Facebook [#u2f_facebook]_. Można zatem przyjąć, że staje się fakycznie standardem.

Dostępne są liczne urządzenia o niewygórowanych cenach. Koszt indywidualnej sztuki wynosi około 70 zł [#yubico_cena]_. Samodzielny montaż pozwala skonstruowanie urządzenia w cenie poniżej 25 zł / sztuka.

.. todo::
  Przedstawić wnioski i wyniki z projektu Koła Naukowego Programistów - http://www.wns.uph.edu.pl/strona-glowna/aktualnosci/656-zapowiedz-nowego-projektu-w-zakresie-bezpieczenstwa-komputerowego-kola-naukowego-programistow

Zapewniona jest także odpowiednia obsługa z strony popularnych przeglądarek internetowych - Google Chrome w wersjach 38 i Opera od wersji 40 domyślnie. Natomiast Firefox wymaga dedykowanej wtyczki [#u2f_firefox_bug]_, a wbudowana obsługa jest zaplanowana na 1 kwartał 2017 roku [#u2f_firefox_support]_.

.. _2factor:

Dwuskładnikowe uwierzytelnienie
-------------------------------

W nowoczesnych systemach komputerowych przed uzyskaniem dostępu często stosuje się uwierzytelniani wieloskładnikowe (*multi-factor authentication*), w szczególności dwuskładnikowe (*two-factor authentication*), czyli łączące dwie różne metody uwierzytelniania.

Jest to praktykowane, ponieważ w komunikacji elektronicznej stosowanie samego hasła wiąże się z różnego rodzaju ryzykiem, a wykorzystanie kilku form uwierzytelnienia może ograniczać skutki przechwycenia (keylogger), albo podsłuchania (sniffer) hasła po którym przestaje ono być wówczas znane wyłącznie osobie uprawnionej, zaś kradzież może pozostać niezauważona. Ryzyko to można ograniczyć, wprowadzając dodatkowy składnik uwierzytelniania wykorzystując kilka form autoryzacji jednocześnie. 

Najpopularniejszym rozwiązaniem jest - łacznie z hasłem - wykorzystanie m. in.:

* sprzętowego tokenu istniejącego w jednym, unikatowym egzemplarzu, więc jego użycie wymaga fizycznego dostępu lub kradzieży, która zostanie zauważona (cecha coś co masz),
* jednorazowych kodów generowanych programowo (TOTP), a także przesłanych z użyciem alternatywnego kanału komunikacji (SMS, połączenia, e-mail).

W ostatnich latach zauważalna jest popularność takich rozwiązań w powszechnych usługach internetowych. Obsługę dla wieloskładnikowego uwierzytelniania zapewnia usługa poczty Gmail i Outlook.com, serwisy społecznościowe Facebook i Google+, a nawet platformy gier Battle.net i Steam. Istnieją dedykowane strony internetowe, których celem jest popularyzacja takich rozwiąząń - `TwoFactorAuth.info.org <http://TwoFactorAuth.info.org>`_  i `Dongleauth.info <https://Dongleauth.info>`_ . Po pierwsze, poprzez promocję wśród konsumentów witryn internetowych, które wspierają bezpieczne formy uwierzytelniania. Po drugie, ma wywierać presję na dostawców usług internetowych, aby wdrożyli oni w optymalny sposób bezpieczne formy uwierzytelniania.

W Polsce dostępność takich rozwiązań rośnie. Analiza witryny Dwa-Skladniki.pl wskazuje, że żaden krajowy dostawa usług pocztowych nie oferuje takich form uwierzytelniania. Ani Interia, ani O2.pl, ani WP.pl, ani Onet.pl nie oferują takich rozwiązań. Zainteresowane osoby zmuszone są do korzystania z usług w/w zagranicznych gigantów. Natomiast spośród firm hostingowych jakąkolwiek formę dwuskładnikowego uwierzytelniania zapewnia wyłącznie MyDevil.net. Jeżeli chce się mieć bezpieczny hosting w Polsce – należy samemu nim zarządzać. Wówczas można skorzystać z usług OVH lub e24cloud [#2fa_analiza_pl]_. 

Warto zwrócić uwagę, że standardy regulacyjne dotyczące dostępu do systemów rządu federalnego USA wymagają nawet używania uwierzytelniania wieloskładnikowego, aby uzyskać dostęp do krytycznych zasobów IT, na przykład podczas logowania do urządzeń sieciowych podczas wykonywania zadań administracyjnych oraz przy dostępie do uprzywilejowanego konta. Również publikacja „The Critical Security Controls for Effective Cyber Defense”, wydana przez instytut SANS, przygotowana przez rządowe agencje i komercyjnych ekspertów śledczych i d/s bezpieczeństwa stanowczo zaleca wykorzystanie takich rozwiązań [#f2]_.

.. rubric:: Footnotes

.. [#citation_needed] Potrzebne źródło

.. [#f1] Tomasz Mielnicki, Franciszek Wołowski, Marek Grajek, Piotr Popis, Identyfikacja i uwierzytelnianie w usługach elektronicznych, Przewodnik Forum Technologii Bankowych przy Związku Banków Polskich, Warszawa, 2013, http://zbp.pl/public/repozytorium/dla_bankow/rady_i_komitety/technologie_bankowe/publikacje/Przewodnik_Identyfikacja_i_uwierzytelnianie_strona_FTB.pdf [dostęp 23 grudnia 2016 roku]

.. [#f2] CIS Controls for Effective Cyber Defense Version 6.0, SANS Institute, https://www.cisecurity.org/critical-controls.cfm [dostęp 16 marca 2016 roku]

.. [#f7] Lorrie Cranor, Time to rethink mandatory password changes, 2 marca 2016 roku, Federalna Komisja Handlu, ftc.gov, https://www.ftc.gov/news-events/blogs/techftc/2016/03/time-rethink-mandatory-password-changes [dostęp 16 marca 2016 roku]

.. [#f8] Brian Barrett, Want Safer Passwords? Don’t Change Them So Often, Wired.com 3.10.2016, http://www.wired.com/2016/03/want-safer-passwords-dont-change-often/ [dostęp 16 marca 2016 roku]

.. [#f9] Sonia Chiasson, P. C. van Oorschot, Quantifying the security advantage of password expiration policies, Designs, Codes and Cryptography, 2015, Volume: 77, Issue 2-3, 401-4

.. [#f_dropbox] Devdatta Akhawe, How Dropbox securely stores your passwords, Dropbox Tech blog, https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/ [dostęp 2 stycznia 2016 roku]

.. [#sekurak_kompedium1] Adrian Vizzdoom Michalczyk, Kompendium bezpieczeństwa haseł – atak i obrona (część 1.), Sekurak.pl 1 lutego 2013 roku, https://sekurak.pl/kompendium-bezpieczenstwa-hasel-atak-i-obrona/ (dostęp: 27 stycznia 2017 roku)

.. [#HTTPS_Usage] Transparency Report, Google, https://www.google.com/transparencyreport/https/metrics/?hl=en (dostęp: 4 lutego 2017 roku)

.. [#HTTPS_Warning] Emily Schechter, Moving towards a more secure web, Google Security Blog 8 września 2016 roku, https://security.googleblog.com/2016/09/moving-towards-more-secure-web.html (dostęp: 4 lutego 2017 roku)

.. [#HTTPS_Firefox] Tanvi Vyas, Peter Dolanjski, Communicating the Dangers of Non-Secure HTTP, Mozilla Security Blog, https://blog.mozilla.org/security/2017/01/20/communicating-the-dangers-of-non-secure-http/ (4 lutego 2017 roku)

.. [#SSH_public_key] "The only REQUIRED authentication 'method name' is "publickey" authentication.  All implementations MUST support this method; however, not all users need to have public keys, and most local policies are not likely to require public key authentication for all users in the near future." (Public Key Authentication Method: "publickey" [w:] T. Ylonen, RFC 4252 - The Secure Shell (SSH) Authentication Protocol)

.. [#Yubico_pcworld] Tony Bradley, How a USB key drive could remove the hassles from two-factor authentication, PCWorld 21 październik 2014 roku, http://www.pcworld.com/article/2836692/how-the-fido-alliances-u2f-could-simplify-two-factor-authentication.html (dostęp 4 luty 2017 roku)

.. [#Yubico_cena] Cena urządzenia FIDO U2F Security Key na Yubico Store, https://www.yubico.com/store/, dostęp 4 luty 2017 roku)

.. [#u2f_google] Nishit Shah, Strengthening 2-Step Verification with Security Key, Google Security Blog, 21 październik 2014 roku, https://security.googleblog.com/2014/10/strengthening-2-step-verification-with.html (dostep 4 luty 2017 roku)

.. [#u2f_dropbox] Patrick Heim, Jay Patel, Introducing U2F support for secure authentication, Dropbox Blog 12 sierpnia 2015 roku, https://blogs.dropbox.com/dropbox/2015/08/u2f-security-keys/ (dostęp 4 luty 2017 roku)

.. [#u2f_github] Ben Toews, GitHub supports Universal 2nd Factor authentication, GitHub Blog, https://github.com/blog/2071-github-supports-universal-2nd-factor-authentication (dostęp 4 luty 2017 roku)

.. [#u2f_bitbucket] TJ Kells, Universal 2nd Factor (U2F) now supported in Bitbucket Cloud, 22 czerwca 2016, Bitbucket Blog, https://blog.bitbucket.org/2016/06/22/universal-2nd-factor/ (dostęp 4 luty 2017 roku)

.. [#u2f_facebook] Brad Hill, Security Key for safer logins with a touch, Facebook Security, https://www.facebook.com/notes/facebook-security/security-key-for-safer-logins-with-a-touch/10154125089265766 (dostęp 4 luty 2017 roku)

.. [#u2f_firefox_bug] Bug 1065729 - Implement the FIDO Alliance u2f javascript API, Mozilla Bugzilla, https://bugzilla.mozilla.org/show_bug.cgi?id=1065729 (online: 4 luty 2017 roku)

.. [#u2f_firefox_support] Jcjones, Security/CryptoEngineering, Mozilla Wiki, https://wiki.mozilla.org/index.php?title=Security/CryptoEngineering&oldid=1159535 (dostęp 4 luty 2017 roku)

.. [#2fa_analiza_pl] Analiza została przeprowadzona w dniu 4 lutego 2017 roku poprzez przegląd całości treści opublikowanych na stronie Dwa-Skladniki.pl
