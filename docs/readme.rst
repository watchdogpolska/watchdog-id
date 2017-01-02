.. _readme:

.. _introduction:

*******************************
Wstęp
*******************************

Sieć Obywatelska - Watchdog Polska - podobnie jak wiele innych instytucji - w swojej działalności wykorzystuje szereg niezależnych aplikacji. Każda z nich posiada własne mechanizmy identyfikacji i uwierzytelniania użytkowników, które są oparte na hasło. Aby zagwarantować bezpieczne uwierzytelnianie w dużej liczbie niezależnych systemów warto ten proces przenieść do dedykowanego funkcjonalnego, wysoce dostępnego systemu komputerowego, który będzie gwarantować jednolity, wysoki poziom bezpieczeństwa, a także zagwarantuje możliwość skutecznych audytów bezpieczeństwa, wczesnego wykrywania nadużyć i odpowiedzi na nowe oczekiwania w zakresie nowoczesnych form uwierzytelniania, w tym uwierzytelniania wieloskładnikowego.

Ponieważ nie został zidentyfikowany dedykowany otwartoźródłowy system, który mógłby spełnić wymagania pojawiła się potrzeba stworzenia własnego systemu, który będzie wspomagać inne aplikacje w procesie rejestracji i uwierzytelniania użytkowników stanowiąc dedykowany *Identify Provider*.

.. Hasło to powinno być unikalne dla każdego systemu, a także mieć odpowiednią złożoność. Dodatkowo hasło w większości systemach powinno ulegać okresowej zmianie. Nie wszyscy posiadają zdolność zapamiętania złożonych haseł, co prowadzi do ponownego używania haseł w wielu miejscach lub stosowania haseł schematycznych z wykorzystaniem prostych transformacji, co stanowi zagrożenie dla tych systemów.
.. _target:

Cel pracy
*********************************

Celem prezentowanej pracy było stworzenie otwartego i elastycznego systemu centralnego uwierzytelniania użytkownika, jak również ich rejestracji. Nowy proces uwierzytelniania ma być jednolity w obrębie różnych systemów, a także wzbogacony o dodatkowe formy uwierzytelniania.

System ten ma przejąć zadanie uwierzytelniania z systemów dotychczas działających w organizacji wspierających tylko prymitywne formy uwierzytelniania, powstałych w oparciu o rozbieżne technologie tworzące indywidualne bazy tożsamości i `credentials`. Aby zapewnić jego rzeczywiste wykorzystanie system winien być łatwy i wygodny w integracji z dotychczas istniejącymi systemami, a - zważywszy na wygodę użytkownika - powinien mieć formę aplikacji internetowej. Powinien mieć charakter modularny, aby umożliwiał łatwe dodawanie nowych formę uwierzytelniania, w miarę pojawiających się zagrożeń, potrzeb i możliwości.

Praca uwzględnia także przygotowanie komponentów do popularnych systemów komputerowych, które umożliwią przeniesienie procesu uwierzytelniania do centralnego systemu. Stanowić to będzie potwierdzenie skuteczności integracji, a także spełnienia wymagań w zakresie prostoty i wygody.

Pomysł centralnej aplikacji wynika z analizy potrzeb Stowarzyszenie, która chciałaby - w celu poprawy swojego bezpieczeństwa - stworzyć możliwość utworzenia zintegrowanego konta użytkownika dla członków zespołu, ale także dla odbiorców swoich działań. Podstawowym celem wdrożenia systemu jest podniesienie poziomu bezpieczeństwa rozproszonych systemów komputerowych i zapewnienie w możliwie wielu aplikacjach bezpiecznych form uwierzytelniania.

.. _creating:

Tworzenie projektu
*********************************

