<script>
	// @ts-nocheck
	import { fly, scale } from 'svelte/transition';
	import { INTENTION_DIRECTIONS, MOVE_DIRECTION } from '$lib/consts';

	export let onbuttonTapped;
	export let coin;
	export let chainId;

	const { DISLIKE, LIKE } = INTENTION_DIRECTIONS;
	let outMoveDirection;
</script>

<div
	class="card w-96 bg-base-200 shadow-xl items-center"
	in:scale|global={{ delay: 200, duration: 300 }}
	out:fly|global={{
		delay: outMoveDirection ? 100 : 0,
		duration: outMoveDirection ? 400 : 0,
		x: outMoveDirection
	}}
>
	<header>
		<img
			src={coin?.data?.sparkline || 'https://www.coingecko.com/coins/16801/sparkline.svg'}
			class="bg-black/50 w-full aspect-[21/9]"
			alt="Post"
		/>
	</header>
	{#if coin}
		<div class="p-4 space-y-4">
			<div class="flex gap-4">
				<figure
					class="avatar flex aspect-square text-surface-50 font-semibold justify-center items-center overflow-hidden isolate bg-surface-400-500-token w-8 rounded-full"
					data-testid="avatar"
				>
					<img class="avatar-image w-full object-cover" src={coin?.small} alt="" style="" />
				</figure>
				<h3 class="h3">{coin?.name || 'n/a'}</h3>
			</div>
			<div class="flex-auto flex justify-between items-center pt-2">
				<h6 class="font-bold">Market Cap</h6>
				<small>{coin?.data?.market_cap || 'n/a'}</small>
			</div>
			<div class="flex-auto flex justify-between items-center">
				<h6 class="font-bold">Total Volume</h6>
				<small>{coin?.data?.total_volume || 'n/a'}</small>
			</div>
		</div>
		<hr class="opacity-50" />
		<footer class="items-center text-center p-2">
			<h2 class="card-title pt-2">Do You like This Coin ?</h2>
			<div class="card-actions justify-center">
				<button
					class="btn btn-outline btn-primary btn-lg"
					on:click={() => {
						outMoveDirection = MOVE_DIRECTION[DISLIKE];
						onbuttonTapped(DISLIKE, coin, chainId);
					}}
				>
					💔
				</button>
				<button
					class="btn btn-outline btn-secondary btn-lg"
					on:click={() => {
						outMoveDirection = MOVE_DIRECTION[LIKE];
						onbuttonTapped(LIKE, coin, chainId);
					}}
				>
					❤️
				</button>
			</div>
		</footer>
	{:else}
		<div class="p-4 space-y-4">Processing...</div>
	{/if}
</div>
