<script>
	// @ts-nocheck
	import { onMount } from "svelte";
	import Lazy from 'svelte-lazy';
	import { LikedCoins } from '$lib/likedCoins';

	/**
	 * @type {any[]}
	 */
	let coinsList = [];
	/**
	 * @type {null}
	 */
	let show = null;

	/**
	 * @param {any} url
	 */
	function toggleShow(url) {
		show = show ? null : url;
	}

	const likedCoinsList = new LikedCoins();
	
	onMount(() => {
		likedCoinsList.likedCoinsList.forEach((val) => {
			coinsList = [...coinsList, val]
		})
	});

</script>

<div class="grid h-full grid-cols-1 place-items-center gap-4 md:grid-cols-2">
	
	 {#each coinsList as coin}
	 	{#if coin.large}
			<Lazy height={250} offset={0}>
				<div
					role="presentation"
					class="card relative w-96 bg-base-200 shadow-xl"
					on:mouseenter={() => toggleShow(coin.large)}
					on:mouseleave={() => toggleShow(coin.large)}
				>
					<figure>
						<img class="h-60 object-cover" src={coin.large} alt="Dog" />
					</figure>
					{#if show === coin.large}
						<button
							class="btn btn-circle btn-error absolute right-0 top-0"
							on:click={() => likedCoinsList.remove(coin.large)}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-6 w-6"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								><path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M6 18L18 6M6 6l12 12"
								/></svg
							>
						</button>
					{/if}
				</div>
			</Lazy>
		{/if}
	 {/each}
</div>
