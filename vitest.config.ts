import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    include: ['instrument/**/*.test.ts', 'analysis/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      include: ['instrument/lib/**/*.ts', 'analysis/code/**/*.ts'],
      exclude: ['**/*.test.ts', '**/*.d.ts'],
    },
  },
  resolve: {
    alias: {
      '@instrument': './instrument/lib',
      '@analysis': './analysis',
    },
  },
});
