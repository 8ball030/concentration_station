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
	
	$: modeValue = ""
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
		classes: 'success-toast',
		max: 1
	};

	transactionLink.subscribe((value) => {
		explorerLink = value;
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
		chain_id = value;
	});

	onMount(() =>{
		socket.on('connect', () => {
			const setting = {
				message: 'Successfully connected to the agent!',
				timeout: 3000,
				background: 'variant-ghost-success',
				max: 1
			};
			toastStore.trigger(setting)
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
			toastStore.trigger(setting)
		});
		
		socket.on('data', (data) => {

			if (APP_MODE.DEGEN === modeValue) {
				if (!handling && coin?.id) {

					const intention = JSON.parse(data).intention;
					const row = coin?.id + " " + intention;
					const intentToast = {
						message: "🔮 " + row + " 🔮",
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
	})

	state.subscribe((value) => {
		cardList = value;
	});

	function updateActiveCard(intentionDirection) {
		console.log('updateActiveCard', intentionDirection)
		outMoveDirection = MOVE_DIRECTION[intentionDirection];
		cardList = [cardList.slice(1)];

		handling = false
	}

	function handleUpdateLiked(intentionDirection) {
		if (intentionDirection === INTENTION_DIRECTIONS.DISLIKE) {
			// likedCoinsList.remove(coin);
		} else {
			// likedCoinsList.add(coin);
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
			updateActiveCard(intentionDirection)
			
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
			chainId={chain_id}
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
