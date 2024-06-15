import { createQueue } from 'kue';

/* eslint-disable no-unused-vars */
const Q_NAME = 'push_notification_code';

const queue = createQueue();
const jobData = {
  phoneNumber: '123-456-7890',
  message: 'Welcome',
};
const job = queue.create(Q_NAME, jobData)
  .save((err) => {
    if (err) {
      console.log(err);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  })
  .on('complete', (result) => {
    console.log('Notification job completed');
  })
  .on('failed', (errorMessage) => {
    console.log('Notification job failed');
  });
