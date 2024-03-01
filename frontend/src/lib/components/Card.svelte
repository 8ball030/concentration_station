<script>
	// @ts-nocheck
	import { fly, scale } from 'svelte/transition';
	import { LikedCoins } from '$lib/likedCoins';
	import {INTENTION_DIRECTIONS} from '$lib/consts';

	export let onbuttonTapped;
	export let coin;
	console.log("coin", coin)
	const likedCoinsList = new LikedCoins();

	let outMoveDirection = 0;
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
		<img src={coin?.data?.sparkline} class="bg-black/50 w-full aspect-[21/9]" alt="Post">
	</header> 
	<div class="p-4 space-y-4">
		<div class="flex gap-4">
			<figure class="avatar flex aspect-square text-surface-50 font-semibold justify-center items-center overflow-hidden isolate bg-surface-400-500-token w-8  rounded-full   " data-testid="avatar">
				<img class="avatar-image w-full object-cover" src={coin?.small} alt="" style="">
			</figure> 
			<h3 class="h3">{coin?.name}</h3> 
		</div>
		<div class="flex-auto flex justify-between items-center pt-2">
			<h6 class="font-bold">Market Cap</h6> 
			<small>{coin?.data?.market_cap}</small>
		</div>
		<div class="flex-auto flex justify-between items-center">
			<h6 class="font-bold">Total Volume</h6> 
			<small>{coin?.data?.total_volume}</small>
		</div>
	</div>
	<hr class="opacity-50"> 
	<footer class="items-center text-center p-2">
		<h2 class="card-title pt-2">Do You like This Coin ?</h2>
		<div class="card-actions justify-center">
			<button
				class="btn btn-outline btn-primary btn-lg"
				on:click={() => {
					console.log("here")
					likedCoinsList.remove(coin);
					outMoveDirection = -400;
					onbuttonTapped(INTENTION_DIRECTIONS.DISLIKE);
				}}
			>
				💔
			</button>
			<button
				class="btn btn-outline btn-secondary btn-lg"
				on:click={async () => {
					likedCoinsList.add(coin);
					outMoveDirection = 400;
					onbuttonTapped(INTENTION_DIRECTIONS.LIKE, coin);

				}}
			>
				❤️
			</button>
		</div>
	</footer>
</div>

