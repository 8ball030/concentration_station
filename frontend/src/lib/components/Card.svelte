<script>
	// @ts-nocheck
	import { fly, scale } from 'svelte/transition';
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import { INTENTION_DIRECTIONS, MOVE_DIRECTION } from '$lib/consts';

	export let onbuttonTapped;
	export let coin;
	export let chainId;
	export let loading;

	const { DISLIKE, LIKE } = INTENTION_DIRECTIONS;
	let outMoveDirection;
</script>

<div class="flex justify-center">
	<button
		disabled={!coin?.name}
		class="btn btn-outline btn-primary btn-lg"
		on:click={() => {
			outMoveDirection = MOVE_DIRECTION[DISLIKE];
			onbuttonTapped(DISLIKE, coin, chainId);
		}}
	>
		<img class="like" src="./left.png" alt="left" />
	</button>
	<div class="stack grid">
		<h2 class="page-sub mb-10">Do you like this coin?</h2>
		<div
			class="card w-96 bg-base-200 shadow-xl items-center coin-card"
			in:scale|global={{ delay: 200, duration: 300 }}
			out:fly|global={{
				delay: outMoveDirection ? 100 : 0,
				duration: outMoveDirection ? 400 : 0,
				x: outMoveDirection
			}}
		>
			<header>
				<img
					src={coin?.large ||
						'https://assets.coingecko.com/coins/images/16801/large/ufo.png?1696516371'}
					class="bg-black/50 w-full aspect-[21/9] coin-image"
					alt="Post"
				/>
			</header>
			{#if coin}
				<div class="p-4 space-y-4">
					<h2 class="h2 coin-name">{coin?.name || 'n/a'}</h2>
				</div>
			{:else}
				<div class="p-4 space-y-4">Processing...</div>
			{/if}
		</div>
		{#if loading}
			<div class="w-96">
				<ProgressBar value={undefined} />
			</div>
		{/if}
	</div>
	<button
		disabled={!coin?.name}
		class="btn btn-outline btn-secondary btn-lg"
		on:click={() => {
			outMoveDirection = MOVE_DIRECTION[LIKE];
			onbuttonTapped(LIKE, coin, chainId);
		}}
	>
		<img class="like" src="./right.png" alt="right" />
	</button>
</div>

<style>
	.coin-card {
		height: 523px;
		width: 468px;
		padding: 10px;
		border-radius: 28.33px;
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
	}
	.like:hover {
		opacity: 0.8;
	}
</style>
