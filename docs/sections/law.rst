.. _law:


********************
Uwarunkowania prawne
********************

W tym dokumencie opiszę uwarunkowania prawne związane z realizacją projektu. Zostaną przedstawione wymagania odnośnie bezpieczeństwa systemów, wymagane dzienniki, a także kwestie dotyczące ochrony danych osobowych. W zakresie ochrony danych osobowych zostanie w szczególności przeanalizowany stan obecny, a także perspektywa zmian i rozwoju. Przedstawione zostaną zarówno rozwiązania z zakresu twardego prawa (ang. `hard law`), jak również miekkie prawo (ang. `soft law`), w szczególności środowiska bezpieczeństwa informatycznego i organizacji pozarządowych zajmujących się prawem do prywatności.

Wdrożenie centralnego uwierzytelniania przez użytkowników może mieć wpływ na ich prawo do prywatności. Uważam, że konieczne jest we współczesnym świecie uwzględnienie ochrony danych osobowych, a szerzej wpływu na prawa do prywatności użytkowników już na etapie projektowania aplikacji, które mogą mieć na tą prywatność wpływ.

Prawo do prywatności
------------------------------

Postęp techniczny stwarzał i nadal stwarza nowe wyzwania dla skutecznej ochrony prywatności i danych osobowych. Zwraca się w literaturze, że łatwo można wykazać, iż niektóre specyficzne właściwości sieci komputerowych niejako z natury rzeczy wywołują nieznane wcześniej zagrożenia dla dóbr osobistych, skłaniając do poszukiwań środków zaradczych [#f1]_. 

Wobec ingerencji w prawo do prywatności należy zwrócić uwagę, że prawo do prywatności zostało w sposób wyraźny zagwarantowane w międzynarodowych aktach prawnych dotyczących ochrony praw człowieka (art. 12 Powszechnej Deklaracji Praw Człowieka, art. 17 Międzynarodowego Paktu Praw Obywatelskich i Politycznych oraz art. 8 Europejskiej Konwencji Praw Człowieka). Prawo do ochrony prawnej życia prywatnego zostało zagwarantowane w art. 47 Konstytucji, a niektóre uprawnienia szczegółowe składające się na treść tego prawa – ponadto w innych przepisach konstytucyjnych.

W kontekście tego projektu należy w szczególności zwrócić uwagę na autonomię informacyjną jednostki, którą gwarantuje  przede wszystkim art. 51 Konstytucji. W myśl art. 51 ust. 1, nikt nie może być obowiązany inaczej niż na podstawie ustawy do ujawniania informacji dotyczących jego osoby. Władze publiczne nie mogą pozyskiwać, gromadzić i udostępniać innych informacji o obywatelach niż niezbędne w demokratycznym państwie prawnym (art. 51 ust. 2). Zasady i tryb gromadzenia oraz udostępniania informacji określa ustawa (ust. 5). Zgodnie z ust. 3, każdy ma prawo dostępu do dotyczących go urzędowych dokumentów i zbiorów danych. Ograniczenie tego prawa może określić ustawa. Z kolei art. 51 ust. 4 stanowi, że każdy ma prawo do żądania sprostowania oraz usunięcia informacji nieprawdziwych, niepełnych lub zebranych w sposób sprzeczny z ustawą.

W literaturze zwraca się, że polski system prawny przyjmuje zasadę (prawo do) samodzielnego decydowania każdej osoby o ujawnianiu dotyczących jej informacji. Zasada ta odnosi się do wszelkich tego rodzaju informacji, w szczególności nie została zawężona do informacji szczególnego charakteru albo dotyczących szczególnych kwestii [#f2]_.

Użyte w analizowanych normach określenie "informacje dotyczące osoby" może być uznane za synonim pojęcia danych osobowych [#f3]_.

Ochrona danych osobowych
------------------------

U podstaw ustawy o ochronie danych osobowych z 1997 r. (dalej: u.o.d.o.) [#f4]_ leży koncepcja, iż przetwarzanie danych dopuszczalne jest tylko w przypadkach i na warunkach wskazanych przez ustawę, równocześnie wykorzystanie danych osobowych nie może być zabronione, o ile odbywa się z poszanowaniem ustawy. 

Ustawa wprowadza dwie podstawowe kategorie danych osobowych - tzw. dane zwykłe i dane sensytywne (wrażliwe), których ujawnienie lub inne wykorzystanie może w sposób szczególnie dotkliwy naruszać prawa i wolności jednostki, określone w art. 27 u.o.d.o. Przetwarzanie w określonym systemie komputerowym danych sensytywne podnosi znacząco wymogi bezpieczeństwa wymagane od systemu informatycznego.

W przypadku systemu centralnego uwierzytelniania bezpośrednio w nim nie będą przetwarzane dane sensytywne. Mogą natomiast one stanowić bramę wejścia do systemu komputerowego, w którym takie dane mogą być przetwarzane.

Ustawa zawiera delegację do wydania rozporządzenia przez ministra właściwego do spraw administracji w porozumieniu z ministrem właściwym do spraw informatyzacji, które określi podstawowe warunki techniczne i organizacyjne, jakim powinny odpowiadać urządzenia i systemy informatyczne służące do przetwarzania danych osobowych, uwzględniając zapewnienie ochrony przetwarzanych danych osobowych odpowiedniej do zagrożeń oraz kategorii danych objętych ochroną, a także wymagania w zakresie odnotowywania udostępniania danych osobowych i bezpieczeństwa przetwarzanych danych (art. 39a u.o.d.o.).

Delegacja została spełniona poprzez rozporządzenie Ministra Spraw Wewnętrznych i Administracji w sprawie dokumentacji przetwarzania danych osobowych oraz warunków technicznych i organizacyjnych, jakim powinny odpowiadać urządzenia i systemy informatyczne służące do przetwarzania danych osobowych z dnia 29 kwietnia 2004 r. [#f5]_


W rozporządzeniu - uwzględniając kategorie przetwarzanych danych oraz zagrożenia wprowadza się poziomy bezpieczeństwa przetwarzania danych osobowych w systemie informatycznym wprowadził trzy poziomy bezpieczeństwa - podstawowy, podwyższony i wysoki. Poziom wysoki stosuje się, gdy przynajmniej jedno urządzenie systemu informatycznego, służącego do przetwarzania danych osobowych, połączone jest z siecią publiczną. Zważywszy że aplikacja ma służyć także do uwierzytelniania także odbiorców Stowarzyszenia należy - podczas projektowania aplikacji - przyjąć konieczność spełnienia wymogów bezpieczeństwa na najwyższym poziomie bezpieczeństwie tj. poziomie wysokim.

Opis środków bezpieczeństwa stosowany na poziomach określa załącznik do rozporządzenia, który jest cytowany poniżej:

    A. Środki bezpieczeństwa na poziomie podstawowym

    I

    1. Obszar, o którym mowa w § 4 pkt 1 rozporządzenia, zabezpiecza się przed dostępem osób nieuprawnionych na czas nieobecności w nim osób upoważnionych do przetwarzania danych osobowych.
    2. Przebywanie osób nieuprawnionych w obszarze, o którym mowa w § 4 pkt 1 rozporządzenia, jest dopuszczalne za zgodą administratora danych lub w obecności osoby upoważnionej do przetwarzania danych osobowych.

    II

    1. W systemie informatycznym służącym do przetwarzania danych osobowych stosuje się mechanizmy kontroli dostępu do tych danych.
    2. Jeżeli dostęp do danych przetwarzanych w systemie informatycznym posiadają co najmniej dwie osoby, wówczas zapewnia się, aby:

    1) w systemie tym rejestrowany był dla każdego użytkownika odrębny identyfikator;
    2) dostęp do danych był możliwy wyłącznie po wprowadzeniu identyfikatora i dokonaniu uwierzytelnienia.

    III

    System informatyczny służący do przetwarzania danych osobowych zabezpiecza się, w szczególności przed:
    1) działaniem oprogramowania, którego celem jest uzyskanie nieuprawnionego dostępu do systemu informatycznego;
    2) utratą danych spowodowaną awarią zasilania lub zakłóceniami w sieci zasilającej.

    IV

    1. Identyfikator użytkownika, który utracił uprawnienia do przetwarzania danych, nie może być przydzielony innej osobie.
    2. W przypadku gdy do uwierzytelniania użytkowników używa się hasła, jego zmiana następuje nie rzadziej niż co 30 dni. Hasło składa się co najmniej z 6 znaków.
    3. Dane osobowe przetwarzane w systemie informatycznym zabezpiecza się przez wykonywanie kopii zapasowych zbiorów danych oraz programów służących do przetwarzania danych.
    4. Kopie zapasowe:

    a) przechowuje się w miejscach zabezpieczających je przed nieuprawnionym przejęciem, modyfikacją, uszkodzeniem lub zniszczeniem;
    b) usuwa się niezwłocznie po ustaniu ich użyteczności.

    V 

    Osoba użytkująca komputer przenośny zawierający dane osobowe zachowuje szczególną ostrożność podczas jego transportu, przechowywania i użytkowania poza obszarem, o którym mowa w § 4 pkt 1 rozporządzenia, w tym stosuje środki ochrony kryptograficznej wobec przetwarzanych danych osobowych.

    VI

    Urządzenia, dyski lub inne elektroniczne nośniki informacji, zawierające dane osobowe, przeznaczone do:
    1) likwidacji - pozbawia się wcześniej zapisu tych danych, a w przypadku gdy nie jest to możliwe, uszkadza się w sposób uniemożliwiający ich odczytanie;
    2) przekazania podmiotowi nieuprawnionemu do przetwarzania danych - pozbawia się wcześniej zapisu tych danych, w sposób uniemożliwiający ich odzyskanie;
    3) naprawy - pozbawia się wcześniej zapisu tych danych w sposób uniemożliwiający ich odzyskanie albo naprawia się je pod nadzorem osoby upoważnionej przez administratora danych.

    VII

    Administrator danych monitoruje wdrożone zabezpieczenia systemu informatycznego.

    B. Środki bezpieczeństwa na poziomie podwyższonym

    VIII

    W przypadku gdy do uwierzytelniania użytkowników używa się hasła, składa się ono co najmniej z 8 znaków, zawiera małe i wielkie litery oraz cyfry lub znaki specjalne.

    IX

    Urządzenia i nośniki zawierające dane osobowe, o których mowa w art. 27 ust. 1 ustawy z dnia 29 sierpnia 1997 r. o ochronie danych osobowych, przekazywane poza obszar, o którym mowa w § 4 pkt i rozporządzenia, zabezpiecza się w sposób zapewniający poufność i integralność tych danych.

    X

    Instrukcja zarządzania systemem informatycznym, o której mowa w § 5 rozporządzenia, rozszerza się o sposób stosowania środków, o których mowa w pkt IX załącznika.

    XI

    Administrator danych stosuje na poziomie podwyższonym środki bezpieczeństwa określone w części A załącznika, o ile zasady zawarte w części B nie stanowią inaczej.

    C. Środki bezpieczeństwa na poziomie wysokim

    XII

    1. System informatyczny służący do przetwarzania danych osobowych chroni się przed zagrożeniami pochodzącymi z sieci publicznej poprzez wdrożenie fizycznych lub logicznych zabezpieczeń chroniących przed nieuprawnionym dostępem.
    2. W przypadku zastosowania logicznych zabezpieczeń, o których mowa w ust. 1, obejmują one:

    a) kontrolę przepływu informacji pomiędzy systemem informatycznym administratora danych a siecią publiczną;
    b) kontrolę działań inicjowanych z sieci publicznej i systemu informatycznego administratora danych.

    XIII

    Administrator danych stosuje środki kryptograficznej ochrony wobec danych wykorzystywanych do uwierzytelnienia, które są przesyłane w sieci publicznej.

    XIV

    Administrator danych stosuje na poziomie wysokim środki bezpieczeństwa, określone w części A i B załącznika, o ile zasady zawarte w części C nie stanowią inaczej.

