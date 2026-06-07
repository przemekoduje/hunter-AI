const { MongoClient } = require('mongodb');

async function main() {
  const url = 'mongodb+srv://przemekrakotny_db_user:altiff1974@hunterai.xikwejz.mongodb.net/?appName=HunterAI';
  const client = new MongoClient(url);

  try {
    await client.connect();
    const admin = client.db().admin();
    const dbs = await admin.listDatabases();

    for (const dbInfo of dbs.databases) {
      if (['admin', 'local', 'config'].includes(dbInfo.name)) continue;
      const db = client.db(dbInfo.name);
      const collections = await db.listCollections().toArray();
      
      for (const col of collections) {
        const count = await db.collection(col.name).countDocuments();
        const sample = await db.collection(col.name).findOne({});
        console.log(`DB: ${dbInfo.name} | Collection: ${col.name} | Count: ${count}`);
        console.log(`Schema: ${Object.keys(sample || {}).join(', ')}`);
        console.log('---');
      }
    }
  } catch (e) {
    console.error(e);
  } finally {
    await client.close();
  }
}

main();
