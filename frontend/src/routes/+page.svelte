<script>
	// @ts-nocheck
	import { onMount } from 'svelte';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import io from 'socket.io-client';

	import Card from '$lib/components/Card.svelte';
	import { state, mode, chain } from '$lib/stores';
	import { LikedCoins } from '$lib/likedCoins';
	import { getCurrentCoin, getLedgers, postSwap } from '$lib/actions';
	import {
		SOCKET_URL,
		INTENTION_DIRECTIONS,
		MOVE_DIRECTION,
		APP_MODE,
		CHAIN_ID_TO_LEDGER_ID
	} from '$lib/consts';
	import { transactionLink, likedCount, recentTrx, currentCoin } from '$lib/stores';
	import * as buffer from 'buffer';

	const socket = io(SOCKET_URL, {});

	$: connection_status = socket.connected;

	let chainId;
	let coin = null;
	let cardList = [0];
	let explorerLink = '';
	let longestStreak = 0;

	// states
	$: loading = false;
	let handling = false;
	let count = 0;

	$: modeValue = '';

	const toastStore = getToastStore();

	// store subscriptions
	transactionLink.subscribe((value) => {
		explorerLink = value;
	});
	likedCount.subscribe((val) => {
		count += val;
	});
	state.subscribe((value) => {
		cardList = value;
	});

	async function handleSubmitMode(val) {
		const res = await postMode(val);
	}

	$: mode.subscribe((value) => {
		modeValue = value;
		if (value === APP_MODE.DEGEN || value === APP_MODE.AGENT) {
			handleSubmitMode(value);
			socket.connect();
		} else {
			socket.disconnect();
		}
	});

	$: chain.subscribe((value) => {
		chainId = value;
	});

	onMount(() => {
		// this is needed to address errors similar to https://github.com/vitejs/vite/issues/9703
		if (typeof window.global === 'undefined') {
			window.global = window;
		}
		if (typeof window.Buffer === 'undefined') {
			window.Buffer = buffer.Buffer;
		}

		socket.on('connect', () => {
			toastStore.trigger(STATUS_MSGS.AGENT_SUCCESS);
			connection_status = true;
		});

		socket.on('disconnect', () => {
			connection_status = false;
			toastStore.trigger(STATUS_MSGS.AGENT_FAIL);
		});

		socket.on('data', (data) => {
			if (APP_MODE.DEGEN === modeValue) {
				if (!handling && coin?.id) {
					const intention = JSON.parse(data).intention;
					const row = coin?.id + ' ' + intention;
					toastStore.trigger(STATUS_MSGS.AGENT_DATA(row));
					updateActiveCard(intention);
					handleIntention(intention);
				}
			}
		});

		getCoin();
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

		if (!res.error) {
			getCoin();
			updateActiveCard();

			if (intentionDirection === INTENTION_DIRECTIONS.LIKE) {
				toastStore.trigger(STATUS_MSGS.TX_SUCCESS);
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
		toastStore.trigger(STATUS_MSGS.API_ERROR(endpoint, err));
	}
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
<div class="place-items-center mt-20">
	{#each cardList as dummy (dummy)}
		<Card {loading} {coin} {chainId} onbuttonTapped={handleIntention} />
	{/each}
</div>
