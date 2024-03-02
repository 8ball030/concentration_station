<script>
	// @ts-nocheck
	import { onMount } from 'svelte';
	import { ProgressBar, getToastStore } from '@skeletonlabs/skeleton';
	import io from 'socket.io-client';

	import Card from '$lib/components/Card.svelte';
	import { state, mode, chain, currentCoin, likedCount } from '$lib/stores';
	import { getCurrentCoin, getLedgers, postSwap } from '$lib/actions';
	import {
		SOCKET_URL,
		INTENTION_DIRECTIONS,
		MOVE_DIRECTION,
		APP_MODE,
		CHAIN_ID_TO_LEDGER_ID
	} from '$lib/consts';
	import { transactionLink } from '$lib/stores';

	const { DISLIKE, LIKE } = INTENTION_DIRECTIONS;
	const socket = io(SOCKET_URL, {});

	$: connection_status = socket.connected;

	let chainId;
	let coin = null;
	let cardList = [0];
	let explorerLink = '';
	let longestStreak = 0;
	let count = 0;

	$: index = 0;

	// states
	let loading = false;
	let handling = false;

	$: modeValue = '';
	$: outMoveDirection = 0;

	const toastStore = getToastStore();
	const succssesToast = {
		message: `👍🏼 Transaction hash <br/> 0x20d0fda3b4bfbac76ed7d9fe9f6b669b50ad3e94d6a1bacc047584afe9f7ef53`,
		action: {
			label: 'See on Exlorer',
			response: () => window.open(explorerLink, '_blank').focus()
		},
		timeout: 1000,
		background: 'variant-filled-success',
		button: 'variant-ghost-success',
		classes: 'success-toast',
		max: 1
	};

	transactionLink.subscribe((value) => {
		explorerLink = value;
	});
	likedCount.subscribe((val) => {
		count += val;
	});
	state.subscribe((value) => {
		cardList = value;
	});

	$: mode.subscribe((value) => {
		modeValue = value;
		if (value === APP_MODE.DEGEN || value === APP_MODE.AGENT) {
			socket.connect();
		} else {
			socket.disconnect();
		}
	});

	$: chain.subscribe((value) => {
		chainId = value;
	});

	onMount(() => {
		socket.on('connect', () => {
			const setting = {
				message: 'Successfully connected to the agent!',
				timeout: 3000,
				background: 'variant-ghost-success',
				max: 1
			};
			toastStore.trigger(setting);
			connection_status = true;
		});

		socket.on('disconnect', () => {
			connection_status = false;
			const setting = {
				message: 'Disconnected from the agent!',
				timeout: 3000,
				background: 'variant-ghost-error',
				max: 1
			};
			toastStore.trigger(setting);
		});

		socket.on('data', (data) => {
			if (APP_MODE.DEGEN === modeValue) {
				if (!handling && coin?.id) {
					const intention = JSON.parse(data).intention;
					const row = coin?.id + ' ' + intention;
					const intentToast = {
						message: '🔮 ' + row + ' 🔮',
						timeout: 2500,
						background: 'variant-ghost-info',
						classes: 'info-toast',
						position: 't',
						max: 1
					};
					toastStore.trigger(intentToast);
					updateActiveCard(intention);
					handleIntention(intention);
				}
			}
		});
	});

	state.subscribe((value) => {
		cardList = value;
	});

	function updateActiveCard() {
		cardList = [cardList.slice(1)];
		handling = false;
	}

	// when we get intention from socket submit a swap on liked ( 'right' )
	async function handleIntention(intentionDirection) {
		// data shape {'intention': random.choice(['LEFT', 'RIGHT'])}
		loading = true;
		handling = true;
		const res = await postSwap(
			coin.id,
			intentionDirection,
			CHAIN_ID_TO_LEDGER_ID[chainId],
			handleApiError
		);

		if (!res?.error) {
			getCoin();
			updateActiveCard();

			if (intentionDirection === INTENTION_DIRECTIONS.LIKE) {
				const submittedToast = {
					message: `🤞🏼 Transaction submitted 🤞🏼`,
					timeout: 1000,
					max: 1
				};
				toastStore.trigger(submittedToast);
				// TODO: some check here with a callback to get the transaction hash
				toastStore.trigger(succssesToast);
			}
		} else {
			handling = false;
		}
		loading = false;
	}

	async function getCoin() {
		let res = await getCurrentCoin(handleApiError);
		if (!res?.error) {
			currentCoin.set(res);
			coin = res;
		}
	}

	function handleApiError(endpoint, err) {
		const errorToast = {
			message: ` =( ${err} ${endpoint}`,
			background: 'variant-filled-error',
			classes: 'error-toast'
		};
		toastStore.trigger(errorToast);
	}

	onMount(() => {
		getCoin();
	});
</script>

<div class="flex justify-between">
	<div class="font-semibold flex gap-10 p-10">
		{#if coin?.name}
			<div>{coin?.name} - Market Cap: {coin?.data?.market_cap || ''}</div>
			<div>Total Volume: {coin?.data?.total_volume || ''}</div>
		{/if}
	</div>
	<div class="font-semibold flex gap-10 p-10">
		<div>Current Streak: {count}</div>
		<div>Longest Streak: {longestStreak}</div>
	</div>
</div>
<hr class="opacity-50" />
<div class="flex justify-center">
	<button
		disabled={!coin?.name}
		class="btn btn-outline btn-primary btn-lg"
		on:click={() => {
			outMoveDirection = MOVE_DIRECTION[DISLIKE];
			handleIntention(DISLIKE, coin, chainId);
		}}
	>
		<img class="like" src="./left.png" alt="left" />
	</button>
	<div class="place-items-center mt-20">
		{#each cardList as dummy (dummy)}
			<Card {loading} {coin} {chainId} {outMoveDirection} />
		{/each}
	</div>
	<button
		disabled={!coin?.name}
		class="btn btn-outline btn-secondary btn-lg"
		on:click={() => {
			outMoveDirection = MOVE_DIRECTION[LIKE];
			handleIntention(LIKE, coin, chainId);
		}}
	>
		<img class="like" src="./right.png" alt="right" />
	</button>
</div>

<style>
</style>
