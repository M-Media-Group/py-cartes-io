# Official Cartes.io Python package

## Usage

Install Cartes.io Python package:

```python
pip install py-cartes-io
```

First, import the package:

```python
import py_cartes_io as cartes
```

### Create a map

```python
newMap = cartes.Maps().create()
print(newMap['uuid'])
print(newMap['token'])
```

### Get a list of maps

```python
cartes.Maps().get()
```

You can use the `add_param` method to add parameters to the request, especially useful for pagination:

```python
cartes.Maps().add_param('page', 2).get()

# There is also a shorthand for this
cartes.Maps().page(2).get()
```

### Get a specific map

```python
cartes.Maps('048eebe4-8dac-46e2-a947-50b6b8062fec').get()
```
### Get a maps markers

```python
cartes.Maps('048eebe4-8dac-46e2-a947-50b6b8062fec').markers().get()
```

You can also add parameters to the request with `add_param` method:

```python
map = cartes \
    .Maps('651107a9-1d22-46a8-8254-111f7ac74a2b') \
    .markers() \
    .add_param('show_expired', True) \
    .get()

print(map)
```

### Create markers

```python
params = {
    'lat': row['lat'],
    'lng': row['lng'],
    'description': row['description'],
    'category_name': row['category_name'],
    'link': row['link']
}

cartes.Maps('048eebe4-8dac-46e2-a947-50b6b8062fec').markers().create(params)

# you can also pass a map_token (or api_key) if your map settings require it
cartes.Maps('048eebe4-8dac-46e2-a947-50b6b8062fec', map_token="xxx").markers().create(params)
```

### Get related maps for a specific map

```python
cartes.Maps('048eebe4-8dac-46e2-a947-50b6b8062fec').related().get()
```
