<script>
	// @ts-nocheck

	import { transactionLink, recentTrx } from '$lib/stores';

	let explorerLink = '';
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
	// recentTrx.subscribe((value) => {
	// 	if (value) {
	// 		transactions = value;
	// 	}
	// });
</script>

<div class="p-2 text-center">
	<h3 class="text-tertiary-100">Recently Active Transations</h3>
	{#each transactions as trx}
		<div class="flex justify-center text-center">
			<small class="text-tertiary-300">
				`👍🏼 Transaction hash {trx.hash}
			</small>
			<!-- <button class="btn btn-sm variant-ghost-secondary"
				><a href={trx.link}>See on Exlorer</a></button
			> -->
		</div>
	{/each}
</div>
