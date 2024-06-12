import { createClient, print as redisPrint } from 'redis';

const client = createClient()
  .on('error', (err) => console.log('Redis client not connected to the server:', err.message))
  .on('connect', () => console.log('Redis client connected to the server'));

const H_KEY = 'HolbertonSchools';
const H_ITEMS = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

for (const [key, val] of Object.entries(H_ITEMS)) {
  client.hset(H_KEY, key, val, redisPrint);
}

client.hgetall(H_KEY, (err, obj) => { console.log(obj); });
