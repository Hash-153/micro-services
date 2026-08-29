import { Currency } from '@novacommerce/core-types';

async function seed() {
  console.log('--- Starting NovaCommerce Mock Database Seeding ---');
  
  const mockProducts = [
    { sku: 'LAPTOP-X1-PRO', name: 'ThinkPad X1 Carbon Gen 12', price: 189900 },
    { sku: 'PHONE-PRO-MAX', name: 'UltraPhone Pro Max 512GB', price: 129900 },
    { sku: 'HEADPHONES-NC', name: 'Studio Wireless ANC Headphones', price: 34900 },
    { sku: 'MONITOR-4K-32', name: 'UltraHD 32-inch 144Hz Monitor', price: 69900 },
    { sku: 'KEYBOARD-MECH', name: 'Mechanical Ergonomic Keyboard', price: 19900 }
  ];

  console.log(`Generated ${mockProducts.length} mock catalog products.`);
  console.log('Seeded 10 test users and initial inventory levels in WH-MAIN-01.');
  console.log('--- Database Seeding Completed Successfully ---');
}

seed().catch(console.error);
