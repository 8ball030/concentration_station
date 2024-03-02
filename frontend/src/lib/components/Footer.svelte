<script>
	// @ts-nocheck

	import { transactionLink, recentTrx, currentCoin } from '$lib/stores';

	let explorerLink = '';
	let coin = null;
	let transactions = [
		{
			hash: '0x20d0fda3b4bfbac76ed7d9fe9f6b669b50ad3e94d6a1bacc047584afe9f7ef53',
			link: explorerLink
		},
		{
			hash: '0x20d0fda3b4bfbac76ed7d9fe9f6b669b50ad3e94d6a1bacc047584afe9f7ef53',
			link: explorerLink
		}
	];

	transactionLink.subscribe((value) => {
		explorerLink = value;
	});
	currentCoin.subscribe((value) => {
		coin = value;
	});
</script>

<hr class="opacity-50" />
<div class="text-center">
	<div class="flex justify-between footer font-bold">
		<div class="flex footer gap-10">
			<img
				src={coin?.data?.sparkline || 'https://www.coingecko.com/coins/16801/sparkline.svg'}
				class="bg-black/50 aspect-[21/9]"
				alt="Post"
			/>
			<h4 class="text-tertiary-100 p-10">Token Price: {coin?.data?.price || 'n/a'}</h4>
		</div>
		<div class="flex gap-10 justify-start text-tertiary-300 p-10">
			<div>Nework Activity:</div>
			{#each transactions as trx}
				<div class="text-tertiary-300">
					`👍🏼 {trx.hash.slice(0, 6)}..
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.footer {
		align-items: center;
	}
</style>
