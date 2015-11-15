# Manual #

Una vez presentada UMO en una entrada anterior, vamos a ver con un poco más de detalle cómo desplegarla para empezar a jugar con ella. Se ha probado la herramienta en un sistema con GNU/Linux Debian Squeeze y se ha utilizado Python 2.6.6.

Lo primero es descargar la herramienta:

```
$ export workdir=/tmp/umo
$ mkdir -p $workdir
$ cd $workdir
$ wget http://umo.googlecode.com/files/umobeta0.1b.tar.gz
```

Una vez descargada la descomprimimos:

```
$ tar -xvzf umobeta0.1b.tar.gz
```

Una vez descomprimida la herramienta, dispondremos de la siguiente estructura de directorios:

```
x trunk/
x trunk/crawler.py
x trunk/bingScan.py
x trunk/googleScan.py
x trunk/umoconfig.py
x trunk/malwareScan.py
x trunk/xgoogle/
x trunk/xgoogle/BeautifulSoup.pyc
x trunk/xgoogle/googlesets.py
x trunk/xgoogle/BeautifulSoup.py
x trunk/xgoogle/search.pyc
x trunk/xgoogle/__init__.pyc
x trunk/xgoogle/browser.py
x trunk/xgoogle/translate.py
x trunk/xgoogle/__init__.py
x trunk/xgoogle/search.py
x trunk/xgoogle/browser.pyc
x trunk/xgoogle/sponsoredlinks.py
x trunk/umo.py
x trunk/safebrowsing/
x trunk/safebrowsing/base.py
x trunk/safebrowsing/conf.py
x trunk/safebrowsing/query_lookup.py
x trunk/safebrowsing/__init__.py
x trunk/safebrowsing/backend.py
x trunk/safebrowsing/prepare_db.py
```

Ahora es necesario instalar el API pybing que nos permitirá lanzar consultas a Bing, para ello seguiremos las instrucciones de la propia página del api. Si os bajáis el “.egg” de la sección downloads os dará un error que está corregido en [r33](https://code.google.com/p/umo/source/detail?r=33).

Una vez instalado es aconsejable realizar una prueba a través de la consola de python de que el API funciona correctamente:

```
# python
Python 2.6.6 (r266:84292, Dec 26 2010, 22:31:48)
[GCC 4.4.5] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from pybing.query import WebQuery
>>> query = WebQuery('Mi API key', query='python bing')
>>> results = query.execute()
>>> for result in results[:3]:
... print repr(result.title)
...
u'Python Wrapper on Bing API \u2014 The Usware Blog - Django Web ...'
u"Bing.com (Nuevo Buscador de Microsoft) - Web-engineer's.es"
u'YouTube - \u202aMonty Python - The Machine That Goes Bing ...'
>>>
```

Para conseguir nuestra API Key de Bing, tendremos que ir a la página Web de Bing para obtenerla. Ahora es el momento de configurar la librería safebrowsing de python, apoyándonos como siempre en la web oficial. Primero deberemos crear la base datos. Para ello utilizaremos Mysql (acordaros de disponer de python-mysqldb para poder interactuar con la base de datos) y haremos:

```
Creamos la base de datos: safebrowsing
mysql> CREATE DATABASE safebrowsing;
Creamos el esquema de la base de datos como indica en la web oficial.

Un usuario para acceso a la base de datos de safebrowsing: umosb

mysql> CREATE USER 'umosb'@'localhost' IDENTIFIED BY 'mi pass'
Damos permisos a ese usuario sobre la base de datos.

mysql> GRANT ALL PRIVILEGES ON safebrowsing.* TO 'umosb'@'localhost';
mysql> flush privileges;
```

Ahora estos datos los pondremos en fichero “trunk/safebrowsing/conf.py”:

```
# Inspired from Django's settings.py
DATABASE_ENGINE = 'mysql' # Possible values being 'postgresql', 'mysql', 'sqlite3' or 'memcached'
DATABASE_NAME = 'safebrowsing' # Or path to database file if using sqlite3.
DATABASE_USER = 'umosb' # Not used with sqlite3.
DATABASE_PASSWORD = 'mipass' # Not used with sqlite3.
DATABASE_HOST = 'localhost' # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '' # Set to empty string for default. Not used with sqlite3.
API_KEY = 'Mi API key' # API Key provided by Google.
```

Del único dato que no hemos hablado es del API key de safebrowsing de Google. Para conseguirlo deberemos disponer de una cuenta de Google y acceder a la web donde se nos generará la key estando autenticados con nuestra cuenta de Google.

Por último configuraremos en “trunk/umoconfig.py” los diferentes valores. Sobretodo debemos fijar en ese fichero el Bing API key.

```
skippages = 0
pages = 10
results = 100
googlesleep = 5
user_agent = 'code.google.com/umo'
bingresults = 400
bingkey = 'API Key Bing'
depth = '1'
malware = 'umomalware.log'
safebrowsing = 'True'
updatesafebrowsing = 'False'
maxtries = 5
```

Llegados a este punto si todo ha ido bien tendremos umo beta 0.1b lista para jugar. En una próxima entrada pondré ejemplos de uso, para que sea más sencillo conocerla.

Nota: Con las pruebas que estoy realizando existen algunas búsquedas, sobretodo con Google, que no están del todo controladas por el script; en estos momento estoy “debugueando” y corrigiendo.