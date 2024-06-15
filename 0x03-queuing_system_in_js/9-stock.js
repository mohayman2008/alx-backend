import { promisify } from 'util';
import express from 'express';
import { createClient } from 'redis';

const PRODUCT_NOT_FOUND_JSON = '{ "status": "Product not found" }';
const listProducts = [
  {
    Id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  },
  {
    Id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  },
  {
    Id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  },
  {
    Id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

const redis = createClient()
  .on('error', (err) => console.log('Redis client not connected to the server:', err.message))
  .on('connect', () => console.log('Redis client connected to the server'));

const app = express();
const PORT = 1245;

app.listen(PORT, () => {
  console.log(`Express app started on port ${PORT}`);
});

app.get('/list_products', (req, res) => {
  res.send(genProductsListJSON(listProducts));
});

app.get('/list_products/:itemId', async (req, res) => {
  res.send(await genProductJSON(Number(req.params.itemId)));
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const product = getItemById(itemId);
  if (!product)
    res.send(PRODUCT_NOT_FOUND_JSON);

  const available = product.stock - await getCurrentReservedStockById(itemId);

  const obj = {};
  if (available > 0) {
    obj.status = 'Reservation confirmed';
    await reserveStockById(itemId);
  } else {
    obj.status = 'Not enough stock available';
  }
  obj.itemId = itemId;

  res.send(JSON.stringify(obj));
});

function getItemById(id) {
  for (const product of listProducts) {
    if (product.Id === id) return product;
  }
  return null;
}

function genProductsListJSON(listOfProducts) {
  const list = [];
  for (const product of listOfProducts) {
    const obj = {
      itemId: product.Id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
    };
    list.push(obj);
  }
  return JSON.stringify(list);
}

async function genProductJSON(itemId) {
  const product = getItemById(itemId);
  if (!product)
    return PRODUCT_NOT_FOUND_JSON;

  const obj = {
    itemId: product.Id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: product.stock - await getCurrentReservedStockById(itemId),
  };

  return JSON.stringify(obj);
}

function reserveStockById(itemId, stock = 1) {
  redis.incrby(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const reservedStock = await promisify(redis.get).bind(redis)(`item.${itemId}`);
  return reservedStock;
}
