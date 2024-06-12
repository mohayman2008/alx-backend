import { createClient } from 'redis';

const client = createClient() // eslint-disable-line no-unused-vars
  .on('error', (err) => console.log('Redis client not connected to the server:', err.message))
  .on('connect', () => console.log('Redis client connected to the server'));
