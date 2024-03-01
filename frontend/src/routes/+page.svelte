<script>
// @ts-nocheck
	import { onMount } from "svelte";
	import { fly } from 'svelte/transition'
	import { quintOut } from 'svelte/easing';
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import io from 'socket.io-client';

	import TransactionFrame from '$lib/components/TransactionFrame.svelte';
	import Card from '$lib/components/Card.svelte';
	import {state} from '$lib/stores'
	import {getCurrentCoin, getLedgers, postSwap} from '$lib/actions';
	import {SOCKET_URL, DEFAULT_CHAIN, INTENTION_DIRECTIONS} from '$lib/consts'
	import {mockCoin} from '$lib/mock'
	
	const socket = io(SOCKET_URL, {});
	
	$: connection_status = socket.connected;

	// transaciton modal
	const modalStore = getModalStore();
    const modalComponent = { ref: TransactionFrame };

    const modal = {
        type: 'component',
        component: modalComponent,
    };

	let cardDummyList = [0]
	let index = 0
	let coin = {}
  	let animate = false
	let loading = false

	onMount(() =>{
		// we want to call connect on the socket
		socket.connect();

		socket.on('connect', () => {
			console.log('Successfully connected to the agent!')
			const setting = {
				message: 'Successfully connected to the agent!',
				timeout: 3000,
				background: 'variant-ghost-success'
			};

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
		});

		socket.on('data', (data) => {
			console.log('intention', data)
			
			//handleIntention(data?.intention);
		});
	})

	state.subscribe((value) => {
		cardDummyList = value;
	});


	function updateActiveCard() {
		cardDummyList = [...cardDummyList.slice(1), Math.max(...cardDummyList) + 1];
		index +=1
	}

	// when we get intention from socket submit a swap on liked ( 'right' ) 
	async function handleIntention(intentionDirection) {
		// data shape {'intention': random.choice(['LEFT', 'RIGHT'])}
		if (intentionDirection === INTENTION_DIRECTIONS.LIKE) {
			loading = true

			const res = await postSwap(coin.id, DEFAULT_CHAIN)
			if (res) {
				getCoin()
				handleSwapPosted()
			}
			loading = false
		} else {
			updateActiveCard()
		}
	}

	function handleSwapPosted() {
		modalStore.trigger(modal);
		animate = true
		updateActiveCard()

		setTimeout(() => {
			animate = false
			modalStore.close();
		}, 1000)
	}

	function setCoin(func){
		func()
	}

	async function getCoin(){
		coin = await getCurrentCoin()
	}

	onMount(() => {
		// getLedgers()
		getCoin()
	});
</script>

<div class="success">
	{#if animate}
		<div
			transition:fly={
				{ 
					delay: 0,
					duration: 100,
					x: -50,
					y: 200,
					opacity: 0.5,
					easing: quintOut 
				}
			}
			>
			👍🏼 
		</div>
	{/if}
</div>
<div class="stack grid place-items-center mt-40">
	{#each cardDummyList as dummy (dummy)}
		<Card coin={coin} onbuttonTapped={handleIntention} />
	{/each}
	{#if loading}
		<div class="w-96">
			<ProgressBar value={undefined} />
		</div>
	{/if}
</div>

<style>
	.success {
		padding-top: 35px;
		height: 100px;
		width: 100%;
		z-index: 1000;
		text-align: center;
	}
  </style>
