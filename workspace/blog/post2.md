# JSON to CSV API: ETL Made Effortless

If you build data pipelines, you know the drill:
pull JSON from an API, transform it, load into a spreadsheet or DB.
The transform step is always the same boilerplate.

## Skip the Boilerplate

One POST request is all it takes:

```python
import requests, json

data = [{"product":"Widget","sales":120},{"product":"Gadget","sales":340}]
resp = requests.post(
    "https://boogeyman-unknowing-amenity.ngrok-free.dev/convert",
    json=data
)
print(resp.text)
# product,sales
# Widget,120
# Gadget,340
```

## JavaScript Example

```js
const resp = await fetch(
  'https://boogeyman-unknowing-amenity.ngrok-free.dev/convert',
  {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify([{name:'Alice',age:30}])
  }
);
console.log(await resp.text());
```

## Response Headers Tell You Everything

- X-Charge-USD: 0.01
- X-Rows-Converted: 2
- X-Request-Count: 42

## Pricing: $0.01 flat

No tiers, no subscriptions, no API keys.
Pay as you go, frictionless.

Endpoint: https://boogeyman-unknowing-amenity.ngrok-free.dev/convert
