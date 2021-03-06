### Installation
        
    $ git clone https://github.com/XENKing/lightdataparser
    
    $ cd lightdataparser
    
    $ python setup.py sdist (or python3 setup.py sdist)
    
    $ cd dist
    
    $ (sudo) pip install pkg_available_in_directory (or pip3 install pkg_available_in_directory) 
    
      # where 'pkg_available_in_directory' is the exact name of the package
      
      # created in the 'dist' folder
      
    # OR
    
    $ (sudo) pip install git+https://github.com/XENKing/lightdataparser.git
        
        
**Note:** use 'sudo' depending on whether you want to install package system-wide or not
        
**Note:** use pip or pip3 depending on what is available on your system

### Uninstall
        
    $ (sudo) pip uninstall lightdataparser (OR pip3 uninstall lightdataparser)

### Usage
    $ lightdataparser [args] <files/directory/path>
 
**For extra help use:** 

    $ lightdataparser -h

<details> 
 <summary>Task summary</summary>

### Description
Представляет из себя проcтой ETL с разными форматами файлов.

Задание состоит из двух блоков:

1. [Basic](#basic) - основная задача
2. [Advanced](#advanced) - дополнение к основной задаче 

Использовать можно только средства стандартной библиотеки Python.
Во всех случаях программа должна запускаться из терминала.

Для проверки работы программы предоставлются входные данные и результаты в виде 6 файлов:
* входные данные:
  * csv_data_1.csv
  * csv_data_2.csv
  * json_data.json
  * xml_data.xml
* результаты **Basic**:
  * basic_results.tsv
* результаты **Advanced**:
  * advanced_results.tsv

### Задача
Есть четыре файла: два `.csv`, один `.json` и один .`xml` файл.   


Первый `.csv` имеет следующую структуру:

|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |
|... |... |... |... |... |... |... |... |

Второй `.csv` имеет следующую структуру:

|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |... |Mz  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |... |i   |
|... |... |... |... |... |... |... |... |... |... |

**Внимание! Порядок колонок может несовпадать. В обоих файлах есть заголовки.**


`.json` файл имеет следуующую структуру:
```python
{
  "fields": [
    {
      "D1": "s",
      "D2": "s",
      ...
      "Dn": "s",
      "M1": i,
      ...
      "Mp": i,
    },
    ...
  ]
}
```

`.xml` файл сожержит в себе следующую структуру:
```xml
<objects>
  <object name="D1">
    <value>s</value>
  </object>
  <object name="D2">
    <value>i</value>
  </object>
  ...
  <object name="Dn">
    <value>s</value>
  </object>
  <object name="M1">
    <value>i</value>
  </object>
  <object name="M2">
    <value>i</value>
  </object>
  ...
  <object name="Mn">
    <value>i</value>
  </object>
</objects>
```

Где *z* > *n*, *p* >= *n*, *s* строка и *i* целое число.

#### Basic

Файлы нужно будет трансформировать в один `.tsv` файл со следующей структурой:


|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |
|... |... |... |... |... |... |... |... |

Он должен быть отсортирован по колонке **D1** и содержать даннные из всех четырёх файлов.


#### Advanced

Файлы нужно будет трансформировать в один `.tsv` файл со следующей структурой:

|D1   |D2   |... |Dn   |MS1  |MS2  |...  |MSn  |
|:---:|:--:|:---:|:---:|:---:|:---:|:---:|:---:|
|s    |s   |...  |s    |i    |i    |...  |i    |
|...  |... |...  |...  |...  |...  |...  |...  |

В колонках **MS1**...**MSn** должны находиться суммы знаений соответствующих **M1**...**Mn** из 4 файлов сгруппированные 
по уникальнным значениям комбинаций строк из **D1**...**Dn**.

##### Пример
**Содeржимое .tsv файла с данными из 4 файлов:**

|D1  |D2  |M1  |M2  |M3  |
|:--:|:--:|:--:|:--:|:--:|
|a   |a   |0   |0   |0   |
|a   |a   |1   |0   |1   |
|a   |a   |0   |2   |1   |
|a   |b   |1   |1   |1   |
|c   |c   |7   |7   |7   |

**Ожидаемый результат:**

|D1  |D2  |M1  |M2  |M3  |
|:--:|:--:|:--:|:--:|:--:|
|a   |a   |1   |2   |2   |
|a   |b   |1   |1   |1   |
|c   |c   |7   |7   |7   |

</details> 
