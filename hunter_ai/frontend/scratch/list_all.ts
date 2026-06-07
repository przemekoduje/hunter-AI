import { MongoClient } from 'mongodb';

async function main() {
  const url = 'mongodb+srv://przemekrakotny_db_user:altiff1974@hunterai.xikwejz.mongodb.net/?appName=HunterAI';
  const client = new MongoClient(url);

  try {
    await client.connect();
    console.log('Connected to Atlas');
    
    const admin = client.db().admin();
    const dbs = await admin.listDatabases();
    console.log('Databases:', dbs.databases.map(db => db.name));

    const leadsDb = client.db('leads');
    const leadsCollection = leadsDb.collection('leads');
    
    const recordWithDate = await leadsCollection.findOne({ data_wydania_decyzji: { $exists: true, $ne: null } });
    
    if (recordWithDate) {
      console.log('\n=== Rekord z datą znaleziony! ===');
      console.log(JSON.stringify(recordWithDate, null, 2));
    } else {
      console.log('\n!!! UWAGA: W bazie NIE MA rekordów z wypełnioną datą !!!');
    }
    
    const total = await leadsCollection.countDocuments();
    console.log(`Łączna liczba rekordów: ${total}`);
  } catch (e) {
    console.error(e);
  } finally {
    await client.close();
  }
}

main();
