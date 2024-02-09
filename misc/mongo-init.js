use admin;

db.createUser(
  {
    user: 'admin',
    pwd: 'root',
    roles: [ { role: 'root', db: 'admin' } ]
  }
);

use db;

db.createCollection('users');

db.users.insertMany([
  { login: 'admin', password: 'root' },
  { login: 'user', password: '123' }
]);