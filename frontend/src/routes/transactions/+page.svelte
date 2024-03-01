<script>
	import { onMount } from "svelte";
	import { transactionsMock } from "$lib/mock";
    import {getTransactions} from '$lib/actions';

	// TODO: remove mock
	let transactionsArray = Promise.resolve(transactionsMock)

	onMount(() => {
		// transactionsArray = getTransactions()
	});
</script>

<div class="table-container p-10">
	{#await transactionsArray then transactionsArray}
		<h3 class="mb-2 text-xl">List of Transactions</h3>
		<table class="table table-hover">
			<thead>
				<tr>
					<th>ID</th>
					<th>Coin</th>
					<th>Amount</th>
					<th>Price</th>
					<th>Action</th>
					<th>Hash</th>
					<th>Date</th>
				</tr>
			</thead>
			<tbody>
				{#each transactionsArray as row, i}
					<tr>
						<td>{row.id}</td>
						<td>{row.coin}</td>
						<td>{row.amount}</td>
						<td>{row.price}</td>
						<td>{row.side}</td>
						<td>{row.tx_hash}</td>
						<td>{row.timestamp}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/await}
</div>