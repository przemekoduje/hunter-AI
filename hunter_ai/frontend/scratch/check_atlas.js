const { MongoClient } = require('mongodb');

async function main() {
  const url = 'mongodb+srv://przemekrakotny_db_user:altiff1974@hunterai.xikwejz.mongodb.net/?appName=HunterAI';
  const client = new MongoClient(url);

  try {
    await client.connect();
    console.log('Connected to Atlas');
    
    const admin = client.db().admin();
    const dbs = await admin.listDatabases();
    console.log('Databases:', dbs.databases.map(db => db.name));

    for (const dbInfo of dbs.databases) {
      if (['admin', 'local', 'config'].includes(dbInfo.name)) continue;
      const db = client.db(dbInfo.name);
      const collections = await db.listCollections().toArray();
      console.log(`DB: ${dbInfo.name}, Collections: ${collections.map(c => c.name).join(', ')}`);
      
      for (const col of collections) {
        const count = await db.collection(col.name).countDocuments();
        console.log(`  - ${col.name}: ${count} docs`);
      }
    }
  } catch (e) {
    console.error('Error:', e.message);
  } finally {
    await client.close();
  }
}

main();
