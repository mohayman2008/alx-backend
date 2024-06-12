import { createClient } from 'redis';

const client = createClient()
  .on('error', err => console.log('Redis client not connected to the server:', err.message))
  // .on('ready', () => console.log('Redis client connected to the server'))
  .on('connect', () => console.log('Redis client connected to the server'));