.. todo:: Uzupełnić numery strony w #f1 i #f2 na podstawie wydania papierowego.

Wskazać należy także na częściową uzasadnioną krytykę powyższych regulacji, których nieprawidłowe odczytanie może prowadzić do wręcz do ograniczenia bezpieczeństwa. W przywołanym zaączniku określono dla poziomu B i C, że jeśli do uwierzytelniania użytkowników używa się hasła, jego zmiana następuje nie rzadziej niż co 30 dni. W poszczególnych przypadkach określono wymogi co do złożoności haseł. 

Przepisy te bywają odczytywane jako wprowadzające bezwzględny wymóg cyklicznego zmienia hasła, jeżeli tylko formą uwierzytelniania jest hasło [#f6]_. Takie odczytanie tych przepisów okazuje się jednak, że mógłoby prowadzić do ograniczenia bezpieczeństwa systemów informatycznych (zob. :ref:`password_policy`). 

Wobec pojawiających się wątpliwości stanowisko w tym zakresie - w 2016 roku kilkukrotnie - przedstawiała Minister Cyfryzacji, która jest obecnie odpowiedzialna za ewentualną zmianę rozporządzenia. Należy w tym zakresie zwrócić szczególną uwagę na pismo Minister Cyfryzacji z dnia 12 maja 2016 roku [#f10]_:

    Wymóg cyklicznej zmiany hasła w praktyce zwiększa poziom zabezpieczenia i ochrony danych osobowych. Jeżeli stosowana jest zmiana hasła co 30 dni, to dostęp do konkretnego systemu czy zbioru danych osobowych jest możliwy jedynie przez ww. okres. W przypadku, gdy system informatyczny nie wymusza zmiany hasła w określonych odstępach czasu, wówczas uzyskanie hasła przez osoby nieuprawnione może oznaczać uzyskanie permanentnego dostępu do danego systemu. W odpowiedzi na sugestię zawartą w petycji, zgodnie z którą przepisy prawa powszechnie obowiązującego powinny przewidywać możliwości autoryzacji wieloskładnikowej zamiast wymogu częstej zmiany haseł albo że wymóg zmiany haseł powinien przynajmniej zostać ograniczony w przypadku wprowadzenia takiej formy autoryzacji pragnę uprzejmie wyjaśnić, że przepisy rozporządzenia w sprawie dokumentacji przetwarzania danych osobowych oraz warunków technicznych i organizacyjnych, jakim powinny odpowiadać urządzenia i systemy informatyczne służące do przetwarzania danych osobowych, wprowadzają obowiązek cyklicznej zmiany haseł i ustanawiają jedynie minimalny poziom zabezpieczenia systemów informatycznych. Wymogi określone w załączniku do ww. rozporządzenia odnoszące się do haseł (w pkt Iy.2 oraz w pkt VIII), poprzedzone są zastrzeżeniem: *w przypadku gdy do uwierzytelniania użytkowników używa się hasła....* Przyjęcie takiego rozwiązania nie wyklucza zatem innych sposoby uwierzytelniania, jeżeli zapewniają odpowiednie środki techniczne i organizacyjne niezbędne dla zapewnienia poufności, integralności i rozliczalności przetwarzanych danych oraz zostały opisane w Polityce bezpieczeństwa, o której mowa w 4 ust. 5 ww. rozporządzenia. W związku z powyższym, w celu ochrony systemów informatycznych możliwe jest stosowanie bardziej złożonych zabezpieczeń, w tym autoryzacji wieloskładnikowej. Zaznaczyć należy, że bardziej zaawansowane formy uwierzytelniania są w Polsce już obecnie powszechnie stosowane zarówno w sektorze prywatnym, jak i publicznym. Pragnę również podkreślić, że w 2018 roku wejdzie w życie rozporządzenie Parlamentu Europejskiego i Rady (UE) 2016/679 z dnia 27 kwietnia 2016 r. w sprawie ochrony osób fizycznych w zwiqzku z przetwarzaniem danych osobowych i w sprawie swobodnego przepływu takich danych oraz uchylenia dyrektywy 95/46/WE (ogólne rozporządzenie o ochronie danych).

Powyższe stanowisko przemawiają dodatkowo za zasadnością wdrożonych alternatywnych form uwierzytelniania, których szczegółowa analiza została przedstawioan (:ref:`2factor`).

.. rubric:: Footnotes

.. [#f1] Janusz Barta, Paweł Fajgielski, Ryszard Markiewicz,  Ochrona danych osobowych. Komentarz, wyd. V

.. [#f2] Janusz Barta, Paweł Fajgielski, Ryszard Markiewicz,  Ochrona danych osobowych. Komentarz, wyd. V

.. [#f3] Janusz Barta, Paweł Fajgielski, Ryszard Markiewicz,  Ochrona danych osobowych. Komentarz, wyd. V

.. [#f4] Dz.U. 1997 Nr 133, poz. 883 t.j. Dz.U. z 2016 r. poz. 922

.. [#f5] Dz.U. Nr 100, poz. 1024

.. [#f6] Adam Dobrawy, O potrzebie wzmocnienia ochrony danych osobowych, Blog Dobrawego, 30 marca 2016 roku, https://ochrona.jawne.info.pl/2016/03/30/o-potrzebie-zmian-ochronie-danych-osobowych/ [dostep 22 grudnia 2016 roku]

.. [#f10] pismo Minister Cyfryzacji znak BM-WSKN.053.5.2016 z dnia 12 maja 2016 roku stanowiące odpowiedź na petycje autora niniejszego opracownaia, http://mc.bip.gov.pl/skargi-wnioski-petycje/petycja-o-uwzglednienie-dwuskladnikowej-autoryzacji.html [dostęp 22 grudnia 2016 roku]

