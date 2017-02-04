.. _readme:

.. _introduction:

*******************************
Wstęp
*******************************

Często w obrębie jednej instytucje funkcje wiele niezależnych aplikacji sieciowych. Każda z nich posiada własne mechanizmy identyfikacji i uwierzytelniania użytkowników, które są oparte na hasło. 

Aby zagwarantować bezpieczne uwierzytelnianie w dużej liczbie niezależnych systemów warto ten proces przenieść do dedykowanego funkcjonalnego, wysoce dostępnego systemu komputerowego, który będzie gwarantować jednolity, wysoki poziom bezpieczeństwa, a także zagwarantuje możliwość skutecznych audytów bezpieczeństwa, wczesnego wykrywania nadużyć i odpowiedzi na nowe oczekiwania w zakresie nowoczesnych form uwierzytelniania, w tym uwierzytelniania wieloskładnikowego.

Ponieważ nie został zidentyfikowany dedykowany otwartoźródłowy system, który mógłby zostać wdrożony w organizacji pojawiła się potrzeba stworzenia własnego systemu, który będzie wspomagać inne aplikacje w procesie rejestracji i uwierzytelniania użytkowników stanowiąc dedykowany *Identify Provider* zapewniając mechanizm *Single sign-on*.

.. _target:

Cel pracy
*********

Celem prezentowanej pracy było stworzenie otwartego i elastycznego systemu centralnego uwierzytelniania użytkownika, jak również ich rejestracji. Nowy proces logowania ma być jednolity w obrębie różnych systemów, a także wzbogacony o dodatkowe formy uwierzytelniania.

System ten ma przejąć zadanie uwierzytelniania z systemów dotychczas działających w organizacji, a wspierających tylko prymitywne formy uwierzytelniania, powstałych w oparciu o rozbieżne technologie tworzące indywidualne bazy tożsamości i danych uwierzytelniających. Aby zapewnić jego rzeczywiste wykorzystanie system winien być łatwy i wygodny w integracji z dotychczas istniejącymi systemami, a - zważywszy na wygodę użytkownika - powinien mieć formę aplikacji internetowej. Powinien mieć charakter modularny w zakresie form uwierzytelniania, aby umożliwiał łatwe dodawanie nowych form uwierzytelniania wraz z pojawiającymi się zagrożeniami, potrzebami i możliwości.

Praca uwzględnia także przygotowanie komponentów do dotychczas funkcjonujących systemów, które umożliwią przeniesienie procesu uwierzytelniania do centralnego systemu. Stanowić to będzie potwierdzenie skuteczności protokołu integracji, a także spełnienia jego wymagań w zakresie prostoty i wygody.

Idea centralnej aplikacji wynika z analizy potrzeb Stowarzyszenie Sieć Obywatelska - Watchdog Polska, które chciałoby - w celu poprawy swojego bezpieczeństwa - stworzyć możliwość utworzenia zintegrowanego konta użytkownika dla członków zespołu, ale także dla odbiorców swoich działań (wolontariuszy, aktywistów itp.). Podstawowym celem wdrożenia systemu jest podniesienie poziomu bezpieczeństwa rozproszonych systemów komputerowych i zapewnienie w możliwie wielu aplikacjach bezpiecznych form uwierzytelniania.

.. _creating:

Tworzenie projektu
*********************************

Koncepcja systemu została opracowane przez autora na podstawie osobistych doświadczeń [#f1]_ podczas pełnienia funkcji Administratora Bezpieczeństwa Informacji (ABI) w Stowarzyszeniu Sieć Obywatelska - Watchdog Polska.

Autor rozpoczął opracowanie projektu od analizy formy uwierzytelniania (:ref:`authentication`), a następnie rozpatrzył dotychczasowe standardowych form delegacji uwierzytelniania (:ref:`protocol`). Rozpatrzone zostały wymagania prawne mogące mieć wpływa na sposób funkcjonowania aplikacji (:ref:`law`). Po wnikliwej analizie sformował główne założenia aplikacji (:ref:`requirements`).

Główny komponent aplikacji zrealizowano w języku Python z wykorzystaniem frameworka `Django`_. Podczas pracy został wykorzystano liczne narzędzia wspomagające prace. Do zarządzania projektem wykorzystano `GitHub`_, który zapewniał także hosting dla wykorzystanego systemu kontroli wersji Git. Systemy te były z sobą zintegrowane. Z systemem kontroli wersji był zintegrowany także system ciągłej integracji `Travis CI`_. W przypadku środowiska testowego został wykorzystany hosting `Heroku`_, który zapewnił możliwość weryfikację współpracy komponentów w sieci Internet z wykorzystaniem różnych aplikacji klienckich.

.. _Django: https://djangoproject.com/

.. _GitHub: https://www.github.com/

.. _Travis CI: https://travis-ci.org/

.. _Heroku: http://heroku.com/

.. rubric:: Footnotes

.. [#f1] `Wpis Karola Breguła na portalu Facebook z dnia 3 grudnia 2016 roku <https://www.facebook.com/adam.dobrawy/posts/592261217627776>`_
