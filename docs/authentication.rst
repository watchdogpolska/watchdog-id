.. _authentication:

****************
Uwierzytelnianie
****************

W tym dokumencie opiszemy formy uwierzytelniania, z szczególnym uwzględnieniem dwuskładnikowego uwierzytelniania. Założenia leżące u jego podstaw, korzyści, ryzyko, ograniczenia, a także przeanalizujemy formy dwuskładnikowego dokonując analizy ich słabych i mocnych stron.

.. _authentication_intro:

Uwagi wstępne
*************

Na samym wstępinie niniejszych rozważań warto uporządkować terminologie odwołując się do literatury przedmiotu[*]_:

> Usługi elektroniczne zakładające interakcję z użytkownikiem wymagają zwykle identyfikacji użytkownika i jego uwierzytelnienia. Zgodnie z terminologią, identyfikację rozumie się jako nadanie (przypisanie) identyfikatora do osoby oraz deklarację (stwierdzenie) tożsamości osoby poprzez przedstawienie indentyfikatora. Taki identyfikator jednoznacznie tą osobę identyfikuje i stanowi elektroniczną tożsamość użytkownika w tymże środowisku. Sama identyfikacja pozwala zatem na stwierdzenie „o kogo chodzi”, ale nie potwierdza, że użytkownik danej e-usługi jest faktycznie tą osobą, która została zadeklarowana i zidentyfikowana. Do tego potwierdzenia służy właśnie uwierzytelnienie, polegające na dostarczeniu dowodów, że użytkownik jest właśnie tą zidentyfikowaną osobą (nikt się nie podszywa). W szczególnych przypadkach identyfikacja i uwierzytelnienie może przebiegać jednocześnie (np. gdy nasz identyfikator jest tajny, stanowiąc jednocześnie „hasło”), ale zasadniczo są to dwa różne procesy. Z kolei pod pojęciem autoryzacji (często mylonej z uwierzytelnieniem i niepoprawnie nazywanej „autentykacją”) rozumie się proces nadania określonych uprawnień, z których następnie poprawnie zidentyfikowana i uwierzytelniona osoba będzie mogła korzystać.

Metody uwierzytelniania można podzielić na wykorzystujące:

* coś co wiesz (something you know) – informacja będąca w wyłącznym posiadaniu uprawnionego podmiotu, na przykład hasło lub klucz prywatny;
* coś co masz (something you have) – przedmiot będący w posiadaniu uprawnionego podmiotu, na przykład generator kodów elektronicznych (token), telefon komórkowy (kody SMS, połączenie autoryzacyjne) lub klucz analogowy,
* coś czym jesteś (something you are) – metody biometryczne.

.. todo:: Zapoznać się z:
    https://pages.nist.gov/800-63-3/sp800-63b.html DRAFT NIST Special Publication 800-63B Digital Authentication Guideline
    Bring Your Own Authentication (BYOA) 

.. _password_policy:

Polityka haseł
**************

Warto dostrzec, że nieadekwatna polityka haseł może prowadzić do ograniczenia bezpieczeństwa, a nie jego poprawy. Moim zdaniem dotyczy to w szczególności wymogu częstej zmiany haseł bez wdrożenia alternatywnych rozwiązań. Częsta zmiana haseł rodzi kilka zasadniczych problemów. Nie wszyscy posiadają zdolność zapamiętania złożonych haseł, co prowadzi do ponownego używania haseł w wielu miejscach lub stosowania haseł schematycznych z wykorzystaniem prostych transformacji. W takim wypadku zbyt skomplikowane i często zmieniane hasła prowadzą do zapisywania ich w jawnej formie, co może narażać na ich kradzież.

