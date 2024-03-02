<script>
	// @ts-nocheck
	import { onMount } from 'svelte';

	export let account;
	export let profile;
	console.log('profile', profile);
	import { ERC725 } from '@erc725/erc725.js';
	import lsp4Schema from '@erc725/erc725.js/schemas/LSP4DigitalAsset.json';
	import { INTERFACE_IDS } from '@lukso/lsp-smart-contracts/dist/constants.cjs.js';

	const coinImg = 'https://assets.coingecko.com/coins/images/16801/large/ufo.png?1696516371';
	const myAsset = new ERC725(lsp4Schema, account, 'https://rpc.testnet.lukso.gateway.fm', {
		ipfsGateway: 'https://api.universalprofile.cloud/ipfs'
	});

	async function getAssets() {
		const isLSP7 = await myAsset.supportsInterface(INTERFACE_IDS.LSP7DigitalAsset);
		const isLSP8 = await myAsset.supportsInterface(INTERFACE_IDS.LSP8IdentifiableDigitalAsset);
		console.log(isLSP7, isLSP8);
	}

	onMount(() => {
		getAssets();
	});
</script>

<div class="flex">
	<div
		class="card coin-card variant-ghost-primary card-hover overflow-hidden"
		href="/elements/cards"
	>
		<header>
			<img
				src={profile?.backgroundImage?.[0]?.url.replace(
					'ipfs://',
					'https://api.universalprofile.cloud/ipfs/'
				) || 'https://picsum.photos/200'}
				class="bg-black/50 w-full aspect-[21/9] coin-image"
				alt="bg"
			/>
		</header>
		<div class="p-4 space-y-4">
			<figure
				class="avatar flex aspect-square text-surface-50 font-semibold justify-center items-center overflow-hidden isolate bg-surface-400-500-token w-10 rounded-full"
				data-testid="avatar"
			>
				<img
					class="avatar-image w-full object-cover"
					src="https://images.unsplash.com/photo-1617296538902-887900d9b592?ixid=M3w0Njc5ODF8MHwxfGFsbHx8fHx8fHx8fDE2ODc5NzExMDB8&amp;ixlib=rb-4.0.3&amp;w=32&amp;h=32&amp;auto=format&amp;fit=crop"
					alt=""
					style=""
				/>
			</figure>
			<h6 class="h6">{account || '0x'}</h6>
			<h3 class="h3 coin-name">{profile?.name || 'Anonymous'}</h3>
			<article>
				<p>{profile?.descption || 'Hello!'}</p>
			</article>
		</div>
		<hr class="opacity-50" />
		<footer class="p-4 flex justify-start items-center space-x-4">
			<div class="flex-auto flex justify-between items-center">
				<h6 class="font-bold" data-toc-ignore="">Amount Value</h6>
				<div>324</div>
			</div>
			<div class="flex-auto flex justify-between items-center">
				<h6 class="font-bold" data-toc-ignore="">Score</h6>
				<div>5</div>
			</div>
			<div class="flex-auto flex justify-between items-center">
				<h6 class="font-bold" data-toc-ignore="">Anoun</h6>
				<div>324</div>
			</div>
		</footer>
	</div>
	<div class="details-card card variant-ghost-secondary">
		<h2 class="page-sub">Your Library</h2>
		<div class="flex flex-wrap mt-4">
			<div class="token-card">
				<img src={coinImg} alt="coinImg" />
			</div>
			<div class="token-card">
				<img src={coinImg} alt="coinImg" />
			</div>
			<div class="token-card">
				<img src={coinImg} alt="coinImg" />
			</div>
		</div>
	</div>
</div>

<style>
	.details-card {
		height: 717px;
		width: 688px;
		padding: 10px;
		border-radius: 28.33px;
		margin-left: 25px;
	}
	.coin-card {
		height: 717px;
		width: 468px;
		padding: 10px;
		border-radius: 28.33px;
	}
	.token-card {
		height: 160px;
		width: 160px;
		padding: 10px;
		border-radius: 28.33px;
	}
	.token-card img {
		border-radius: 10px;
	}
	.coin-image {
		border-radius: 28.33px;
		height: 428px;
	}
	.coin-name {
		font-size: 32px;
		font-size: bold;
	}
	.page-sub {
		font-size: 28px;
		font-weight: 600;
		text-align: center;
		margin-top: 10px;
	}
</style>
