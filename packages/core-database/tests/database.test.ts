import { InMemoryBaseRepository } from '../src/index.js';

interface TestUser {
  id: string;
  name: string;
  email: string;
}

class TestUserRepository extends InMemoryBaseRepository<TestUser> {}

describe('Core Database Suite', () => {
  let repo: TestUserRepository;

  beforeEach(() => {
    repo = new TestUserRepository();
  });

  it('should create, find, update and delete entities', async () => {
    const user = await repo.create({ id: 'u1', name: 'Alice', email: 'alice@example.com' });
    expect(user.id).toBe('u1');

    const found = await repo.findById('u1');
    expect(found?.name).toBe('Alice');

    const updated = await repo.update('u1', { name: 'Alice B.' });
    expect(updated?.name).toBe('Alice B.');

    const count = await repo.count();
    expect(count).toBe(1);

    const deleted = await repo.delete('u1');
    expect(deleted).toBe(true);

    const afterDelete = await repo.findById('u1');
    expect(afterDelete).toBeNull();
  });
});
