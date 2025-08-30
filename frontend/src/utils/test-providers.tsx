import React from 'react';
import type { ReactElement } from 'react';
import { render } from '@testing-library/react';
import type { RenderOptions } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { configureStore } from '@reduxjs/toolkit';

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
const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => {
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

  return render(ui, { wrapper: AllTheProviders, ...options });
};

// Export custom render function
export { customRender as render };

// Export the store creation function
export { createTestStore };
