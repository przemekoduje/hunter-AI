import prisma from '../lib/prisma';

async function test() {
  try {
    console.log('Testing DB connection...');
    const count = await prisma.lead.count();
    console.log('Total leads:', count);

    const year = '2024';
    const where: any = {
      OR: [
        { data_wydania_decyzji: { contains: year } },
        { data_wydania_decyzji: null },
        // { data_wydania_decyzji: { exists: false } } // Suspected cause
      ]
    };

    console.log('Testing query with exists: false (simulated error)...');
    try {
      const leads = await prisma.lead.findMany({
        where: {
          OR: [
            ...where.OR,
            { data_wydania_decyzji: { exists: false } as any }
          ]
        },
        take: 1
      });
      console.log('Query with exists: false succeeded (unexpected)');
    } catch (e: any) {
      console.error('Query with exists: false failed as expected:', e.message);
    }

    console.log('Testing query with isSet: false...');
    const leadsFix = await prisma.lead.findMany({
      where: {
        OR: [
          ...where.OR,
          { data_wydania_decyzji: { isSet: false } }
        ]
      },
      take: 1
    });
    console.log('Query with isSet: false succeeded');

  } catch (err) {
    console.error('Fatal error:', err);
  } finally {
    await prisma.$disconnect();
  }
}

test();
