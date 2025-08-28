import React from 'react';
import type { ReactElement } from 'react';
import { render } from '@testing-library/react';
import type { RenderOptions } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { configureStore } from '@reduxjs/toolkit';

// Import your store configuration when available
// import { store } from '../store';

// Create a mock store for testing
const createTestStore = () => {
  return configureStore({
    reducer: {
      // Add your reducers here when available
      // auth: authReducer,
      // items: itemsReducer,
    },
    preloadedState: {
      // Add initial state for testing
    },
  });
};

// Create a test theme
const testTheme = createTheme({
  // Customize theme for testing if needed
});

// Custom render function that includes providers
const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  const store = createTestStore();

  return (
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider theme={testTheme}>
          {children}
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  );
};

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllTheProviders, ...options });

// Re-export everything
export * from '@testing-library/react';

// Override render method
export { customRender as render };

// Export test utilities
export const testUtils = {
  // Wait for a condition to be true
  waitFor: (condition: () => boolean, timeout = 1000) => {
    return new Promise<void>((resolve, reject) => {
      const startTime = Date.now();

      const checkCondition = () => {
        if (condition()) {
          resolve();
          return;
        }

        if (Date.now() - startTime > timeout) {
          reject(new Error('Condition not met within timeout'));
          return;
        }

        setTimeout(checkCondition, 50);
      };

      checkCondition();
    });
  },

  // Mock API responses
  mockApiResponse: (url: string, response: any) => {
    global.fetch = jest.fn().mockImplementation((requestUrl) => {
      if (requestUrl === url) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(response),
        });
      }
      return Promise.resolve({
        ok: false,
        status: 404,
        statusText: 'Not Found',
      });
    });
  },

  // Mock localStorage
  mockLocalStorage: () => {
    const store: Record<string, string> = {};

    return {
      getItem: jest.fn((key: string) => store[key] || null),
      setItem: jest.fn((key: string, value: string) => {
        store[key] = value;
      }),
      removeItem: jest.fn((key: string) => {
        delete store[key];
      }),
      clear: jest.fn(() => {
        Object.keys(store).forEach(key => delete store[key]);
      }),
      length: Object.keys(store).length,
      key: jest.fn((index: number) => Object.keys(store)[index] || null),
    };
  },

  // Mock sessionStorage
  mockSessionStorage: () => {
    const store: Record<string, string> = {};

    return {
      getItem: jest.fn((key: string) => store[key] || null),
      setItem: jest.fn((key: string, value: string) => {
        store[key] = value;
      }),
      removeItem: jest.fn((key: string) => {
        delete store[key];
      }),
      clear: jest.fn(() => {
        Object.keys(store).forEach(key => delete store[key]);
      }),
      length: Object.keys(store).length,
      key: jest.fn((index: number) => Object.keys(store)[index] || null),
    };
  },

  // Create test user data
  createTestUser: (overrides = {}) => ({
    id: 1,
    username: 'testuser',
    email: 'test@example.com',
    is_active: true,
    date_joined: '2024-01-01T00:00:00Z',
    ...overrides,
  }),

  // Create test item data
  createTestItem: (overrides = {}) => ({
    id: 1,
    title: 'Test Item',
    description: 'This is a test item',
    owner: 1,
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
    ...overrides,
  }),
};

// Export the store creation function
export { createTestStore };
