import { Money } from '../enums/Currency.js';

export interface ProductEntity {
  id: string;
  sku: string;
  name: string;
  slug: string;
  description: string;
  categoryId: string;
  basePrice: Money;
  isActive: boolean;
  tags: string[];
  attributes: Record<string, string | number | boolean>;
  images: ProductImage[];
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date;
}

export interface ProductImage {
  id: string;
  url: string;
  altText?: string;
  sortOrder: number;
  isPrimary: boolean;
}

export interface ProductVariantEntity {
  id: string;
  productId: string;
  sku: string;
  name: string;
  priceModifier: number; // in cents
  weightGrams: number;
  dimensionsMm: {
    length: number;
    width: number;
    height: number;
  };
  options: Record<string, string>; // e.g. { "size": "XL", "color": "Navy" }
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface CategoryEntity {
  id: string;
  name: string;
  slug: string;
  description?: string;
  parentId?: string;
  displayOrder: number;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}