Koncepcja i projekt systemu została opracowane przez autora na podstawie osobistych doświadczeń [#f1]_ podczas pełnienia funkcji Administratora Bezpieczeństwa Informacji (ABI) w Stowarzyszeniu Sieć Obywatelska - Watchdog Polska. Po ustaleniu głównych założeń (:ref:`requirements`) rozpoczął analizę dotychczasowych standardowych form delegacji uwierzytelniania (:ref:`protocol`), a następnie poddał analizie alternatywne wobec haseł formy uwierzytelniania (:ref:`authentication_intro`). 

Główny komponent aplikacji zrealizowano w języku Python z wykorzystaniem frameworka `Django`_. Podczas pracy został wykorzystano liczne narzędzia wspomagające prace. Do zarządzania projektem wykorzystano `GitHub`_, który zapewniał także hosting dla wykorzystanego systemu kontroli wersji Git. Systemy te były z sobą zintegrowane. Z systemem kontroli wersji był zintegrowany także system ciągłej integracji `Travis CI`_. W przypadku środowiska testowego został wykorzystany hosting `Heroku`_, który zapewnił możliwość weryfikację współpracy komponentów w sieci Internet.

.. _Django: https://djangoproject.com/

.. _GitHub: https://www.github.com/

.. _Travis CI: https://travis-ci.org/

.. _Heroku: http://heroku.com/

.. _requirements:

Wymagania systemu
*******************************

System ma zostać zaprojektowany w taki sposób, aby możliwe było jego wykorzystanie przez inne. Jednak jego podstawowym odbiorcą jest Stowarzyszenie Sieć Obywatelska - Watchdog Polska. Jest ona niezależna organizacją społeczną, która aktywnie wykorzystuje w swojej pracy nowoczesne technologie. Posiada rozproszoną strukturę, gdzie podstawową komunikacji stanowią różnorodne aplikacje internetowe. Autor niniejszej publikacji jest jej członkiem. Stowarzyszenie swoje cele działania określa jako: 
> Pilnujemy, żeby ludzie wiedzieli, co robi władza. Uczymy mieszkańców, że mogą pytać urzędy o to, dlaczego zlikwidowano szkołę, ile wydano na festyn czy gdzie planowana jest budowa wiatraków. Udzielamy tysięcy porad i setki razy chodzimy do sądu. Dzięki temu coraz więcej ludzi wie, że ma prawo pytać urzędy, te zaś wiedzą, że muszą odpowiadać.

Ze względu na dotychczasowy stan, który musi być uwzględniony w projektowaniu niniejszej aplikacji przyjęto, że  architektura aplikacja będzie składać się z kilku komponentów. Jeden z nich będzie miał charakter centralny, a pozostałe będą uzupełniać istniejące aplikacje wzbogacając je o dodatkowe formy uwierzytelniania.

Centralny moduł uwierzytelniania i zarządzania użytkownikami stanowić będzie `odrębną usługę Watchdog.ID <https://github.com/watchdogpolska/watchdog-id>`_. Usługa ta będzie bazować na frameworku Django w języku Python 3.5. Pełnić będzie funkcje dostawcy tożsamości tak jak jest dla wielu stron Facebook ("Zaloguj przez Facebooka"). Jednak o wiele lepiej cel odzwierciedla odwołanie się do konta Google, które raz utworzone jest dostępne w szeregach systemów firmy Google w sposób niemal niezauważalny.

Ze względu na praktyczne wdrożenie aplikacji równie istotne co centralny moduł uwierzytelniania jest zapewnienie integracji z zewnętrznymi komponentami. Stowarzyszeniu wykorzystuje aplikacje w różnych technologiach. Są to m. in. aplikacje PHP, w tym m. in. ownCloud, liczne instancje Wordpressów. Jak również autorskie aplikacje Python z wykorzystaniem frameworka Django, które są otwarto źródłowe. Należy dla nich opracować integracje z Watchdog.ID. 

System Watchdog.ID wymaga prac, aby zapewnić adekwatny poziom zabezpieczeń, wygląd i przyjazność dla użytkownika. Adekwatny poziom zabezpieczeń wynika w szczególności z wykorzystania systemu do kontroli dostępu do danych osobowych. W tym celu w szczególności mają być wdrożone formy dwuskładnikowego uwierzytelniania. Przystępny wygląd i przyjazność dla użytkownika wynika z otwartego charakteru systemu, który będzie wykorzystywany także przez odbiorców działań Stowarzyszenia. Konieczne jest zatem zapewnienie, że każda osoba zainteresowana działaniami Stowarzyszenia będzie mogła skutecznie uwierzytelnić swoje konto w systemie Watchdog.ID. Szczegółowe wymagania w zakresie bezpieczeństwa w związku z ochroną danych osobowych zostały przeanalizowane w rozdziale :ref:`law`.

.. rubric:: Footnotes

.. [#f1] `Wpis Karola Breguła na portalu Facebook z dnia 3 grudnia 2016 roku <https://www.facebook.com/adam.dobrawy/posts/592261217627776>`_
