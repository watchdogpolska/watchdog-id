.. _requirements:

*****************
Wymagania systemu
*****************

System ma zostać zaprojektowany w taki sposób, aby możliwe było jego wdrożenie przez różne podmioty. Jednak jego podstawowym odbiorcą jest Stowarzyszenie Sieć Obywatelska - Watchdog Polska. Jest ona niezależna organizacją społeczną, która aktywnie wykorzystuje w swojej pracy nowoczesne technologie. Posiada rozproszoną strukturę, gdzie podstawową komunikacji stanowią różnorodne aplikacje internetowe. Autor niniejszej publikacji jest jej członkiem. Stowarzyszenie swoje cele działania określa jako: 

    Pilnujemy, żeby ludzie wiedzieli, co robi władza. Uczymy mieszkańców, że mogą pytać urzędy o to, dlaczego zlikwidowano szkołę, ile wydano na festyn czy gdzie planowana jest budowa wiatraków. Udzielamy tysięcy porad i setki razy chodzimy do sądu. Dzięki temu coraz więcej ludzi wie, że ma prawo pytać urzędy, te zaś wiedzą, że muszą odpowiadać.

Ze względu na dotychczasowy stan, który musi być uwzględniony w projektowaniu niniejszej aplikacji przyjęto, że  architektura aplikacja będzie składać się z kilku komponentów. Jeden z nich będzie miał charakter centralny, a pozostałe będą uzupełniać dotychczas funkcjonujące aplikacje wzbogacając je o dodatkowe formy uwierzytelniania.

Centralny moduł uwierzytelniania i zarządzania użytkownikami stanowić będzie `odrębną usługę Watchdog.ID <https://github.com/watchdogpolska/watchdog-id>`_. Usługa ta będzie bazować na frameworku Django w języku Python 3.5. Pełnić będzie funkcje dostawcy tożsamości tak jak jest dla wielu stron Facebook ("Zaloguj przez Facebooka"). Jednak o wiele lepiej cel odzwierciedla odwołanie się do konta Google, które raz utworzone jest dostępne w szeregach systemów firmy Google w sposób niemal niezauważalny.

Ze względu na praktyczne wdrożenie aplikacji równie istotne co centralny moduł uwierzytelniania jest zapewnienie integracji z zewnętrznymi komponentami. Stowarzyszeniu wykorzystuje aplikacje w różnych technologiach. Są to m. in. aplikacje PHP, w tym m. in. ownCloud, liczne instancje Wordpressów. Jak również autorskie aplikacje Python z wykorzystaniem frameworka Django, które są otwarto źródłowe. Należy dla nich opracować integracje z Watchdog.ID. 

System Watchdog.ID wymaga prac, aby zapewnić adekwatny poziom zabezpieczeń, wygląd i przyjazność dla użytkownika. Adekwatny poziom zabezpieczeń wynika w szczególności z wykorzystania systemu do kontroli dostępu do danych osobowych. W tym celu w szczególności mają być wdrożone formy dwuskładnikowego uwierzytelniania. Przystępny wygląd i przyjazność dla użytkownika wynika z otwartego charakteru systemu, który będzie wykorzystywany także przez odbiorców działań Stowarzyszenia. Konieczne jest zatem zapewnienie, że każda osoba zainteresowana działaniami Stowarzyszenia będzie mogła skutecznie uwierzytelnić swoje konto w systemie Watchdog.ID. Szczegółowe wymagania w zakresie bezpieczeństwa w związku z ochroną danych osobowych zostały przeanalizowane w rozdziale :ref:`law`.

Wymagania funkcjonalne
----------------------

Wymagania niefunkcjonalne
-------------------------
