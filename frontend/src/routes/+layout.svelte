<script>
	// @ts-nocheck

	import '../app.postcss';
	import { AppShell, AppBar, Modal, Toast, initializeStores } from '@skeletonlabs/skeleton';
	import { base } from '$app/paths';
	import SelectMode from '$lib/components/SelectMode.svelte';
	import Connect from '$lib/components/Connect.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import SelectChain from '$lib/components/SelectChain.svelte';

	// Highlight JS
	import hljs from 'highlight.js/lib/core';
	import 'highlight.js/styles/github-dark.css';
	import { storeHighlightJs } from '@skeletonlabs/skeleton';
	import xml from 'highlight.js/lib/languages/xml'; // for HTML
	import css from 'highlight.js/lib/languages/css';
	import javascript from 'highlight.js/lib/languages/javascript';
	import typescript from 'highlight.js/lib/languages/typescript';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';

	hljs.registerLanguage('xml', xml); // for HTML
	hljs.registerLanguage('css', css);
	hljs.registerLanguage('javascript', javascript);
	hljs.registerLanguage('typescript', typescript);
	storeHighlightJs.set(hljs);

	initializeStores();
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
</script>

<Toast />
<Modal />
<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<div class="flex gap-20">
					<strong class="text-xl">
						<a href={`/`} rel="noreferrer"> Speculation Station </a>
					</strong>
					<a class="text-xl" href={`${base}/profile`}> Profile </a>
					<a class="text-xl" href={`${base}/activity`}> Activity </a>
				</div>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<SelectMode />
				<SelectChain />
				<a
					class="btn btn-sm variant-ghost-surface"
					href={`${base}/liked`}
					target="_blank"
					rel="noreferrer"
				>
					❤️
				</a>
				<Connect />
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />
	<svelte:fragment slot="pageFooter">
		<Footer />
	</svelte:fragment>
</AppShell>
