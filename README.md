Do uruchomienia programów words.py oraz mkdumpfile.sh konieczne jest
stworzenie zmiennej środowiskowej FASTTEXT_PATH, przechowującej
ściężkę do pliku wykonywalnego fasttexta.

Do uruchomienia programu words.py wymagane jest, aby plik build.py
znajdował się w tym samym folderze, co uruchamiany program.

Program words.py, oprócz oczekiwanego wyniku, może generować również
pliki, które są mu potrzebne do wyznaczenia wyniku końcowego. Pliki te
to model fasttext oraz pliki tekstowe przechowujące ciągi uczący oraz
testujący, które posłużyły do stworzenia tego modelu. Rozmiar tych
plików zależy od ilości przetwarzanych danych i może być liczony w
dzisiątkach MB. Z tego powodu są one domyślnie usuwane, gdy tylko nie
są już potrzebne. Za pomocą opcji wywołania programu można zachować te
pliki i podać je jako argumenty wywołania programu przy jego następnym
wywołaniu, co przyspieszy obliczenia.

words.py - program wypisuje na wyjściu słowa, które są najbardziej
	   charakterystyczne dla każdej etykiety, którą przechowuje
	   model fasttext. Ilość wypisywanych słów, miejsce zapisu
	   wyjścia programu, oraz inne parametry programu są możliwe
	   do ustawienia za pomocą opcji. Opis opcji i argumentów
	   wywołania programu można wyświetlić za pomocą polecenia:

	  	 python3 words.py -h

	   Wyjście programu jest generowane w formacie csv. Za pomocą
	   opcji -q, -y można wstrzymać wszystkie komunikaty programu
	   i przkierować jego wyjście do pliku:

  python3 words.py /sciezka/do/folderu/z/probkami/ -qy > plik_wyjsciowy.csv

	   Albo użyć opcji -o:

  python3 words.py /sciezka/do/folderu/z/probkami/ -o /sciezka/pliku/wyjsciowego
   
build.py - program do konstrukcji plików z ciągami uczącym i
	   testującym.  Lista dostępnych opcji oraz argumenty
	   wywołania programu są wyświetlane po wywołaniu:

	   	 python3 build.py -h

	   Program tworzy 2 pliki: train.txt oraz valid.txt, które
	   przechowują odpowiednio ciąg uczący oraz testujący w
	   postaci:

	   	__label__NazwaEtykiety , tekst_do_nauki

	   Argumentem programu jest ścieżka do folderu z plikami
	   tekstowymi (próbkami), na podstawie których zostaną
	   skonstruowane pliki wyjściowe programu.

	   Pliki są przystosowane do uczenia i testowania modelu
	   fasttext.

mkdumpfile.sh - program tworzący plik ze zrzutem informacji o modelu
	      	fasttexta (dump file), który można podać jako argument
	      	programu words.py. Dump file zawiera pary (etykieta
	      	wektor_etykiety), oddzielone znakiem nowej
	      	linii. Wywołanie:

  ./mkdumpfile.sh /sciezka/modelu/binarnego [opcjonalna/sciezka/pliku/wyjsciowego]

  		W przypadku braku podania scieżki do pliku wyjściowego,
		wyjście zostanie wypisane na stdout.