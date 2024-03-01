<script>
	// @ts-nocheck
	import { onMount } from "svelte";
	import { ProgressBar, getToastStore } from '@skeletonlabs/skeleton';
	import io from 'socket.io-client';

	import Card from '$lib/components/Card.svelte';
	import {state, mode, chain} from '$lib/stores'
	import { LikedCoins } from '$lib/likedCoins';
	import {getCurrentCoin, getLedgers, postSwap} from '$lib/actions';
	import {SOCKET_URL, INTENTION_DIRECTIONS, MOVE_DIRECTION, APP_MODE} from '$lib/consts'
    import {transactionLink} from '$lib/stores'

	const socket = io(SOCKET_URL, {});
	
	$: connection_status = socket.connected;

	let chain_id;
	let coin = {}
	let cardList = [0]
    let explorerLink = ''
	const likedCoinsList = new LikedCoins();

	// states
	let loading = false
	let handling = false;
	$:outMoveDirection = 0;

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
		classes: 'success-toast'
	};

	transactionLink.subscribe((value) => {
		explorerLink = value;
	});

	$: mode.subscribe((value) => {
		console.log('mode', value)
		if (value === APP_MODE.DEGEN) {
			// we want to call connect on the socket
			socket.connect();
		} else {
			socket.disconnect();
		}
	});

	$: chain.subscribe((value) => {
		chain_id = value;
	});

	


	onMount(() =>{
		// we want to call connect on the socket

		socket.on('connect', () => {
			const setting = {
				message: 'Successfully connected to the agent!',
				timeout: 3000,
				background: 'variant-ghost-success'
			};
			toastStore.trigger(setting)
			connection_status = true;
			socket.emit('agent', 'agent');
		});

		socket.on('disconnect', () => {
			connection_status = false;
			const setting = {
				message: 'Disconnected from the agent!',
				timeout: 3000,
				background: 'variant-ghost-error'
			};
			toastStore.trigger(setting)
		});

		
		socket.on('data', (data) => {
			if (!handling && coin?.id) {
				handleIntention(data?.intention);
			}
		});
	})

	state.subscribe((value) => {
		cardList = value;
	});

	function updateActiveCard(intentionDirection) {
		outMoveDirection = MOVE_DIRECTION[intentionDirection];
		cardList = [...cardList.slice(1), Math.max(...cardList) + 1];
		handling = false
	}

	function handleUpdateLiked(intentionDirection) {
		if (intentionDirection === INTENTION_DIRECTIONS.DISLIKE) {
			likedCoinsList.remove(coin);
		} else {
			likedCoinsList.add(coin);
		}
	}

	// when we get intention from socket submit a swap on liked ( 'right' ) 
	async function handleIntention(intentionDirection) {
		handleUpdateLiked()
		// data shape {'intention': random.choice(['LEFT', 'RIGHT'])}
		loading = true
		handling = true

		const res = await postSwap(coin.id, intentionDirection, chain_id, handleApiError)

		if (res) {
			getCoin()
			toastStore.trigger(succssesToast);
			updateActiveCard(intentionDirection)
		} else {
			handling = false
		}
		loading = false
	}

	async function getCoin(){
		coin = await getCurrentCoin(handleApiError)
	}
	
	function handleApiError(endpoint, err){
		const errorToast = {
			message: ` =( ${err} ${endpoint}`,
			background: 'variant-filled-error',
			classes: 'error-toast'
		};
		toastStore.trigger(errorToast);
	}
	
	onMount(() => {
		getCoin()
	});
</script>

<div class="stack grid place-items-center mt-40">
	{#each cardList as dummy (dummy)}
		<Card
			coin={coin}
			outMoveDirection={outMoveDirection}
			onbuttonTapped={handleIntention} />
	{/each}
	{#if loading}
		<div class="w-96">
			<ProgressBar value={undefined} />
		</div>
	{/if}
</div>

<style>
</style>
