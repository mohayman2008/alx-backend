import kue from 'kue';

const queue = kue.createQueue();

kue.Job.range(0, 0xFFFFFFFF, 'asc', (err, jobs) => {
  for (const job of jobs) {
    console.log(job.type, job.id);
    job.remove();
  }
});
