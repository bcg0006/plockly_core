import { testUtils } from './test-utils';

describe('testUtils', () => {
  describe('waitFor', () => {
    it('should resolve when condition is met', async () => {
      let condition = false;
      setTimeout(() => {
        condition = true;
      }, 10);

      await expect(testUtils.waitFor(() => condition, 100)).resolves.toBeUndefined();
    });

    it('should reject when timeout is reached', async () => {
      const neverTrue = () => false;
      await expect(testUtils.waitFor(neverTrue, 50)).rejects.toThrow('Condition not met within timeout');
    });
  });

  describe('mockApiResponse', () => {
    it('should mock fetch for specific URL', async () => {
      const mockResponse = { data: 'test' };
      testUtils.mockApiResponse('/api/test', mockResponse);

      const response = await fetch('/api/test');
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data).toEqual(mockResponse);
    });

    it('should return 404 for unmocked URLs', async () => {
      testUtils.mockApiResponse('/api/test', { data: 'test' });

      const response = await fetch('/api/other');
      expect(response.ok).toBe(false);
      expect(response.status).toBe(404);
    });
  });

  describe('mockLocalStorage', () => {
    it('should provide localStorage mock interface', () => {
      const mockStorage = testUtils.mockLocalStorage();

      expect(mockStorage.getItem).toBeDefined();
      expect(mockStorage.setItem).toBeDefined();
      expect(mockStorage.removeItem).toBeDefined();
      expect(mockStorage.clear).toBeDefined();
      expect(mockStorage.length).toBe(0);
      expect(mockStorage.key).toBeDefined();
    });

    it('should store and retrieve items', () => {
      const mockStorage = testUtils.mockLocalStorage();

      mockStorage.setItem('test', 'value');
      expect(mockStorage.getItem('test')).toBe('value');
      expect(mockStorage.length).toBe(1);
    });

    it('should remove items', () => {
      const mockStorage = testUtils.mockLocalStorage();

      mockStorage.setItem('test', 'value');
      mockStorage.removeItem('test');
      expect(mockStorage.getItem('test')).toBe(null);
      expect(mockStorage.length).toBe(0);
    });

    it('should clear all items', () => {
      const mockStorage = testUtils.mockLocalStorage();

      mockStorage.setItem('test1', 'value1');
      mockStorage.setItem('test2', 'value2');
      mockStorage.clear();
      expect(mockStorage.length).toBe(0);
      expect(mockStorage.getItem('test1')).toBe(null);
      expect(mockStorage.getItem('test2')).toBe(null);
    });

    it('should get key by index', () => {
      const mockStorage = testUtils.mockLocalStorage();

      mockStorage.setItem('test', 'value');
      expect(mockStorage.key(0)).toBe('test');
      expect(mockStorage.key(1)).toBe(null);
    });
  });

  describe('mockSessionStorage', () => {
    it('should provide sessionStorage mock interface', () => {
      const mockStorage = testUtils.mockSessionStorage();

      expect(mockStorage.getItem).toBeDefined();
      expect(mockStorage.setItem).toBeDefined();
      expect(mockStorage.removeItem).toBeDefined();
      expect(mockStorage.clear).toBeDefined();
      expect(mockStorage.length).toBe(0);
      expect(mockStorage.key).toBeDefined();
    });

    it('should store and retrieve items', () => {
      const mockStorage = testUtils.mockSessionStorage();

      mockStorage.setItem('test', 'value');
      expect(mockStorage.getItem('test')).toBe('value');
      expect(mockStorage.length).toBe(1);
    });

    it('should remove items', () => {
      const mockStorage = testUtils.mockSessionStorage();

      mockStorage.setItem('test', 'value');
      mockStorage.removeItem('test');
      expect(mockStorage.getItem('test')).toBe(null);
      expect(mockStorage.length).toBe(0);
    });

    it('should clear all items', () => {
      const mockStorage = testUtils.mockSessionStorage();

      mockStorage.setItem('test1', 'value1');
      mockStorage.setItem('test2', 'value2');
      mockStorage.clear();
      expect(mockStorage.length).toBe(0);
      expect(mockStorage.getItem('test1')).toBe(null);
      expect(mockStorage.getItem('test2')).toBe(null);
    });

    it('should get key by index', () => {
      const mockStorage = testUtils.mockSessionStorage();

      mockStorage.setItem('test', 'value');
      expect(mockStorage.key(0)).toBe('test');
      expect(mockStorage.key(1)).toBe(null);
    });
  });

  describe('createTestUser', () => {
    it('should create test user with default values', () => {
      const user = testUtils.createTestUser();

      expect(user.id).toBe(1);
      expect(user.username).toBe('testuser');
      expect(user.email).toBe('test@example.com');
      expect(user.is_active).toBe(true);
      expect(user.date_joined).toBe('2024-01-01T00:00:00Z');
    });

    it('should create test user with overrides', () => {
      const user = testUtils.createTestUser({
        username: 'customuser',
        email: 'custom@example.com'
      });

      expect(user.username).toBe('customuser');
      expect(user.email).toBe('custom@example.com');
      expect(user.id).toBe(1); // Default value
    });
  });

  describe('createTestItem', () => {
    it('should create test item with default values', () => {
      const item = testUtils.createTestItem();

      expect(item.id).toBe(1);
      expect(item.title).toBe('Test Item');
      expect(item.description).toBe('This is a test item');
      expect(item.owner).toBe(1);
      expect(item.is_active).toBe(true);
      expect(item.created_at).toBe('2024-01-01T00:00:00Z');
      expect(item.updated_at).toBe('2024-01-01T00:00:00Z');
    });

    it('should create test item with overrides', () => {
      const item = testUtils.createTestItem({
        title: 'Custom Item',
        description: 'Custom description'
      });

      expect(item.title).toBe('Custom Item');
      expect(item.description).toBe('Custom description');
      expect(item.id).toBe(1); // Default value
    });
  });
});
