import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { ShipmentEntity } from '@novacommerce/core-types';

export class InMemoryShipmentRepository extends InMemoryBaseRepository<ShipmentEntity> {}