Odnośnie schematycznych haseł warto w tym miejscu dostrzec uwagi Lorrie Cranor z amerykańskiej Federalnej Komisji Handlu (FTC), która opisała na stronie FTC badania przeprowadzone na University of North Carolina (w Chapel Hill). Badacze pozyskali ponad 51 tys. hashy haseł do 10 tys. nieaktywnych kont studentów i pracowników, na których wymuszano zmianę hasła co 3 miesiące. Po ich analizie stwierdzono, że dla 17% kont znajomość poprzedniego hasła pozwalała na zgadnięcie kolejnego hasła w mniej niż 5 próbach [#f7]_ [#f8]_.

Podobne wątpliwości co do skuteczności polityki zmiany haseł wyrażono w badaniach tego problemu przeprowadzonych na Carleton University [#f9]_ . Dostrzeżono w nich, że w przypadku wielu ataków jednorazowy dostęp do systemu umożliwia natychmiastowe pozyskanie plików docelowych, założenie tylnych drzwi, zainstalowanie  oprogramowania typu keylogger lub innego trwałego, złośliwego oprogramowania, które późniejsze zmiany hasła uczyni nieskutecznymi. Autorzy nawet stawiają tezę, że prawdziwe korzyści z wymuszania zmiany haseł nie rekompensują związanych z tym uciążliwości.

Sytuacja ta oznacza, że nie można wprowadzić generalnej reguły, która uzasadniałaby określoną politykę haseł, wymaga to każdorazowo indywidualnej analizy administratora.

.. _2factor:

Dwuskładnikowe uwierzytelnienie
*******************************

W nowoczesnych systemach komputerowych przed uzyskaniem dostępu często stosuje się jednak uwierzytelniani wieloskładnikowe (*multi-factor authentication*), w szczególności dwuskładnikowe (*two-factor authentication*), czyli łączące dwie różne metody uwierzytelniania.

Jest to praktykowane, ponieważ w komunikacji elektronicznej stosowanie samego hasła wiąże się z różnego rodzaju ryzykiem, a wykorzystanie kilku form uwierzytelnienia może ograniczać skutki przechwycenia (keylogger), albo podsłuchania (sniffer) hasła po którym przestaje ono być wówczas znane wyłącznie osobie uprawnionej, zaś kradzież może pozostać niezauważona. Ryzyko to można ograniczyć, wprowadzając dodatkowy składnik uwierzytelniania wykorzystując kilka form autoryzacji jednocześnie np.:

* token istniejący w jednym, unikatowym egzemplarzu, więc jego użycie wymaga fizycznego dostępu lub kradzieży, która zostanie zauważona (cecha coś co masz);
* użycie tokenu wymaga dodatkowo podania hasła (np. w postaci kodu PIN), więc bez jego znajomości token będzie nieprzydatny, nawet w razie kradzieży (cecha coś co wiesz).

Uwierzytelnienie dwuskładnikowe stosuje większość banków internetowych, usługa poczty Gmail, Facebook, Apple, platformy gier (Battle.net) i wiele innych. Powszechnie dostępne są interfejsy programistyczne do jednorazowych haseł przesyłanych za pomocą SMS, tokeny sprzętowe, jak i programowe generatory haseł TOTP (Time-based One-Time Password Algorithm) np. Google Authenticator.

Warto zwrócić uwagę, że standardy regulacyjne dotyczące dostępu do systemów rządu federalnego USA wymagają nawet używania uwierzytelniania wieloskładnikowego, aby uzyskać dostęp do krytycznych zasobów IT, na przykład podczas logowania do urządzeń sieciowych podczas wykonywania zadań administracyjnych oraz przy dostępie do uprzywilejowanego konta. Również publikacja „The Critical Security Controls for Effective Cyber Defense”, wydana przez instytut SANS, przygotowana przez rządowe agencje i komercyjnych ekspertów śledczych i d/s bezpieczeństwa stanowczo zaleca wykorzystanie takich rozwiązań [*]_.

.. _existing_solutions:

Istniejące standardy uwierzytelniania
*************************************

W tym dokumencie opisze istniejące rozwiązania SSO, które mogą stanowić bazę dla szerszego wdrożenia. Zostaną one krótko przedstawione ich założenia, ich zakres, słabe i mocne strony.

W szczególnośći zostaną przedstawione takie mechanizmy jak:

* tradycyjne podejście z LDAP-em - Uniwersytet Przyrodniczo-Humanistyczny w Siedlcach,
* single sign-on (SSO)

    - SAML
    - OAuth 1.0
    - OAuth 2.0
    - OpenID 2.0
    - OpenID Connect

.. rubric:: Footnotes

.. [*] Tomasz Mielnicki, Franciszek Wołowski, Marek Grajek, Piotr Popis, Identyfikacja i uwierzytelnianie w usługach elektronicznych, Przewodnik Forum Technologii Bankowych przy Związku Banków Polskich, Warszawa, 2013, http://zbp.pl/public/repozytorium/dla_bankow/rady_i_komitety/technologie_bankowe/publikacje/Przewodnik_Identyfikacja_i_uwierzytelnianie_strona_FTB.pdf [dostęp 23 grudnia 2016 roku]
.. [*] CIS Controls for Effective Cyber Defense Version 6.0, SANS Institute, https://www.cisecurity.org/critical-controls.cfm [dostęp 16 marca 2016 roku]

.. [#f7] Lorrie Cranor, Time to rethink mandatory password changes, 2 marca 2016 roku, Federalna Komisja Handlu, ftc.gov, https://www.ftc.gov/news-events/blogs/techftc/2016/03/time-rethink-mandatory-password-changes [dostęp 16 marca 2016 roku]

.. [#f8] Brian Barrett, Want Safer Passwords? Don’t Change Them So Often, Wired.com 3.10.2016, http://www.wired.com/2016/03/want-safer-passwords-dont-change-often/ [dostęp 16 marca 2016 roku]

.. [#f9] Sonia Chiasson, P. C. van Oorschot, Quantifying the security advantage of password expiration policies, Designs, Codes and Cryptography, 2015, Volume: 77, Issue 2-3, 401-4
