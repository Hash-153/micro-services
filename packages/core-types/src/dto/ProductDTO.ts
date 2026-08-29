import { z } from 'zod';
import { Currency } from '../enums/Currency.js';

export const CreateProductSchema = z.object({
  sku: z.string().min(3).max(64),
  name: z.string().min(1).max(255),
  slug: z.string().min(1).max(255),
  description: z.string().max(4000),
  categoryId: z.string().uuid(),
  basePrice: z.object({
    amount: z.number().int().nonnegative(),
    currency: z.nativeEnum(Currency)
  }),
  tags: z.array(z.string()).default([]),
  attributes: z.record(z.union([z.string(), z.number(), z.boolean()])).default({}),
  isActive: z.boolean().default(true)
});

export type CreateProductDTO = z.infer<typeof CreateProductSchema>;

export const ProductFilterQuerySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
  categoryId: z.string().uuid().optional(),
  search: z.string().optional(),
  minPrice: z.coerce.number().int().optional(),
  maxPrice: z.coerce.number().int().optional(),
  tags: z.string().optional(), // comma-separated
  sortBy: z.enum(['price_asc', 'price_desc', 'created_desc', 'name_asc']).default('created_desc')
});

export type ProductFilterQueryDTO = z.infer<typeof ProductFilterQuerySchema>;
