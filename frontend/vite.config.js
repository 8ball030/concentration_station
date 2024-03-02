import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { NodeGlobalsPolyfillPlugin } from '@esbuild-plugins/node-globals-polyfill'
// @ts-nocheck

import { resolve } from 'path';
import { NodeModulesPolyfillPlugin } from '@esbuild-plugins/node-modules-polyfill';
import nodePolyfills from 'rollup-plugin-polyfill-node';
import cjs from '@rollup/plugin-commonjs';

// https://vitejs.dev/config/

export default defineConfig({
    // envDir: "./env_web",
	plugins: [sveltekit(), purgeCss({
			safelist: {
				// any selectors that begin with "hljs-" will not be purged
				greedy: [/^hljs-/],
			},
		}),
	],
    build: {
      // minify: false,
      // target: "es2015",
      sourcemap: true,
      commonjsOptions: { include: [] },
      rollupOptions: {
        plugins: [
          // Enable rollup polyfills plugin
          // used during production bundling
          nodePolyfills({
            include: ['node_modules/**/*.js', '../../node_modules/**/*.js'],
          }),
          cjs(),
        ],
      },
    },
    resolve: {
      alias: {
        // '@': resolve(__dirname, 'src'),
		http: 'rollup-plugin-node-polyfills/polyfills/http',
		https: 'rollup-plugin-node-polyfills/polyfills/http',
        process: 'rollup-plugin-node-polyfills/polyfills/process-es6',
        buffer: 'rollup-plugin-node-polyfills/polyfills/buffer-es6',
        events: 'rollup-plugin-node-polyfills/polyfills/events',
        util: 'rollup-plugin-node-polyfills/polyfills/util',
        sys: 'util',
        stream: 'rollup-plugin-node-polyfills/polyfills/stream',
        _stream_duplex:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/duplex',
        _stream_passthrough:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/passthrough',
        _stream_readable:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/readable',
        _stream_writable:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/writable',
        _stream_transform:
          'rollup-plugin-node-polyfills/polyfills/readable-stream/transform',
      },
    },
    optimizeDeps: {
      esbuildOptions: {
        // Node.js global to browser globalThis
        define: {
          global: 'globalThis',
        },
        // Enable esbuild polyfill plugins
        plugins: [
          NodeGlobalsPolyfillPlugin({
            process: true,
			buffer: false,
          }),
          NodeModulesPolyfillPlugin(),
        ],
      },
    },
  }
)
// export default defineConfig({
// 	plugins: [sveltekit(), purgeCss({
// 			safelist: {
// 				// any selectors that begin with "hljs-" will not be purged
// 				greedy: [/^hljs-/],
// 			},
// 		}),
// 	],
// 	optimizeDeps: {
// 		esbuildOptions: {
// 		    define: {
// 			   global: 'globalThis',
// 		  },
// 		  plugins: [
// 			NodeGlobalsPolyfillPlugin({
// 			  process: true,
// 			  buffer: true,
// 			}),
// 		  ],
// 		},
// 	},
// 	resolve: {
// 		alias: {
// 			stream: 'stream-browserify',
// 			https: 'agent-base', 
// 		}
// 	},
// 	build: {
// 		commonjsOptions: {
// 			include: [],
// 			transformMixedEsModules: true,
// 		},
// 	},
// 	define: {
// 		// By default, Vite doesn't include shims for NodeJS/
// 		// necessary for segment analytics lib to work
// 		global: {},
// 	},
// })