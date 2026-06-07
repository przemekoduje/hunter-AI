const { MongoClient } = require('mongodb');

async function main() {
  const url = 'mongodb+srv://przemekrakotny_db_user:altiff1974@hunterai.xikwejz.mongodb.net/leads?appName=HunterAI';
  const client = new MongoClient(url);

  try {
    await client.connect();
    const db = client.db('leads');
    const docs = await db.collection('leads').find({}).toArray();
    console.log('All documents:', JSON.stringify(docs, null, 2));
  } catch (e) {
    console.error(e);
  } finally {
    await client.close();
  }
}

main();
