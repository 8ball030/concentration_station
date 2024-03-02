<script>
	// @ts-nocheck
	import { CHAIN_MODE, CHAIN_NAME, DEFAULT_CHAIN } from '$lib/consts';
	import { chain } from '$lib/stores';

	let chainSlectOpen = false;
	let selectedChain = DEFAULT_CHAIN;

	function toggleChain() {
		chainSlectOpen = !chainSlectOpen;
	}
	function selectMode(selectedMdoe) {
		chain.set(selectedMdoe);
		chainSlectOpen = false;
	}

	chain.set(CHAIN_MODE.ARBITRUM);

	chain.subscribe((value) => {
		selectedChain = value;
	});

	// TODO: add mode descriptions
</script>

<div>
	<div class="mr-24 select" on:click={toggleChain}>{CHAIN_NAME[selectedChain]}</div>
	{#if chainSlectOpen}
		<dl class="list-dl select-list bg-surface-100-800-token">
			<div>
				<div on:click={() => selectMode(CHAIN_MODE.MAINNET)} class="flex-auto">
					<dt>Ethereum</dt>
				</div>
			</div>
			<div>
				<div on:click={() => selectMode(CHAIN_MODE.ARBITRUM)} class="flex-auto">
					<dt>Arbitrum</dt>
				</div>
			</div>
		</dl>
	{/if}
</div>

<style>
	.select {
		cursor: pointer;
	}
	.select-list {
		position: absolute;
		right: 264px;
		top: 74px;
		padding: 8px;
		width: 212px;
	}
	dt:hover {
		background: #6376a3;
	}
</style>
