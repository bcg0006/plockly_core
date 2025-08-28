import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { testUtils } from './test-utils';

describe('Test Utils', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('waitFor', () => {
    it('resolves when condition is met', async () => {
      let condition = false;
      setTimeout(() => { condition = true; }, 100);

      await testUtils.waitFor(() => condition, 1000);
      expect(condition).toBe(true);
    });

    it('rejects when timeout is reached', async () => {
      const condition = () => false;

      await expect(testUtils.waitFor(condition, 100)).rejects.toThrow('Condition not met within timeout');
    });
  });

  describe('mockLocalStorage', () => {
    it('creates a mock localStorage with working methods', () => {
      const mockStorage = testUtils.mockLocalStorage();

      // Test setItem and getItem
      mockStorage.setItem('test', 'value');
      expect(mockStorage.getItem('test')).toBe('value');

      // Test removeItem
      mockStorage.removeItem('test');
      expect(mockStorage.getItem('test')).toBeNull();

      // Test clear
      mockStorage.setItem('key1', 'value1');
      mockStorage.setItem('key2', 'value2');
      mockStorage.clear();
      expect(mockStorage.length).toBe(0);
    });
  });

  describe('mockSessionStorage', () => {
    it('creates a mock sessionStorage with working methods', () => {
      const mockStorage = testUtils.mockSessionStorage();

      // Test setItem and getItem
      mockStorage.setItem('test', 'value');
      expect(mockStorage.getItem('test')).toBe('value');

      // Test removeItem
      mockStorage.removeItem('test');
      expect(mockStorage.getItem('test')).toBeNull();

      // Test clear
      mockStorage.setItem('key1', 'value1');
      mockStorage.setItem('key2', 'value2');
      mockStorage.clear();
      expect(mockStorage.length).toBe(0);
    });
  });

  describe('createTestUser', () => {
    it('creates a test user with default values', () => {
      const user = testUtils.createTestUser();

      expect(user).toEqual({
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
        is_active: true,
        date_joined: '2024-01-01T00:00:00Z',
      });
    });

    it('allows overriding default values', () => {
      const user = testUtils.createTestUser({
        username: 'customuser',
        email: 'custom@example.com',
      });

      expect(user.username).toBe('customuser');
      expect(user.email).toBe('custom@example.com');
      expect(user.id).toBe(1); // Default value preserved
    });
  });

  describe('createTestItem', () => {
    it('creates a test item with default values', () => {
      const item = testUtils.createTestItem();

      expect(item).toEqual({
        id: 1,
        title: 'Test Item',
        description: 'This is a test item',
        owner: 1,
        is_active: true,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      });
    });

    it('allows overriding default values', () => {
      const item = testUtils.createTestItem({
        title: 'Custom Item',
        description: 'Custom description',
      });

      expect(item.title).toBe('Custom Item');
      expect(item.description).toBe('Custom description');
      expect(item.id).toBe(1); // Default value preserved
    });
  });
});
