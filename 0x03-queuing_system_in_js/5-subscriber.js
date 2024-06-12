import { createClient } from 'redis';

const CHANNEL_NAME = 'holberton school channel';
const client = createClient()
  .on('error', (err) => console.log('Redis client not connected to the server:', err.message))
  .on('connect', () => console.log('Redis client connected to the server'));

client.subscribe(CHANNEL_NAME);

client.on('message', (channel, message) => {
  if (channel !== CHANNEL_NAME) return;

  console.log(message);
  if (message === 'KILL_SERVER') {
    client.unsubscribe();
    client.quit();
  }
});
